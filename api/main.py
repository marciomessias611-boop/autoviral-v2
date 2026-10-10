"""
AutoViral v2 — entrypoint FastAPI.

- CORS whitelist (não "*")
- JWT + RBAC em todas as rotas sensíveis
- Global exception handler (sem vazar stacktrace)
- SSRF-safe download (validado em api/security.py)
- Lifespan handler inicializa DB (SQLModel) + semear secrets no Vault (se houver)
- Servir frontend estático
"""
from __future__ import annotations

import logging
import os
import time
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from pythonjsonlogger import jsonlogger
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST

from . import __version__
from .config import settings, ensure_dirs
from .core.database import init_db, close_db, get_engine
from .core.tracing import configure_tracing
from .core.vault_client import get_vault_client
from sqlalchemy import text
from .routers import api_router
from .security import get_current_user

logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter('%(asctime)s %(name)s %(levelname)s %(message)s')
logHandler.setFormatter(formatter)
logging.basicConfig(level=logging.INFO, handlers=[logHandler])
logger = logging.getLogger("autoviral.v2.main")

# Prometheus metrics
REQUEST_COUNT = Counter(
    'autoviral_request_count', 'Total request count', ['method', 'endpoint', 'http_status']
)
REQUEST_LATENCY = Histogram(
    'autoviral_request_latency_seconds', 'Request latency in seconds', ['method', 'endpoint']
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Validate critical secrets and schema; Vault writes are an explicit operator action."""
    settings.validate_runtime_secrets()
    ensure_dirs()
    await init_db()

    if settings.app_env != "test":
        try:
            configure_tracing(
                service_name="autoviral-api",
                jaeger_endpoint=os.getenv("JAEGER_ENDPOINT", "http://jaeger:14268/api/traces"),
            )
            logger.info("OpenTelemetry tracing enabled")
        except Exception as exc:  # noqa: BLE001
            logger.warning("Tracing setup skipped (%s)", type(exc).__name__)

    if settings.vault_required and not get_vault_client().available:
        raise RuntimeError("Vault is required but unavailable or unauthenticated")
    logger.info("AutoViral v2 starting (env=%s, debug=%s)", settings.app_env, settings.debug)
    yield
    await close_db()


def create_app() -> FastAPI:
    app = FastAPI(title="AutoViral v2", version=__version__, docs_url="/docs" if settings.debug else None,
                  description="Publish multi-platform: edit, schedule, multi-account. Secure by default.",
                  lifespan=lifespan)

    # CORS: forbids credentials + wildcard; origins from FRONTEND_ORIGIN (comma separated)
    origins = settings.get_cors_origins() or []
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=settings.cors_allow_credentials,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
    )

    # Rate limiting - use Redis in production, in-memory for tests/dev
    storage_uri = settings.redis_url if settings.redis_url else "memory://"
    limiter = Limiter(
        key_func=get_remote_address,
        default_limits=["100/minute"],
        storage_uri=storage_uri,
    )
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

    # Request logging and metrics middleware
    @app.middleware("http")
    async def log_and_metrics(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        # Normalize path for metrics (use route template instead of raw path)
        endpoint = request.url.path
        route = request.scope.get("route")
        if route and hasattr(route, "path"):
            endpoint = route.path
        
        # Log request as JSON (extra fields)
        logger.info(
            "Request processed",
            extra={
                "method": request.method,
                "endpoint": request.url.path,
                "status_code": response.status_code,
                "duration": process_time,
            }
        )
        # Update Prometheus metrics with normalized endpoint
        REQUEST_COUNT.labels(method=request.method, endpoint=endpoint, http_status=response.status_code).inc()
        REQUEST_LATENCY.labels(method=request.method, endpoint=endpoint).observe(process_time)
        return response

    # Security headers middleware
    @app.middleware("http")
    async def add_security_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        # Basic CSP: allow self, inline scripts and styles only if needed; we adjust as needed.
        response.headers["Content-Security-Policy"] = "default-src 'self';"
        return response

    # Exempt certain paths from rate limiting (health, docs, static)
    @app.middleware("http")
    async def exempt_static_paths(request: Request, call_next):
        if request.url.path.startswith("/health") or request.url.path.startswith("/docs") or \
           request.url.path.startswith("/openapi.json") or request.url.path.startswith("/static") or \
           request.url.path.startswith("/metrics"):
            request.state.view_rate_limit = False  # type: ignore
        return await call_next(request)

    # HSTS header (only in production with TLS)
    if settings.is_production:
        @app.middleware("http")
        async def add_hsts_header(request: Request, call_next):
            response = await call_next(request)
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
            return response

    @app.exception_handler(Exception)
    async def unhandled(request: Request, exc: Exception):  # noqa: ARG001
        logger.exception("unhandled error on %s %s", request.method, request.url.path)
        return JSONResponse(status_code=500, content={"detail": "internal error"})

    @app.get("/health")
    async def root_health():
        try:
            async with get_engine().connect() as connection:
                await connection.execute(text("SELECT 1"))
        except Exception as exc:  # noqa: BLE001
            logger.warning("Health check failed (%s)", type(exc).__name__)
            raise HTTPException(status_code=503, detail="database unavailable") from None
        if settings.vault_required and not get_vault_client().available:
            raise HTTPException(status_code=503, detail="vault unavailable")
        return {"status": "ok", "service": "autoviral-v2", "version": __version__}

    # Prometheus metrics endpoint - protected by authentication
    @app.get("/metrics")
    async def metrics(user: dict = Depends(get_current_user)):
        # Only admin can access metrics
        if "admin" not in user.get("roles", []):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

    # Serve static files (CSS, JS, images)
    app.mount("/static", StaticFiles(directory="api/static"), name="static")

    # Serve frontend
    @app.get("/", response_class=HTMLResponse)
    async def read_root():
        with open("api/static/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read(), status_code=200)

    app.include_router(api_router)
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )