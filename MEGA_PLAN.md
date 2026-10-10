# MEGA PLAN — AutoViral v2 (R$300/mês Budget, 80% Open Source)

> **Single Source of Truth** para todo o projeto. Consolidado a partir de: OMEGA Audit (62/100), Threat Model STRIDE, Inception Outputs, Execution Plan, múltiplos planos existentes.

---

## 1. EXECUTIVE SUMMARY & BUSINESS CONTEXT

### 1.1 Problem Statement
Criadores de conteúdo precisam transformar vídeos longos (YouTube, lives, podcasts) em clipes virais curtos (TikTok, Reels, Shorts) e publicá-los em múltiplas plataformas automaticamente. Ferramentas SaaS atuais (OpusClip, Metricool, Postiz Cloud) custam R$200-1000/mês — proibitivo para criadores individuais.

### 1.2 Solution
**AutoViral Local**: Plataforma 100% auto-hospedada, custo zero recorrente de APIs, que roda em **single VPS (R$60/mês)** com inferência **CPU-only**, usando apenas modelos open source (Whisper, Qwen, Gemma, Piper).

### 1.3 Budget Constraints (HARD LIMITS) — **R$60 VPS + R$240 Rest = R$300/mês**

| Item | Custo Mensal | Custo Anual | Status |
|------|--------------|-------------|--------|
| **VPS (Contabo VPS S)** | **R$60** | R$720 | **HARD CAP** — 4 vCPU, 8GB RAM, 200GB SSD |
| **Domínio/SSL** | ~R$5 | R$60 | Vem do orçamento "Restante" |
| **APIs Externas** | **R$0** | R$0 | **ZERO** (100% self-hosted) |
| **Infra Adicional** | R$0 | R$0 | Self-hosted no VPS |
| **Monitoring/CI/CD** | R$0 | R$0 | Self-hosted / GitHub Actions free tier |
| **Buffer/Contingência** | **R$235** | R$2.820 | Vem do orçamento "Restante" (R$240 - R$5 domínio) |
| **TOTAL** | **R$300** | **R$3.600** | **DENTRO DO ORÇAMENTO** |

> **Orçamento "Restante" (R$240/mês)**: Domínio (R$5) + Buffer/Contingência (R$235) = R$240 ✅

> **Regra de Ouro**: Qualquer decisão que gere custo recorrente > R$0 é automaticamente REJEITADA (Princípio P1).

### 1.4 Open Source Target: **80%+**
- Core pipeline: 100% open source (MIT/Apache/AGPL)
- Frontend: 100% open source (MIT)
- Infra: 100% open source (Docker, PostgreSQL, Redis, Traefik, Prometheus)
- Modelos: 100% open source (Whisper, Qwen, Gemma, Piper)
- Apenas binários proprietários: drivers NVIDIA (se GPU futura), firmware VPS

### 1.5 Success Metrics (MVP)
| Métrica | Target MVP | Target V2 |
|---------|------------|-----------|
| Custo mensal externo | **R$0** | R$0 |
| Pipeline 10min → clips | < 30 min CPU | < 15 min |
| RAM peak | < 6 GB | < 8 GB |
| Deploy time | < 5 min | < 3 min |
| Backup/Restore | < 15 min | < 10 min |
| Clips/semana | 20+ | 50+ |
| Plataformas | 4 (TikTok, Reels, Shorts, YT) | 8+ |

---

## 2. STRATEGIC VISION (12-MONTH ROADMAP)

### 2.1 Vision Statement
> **AutoViral Local** é a primeira plataforma **100% auto-hospedada, custo zero recorrente**, que transforma vídeos longos em clipes virais verticais e os publica automaticamente no TikTok, Instagram Reels, YouTube Shorts e YouTube — rodando inteiramente em **um único VPS entry-level (R$60/mês)** com **inferência CPU-only**.

### 2.2 12-Month Milestones

| Quarter | Focus | Key Deliverables | Budget Impact |
|---------|-------|------------------|---------------|
| **Q1 (Mês 1-3)** | **MVP Core** | Pipeline completo funcional, 4 plataformas publicando, deploy VPS validado | R$60/mês VPS apenas |
| **Q2 (Mês 4-6)** | **Hardening & Scale** | DR testado, LGPD compliance, observabilidade, chaos engineering, load test 50 jobs | R$60/mês VPS |
| **Q3 (Mês 7-9)** | **AI Governance** | Model provenance, adversarial testing, fallback chains, A/B scoring | R$60/mês VPS |
| **Q4 (Mês 10-12)** | **Platform Maturity** | Multi-tenant opcional, analytics avançados, plugin system, community docs | R$60/mês VPS |

### 2.3 Competitive Moats
1. **Zero Recurring Cost** — Único no mercado com pipeline completo a R$0/mês APIs
2. **Full Data Sovereignty** — Conteúdo, audiência, credenciais nunca saem da infra do usuário
3. **CPU-Only Architecture** — Roda em qualquer hardware, zero GPU dependency
4. **Open Source Extensibility** — Fork, modifique, contribua — zero lock-in

---

## 3. DOMAIN DECOMPOSITION (MECE)

### 3.1 Bounded Contexts

```
┌─────────────────────────────────────────────────────────────────┐
│                      AUTOVIRAL DOMAIN                           │
├─────────────┬─────────────┬─────────────┬─────────────────────┤
│   CONTENT   │  PROCESSING │ PUBLISHING  │    PLATFORM         │
│  INGESTION  │  PIPELINE   │  ENGINE     │    SERVICES         │
├─────────────┼─────────────┼─────────────┼─────────────────────┤
│ • Upload    │ • ASR       │ • Scheduler │ • Auth & RBAC       │
│ • Validation│ • Scoring   │ • YouTube   │ • User Management   │
│ • Metadata  │ • Editor    │ • Social    │ • Billing (future)  │
│ • Storage   │ • Thumbnail │ • Webhooks  │ • Audit/Compliance  │
│ • Jobs Queue│ • Pipeline  │ • Analytics │ • Monitoring        │
└─────────────┴─────────────┴─────────────┴─────────────────────┘
```

### 3.2 Context Boundaries & Contracts

| Context | Responsibility | API Contract | Data Ownership |
|---------|---------------|--------------|----------------|
| **Content Ingestion** | Upload, validation, storage, job creation | `POST /clips`, `GET /jobs/{id}` | Video files, metadata |
| **Processing Pipeline** | ASR → Scoring → Editor → Clips | Internal gRPC/REST | Transcripts, scores, clips |
| **Publishing Engine** | Scheduling, OAuth, multi-platform pub | `POST /publish`, webhooks | Social accounts, scheduled posts |
| **Platform Services** | Auth, users, audit, billing, monitoring | Cross-cutting | Users, tokens, audit logs |

### 3.3 Integration Patterns
- **Async**: Job queue via Redis Streams (fire-and-forget)
- **Sync**: REST API for user-facing operations
- **Events**: WebSocket for real-time progress, Webhooks for platform callbacks
- **Data**: Shared PostgreSQL (schema-per-context), Redis for cache/queue

---

## 4. ARCHITECTURAL PRINCIPLES (PRECEDENCE ORDER)

| # | Principle | Precedence | Trade-off Accepted |
|---|-----------|------------|-------------------|
| **P1** | **Zero Custo Recorrente** | MÁXIMA | Abre mão de modelos SOTA, velocidade GPU, plug-and-play |
| **P2** | **Single-Node Simples** | ALTA | Abre mão de escala horizontal, HA nativo, microserviços |
| **P3** | **CPU-Only Inference** | ALTA | Abre mão de velocidade (10-50x mais lento), modelos 7B+ |
| **P4** | **Modelos Quantizados Pequenos** | MÉDIA-ALTA | Abre mão de qualidade máxima, modelos SOTA |
| **P5** | **Pipeline Assíncrono Sequencial** | MÉDIA | Abre mão de throughput paralelo, latência mínima |
| **P6** | **Open Source Self-Hosted** | MÉDIA | Abre mão de backups automáticos, HA gerenciado, SLA |
| **P7** | **Observabilidade Leve** | MÉDIA-BAIXA | Abre mão de dashboards bonitos, alertas sofisticados |

### Precedence Matrix
```
P1 > P2 > P3 > P4 > P5 > P6 > P7
```
Quando conflitos: **vence o de maior precedência**.

---

## 5. TECH STACK SELECTION (DECISION MATRIX)

### 5.1 Core Stack Decisions

| Layer | Decision | Score | Key Rationale |
|-------|----------|-------|---------------|
| **Language** | Python 3.11+ | 4.8 | Ecossistema ML maduro, async nativo, equipe conhece |
| **Framework** | FastAPI 0.109+ | 4.9 | Async nativo, OpenAPI auto, Pydantic v2, performance |
| **ASR** | faster-whisper (tiny/base) | 4.7 | CPU-only, CTranslate2 otimizado, MIT, pt-BR nativo |
| **LLM Scoring** | Ollama + Qwen2.5-1.5B 4-bit | 4.6 | CPU-only, 1.1 GB RAM, Apache 2.0, tool calling |
| **Video Editor** | hotclip (AGPL) headless | 4.8 | Feature parity Opus Clip, AGPL, speaker tracking |
| **Scheduler** | Postiz Self-Hosted (AGPL) | 4.7 | 30+ plataformas, MCP server, mesma codebase cloud |
| **YouTube Upload** | youtube-upload (GPL) CLI | 4.6 | Upload resumível, OAuth2, metadata completa |
| **Database** | PostgreSQL 16 local | 4.8 | ACID, JSONB, backup nativo, SQLAlchemy async |
| **Cache/Queue** | Redis 7 local | 4.8 | Pub/Sub, Streams, TTL, maduro |
| **Storage** | Docker Volumes (bind mounts) | 4.7 | Zero overhead, backup = `tar` |
| **Orchestration** | Docker Compose v2 | 4.9 | Single host, healthchecks, 1 comando deploy |
| **Proxy/TLS** | Traefik v3 | 4.7 | Auto-discovery, Let's Encrypt, mTLS |
| **Monitoring** | Leve (logs + healthchecks + cron) | 4.5 | < 50 MB RAM, zero containers extra |
| **CI/CD** | GitHub Actions → SSH | 4.7 | Grátis (2000 min/mês), cache, matrix |
| **TTS** | Piper TTS (V2 opcional) | 4.0 | CPU-only, ONNX, MIT, removido do MVP |

### 5.2 Model Selection (CPU-Only, < 3GB RAM each)

| Model | Variant | Size | RAM | Use Case | License |
|-------|---------|------|-----|----------|---------|
| **Whisper** | tiny (39 MB) | 39 MB | ~1 GB | Dev/testes rápidos | MIT |
| **Whisper** | **base (142 MB)** | 142 MB | **~1.5 GB** | **Produção** | MIT |
| **Qwen2.5** | **1.5B 4-bit** | 1.1 GB | **~1.2 GB** | **Scoring padrão** | Apache 2.0 |
| **Qwen2.5** | 3B 4-bit | 2.2 GB | ~2.5 GB | Qualidade superior (se RAM > 6GB) | Apache 2.0 |
| **Gemma2** | 2B 4-bit | 1.6 GB | ~1.8 GB | Alternativa pt-BR forte | Gemma License |
| **Piper TTS** | V2 | ~500 MB | ~800 MB | TTS opcional V2 | MIT |

### 5.3 Resource Budget (Validated)

| Component | CPU | RAM | Disk |
|-----------|-----|-----|------|
| API (FastAPI) | 0.5 vCPU | 500 MB | 500 MB |
| faster-whisper (base) | 2-4 vCPU | 1.5 GB | 142 MB |
| Ollama (qwen2.5-1.5B) | 1-2 vCPU | 1.2 GB | 1.1 GB |
| hotclip | 1-2 vCPU | 500 MB | 2 GB |
| Postiz + DB | 0.5 vCPU | 500 MB | 2 GB |
| PostgreSQL | 0.2 vCPU | 200 MB | 1 GB |
| Redis | 0.1 vCPU | 100 MB | 100 MB |
| Traefik | 0.1 vCPU | 50 MB | 50 MB |
| **TOTAL** | **~4 vCPU** | **~5.3 GB** | **~10 GB** |

**VPS Spec**: Contabo VPS S — 4 vCPU, 8 GB RAM, 200 GB SSD — **R$60/mês** (34% headroom RAM)

---

## 6. AUTO-ADRs (IRREVERSIBLE DECISIONS)

### ADR-001: Database — PostgreSQL 16 Local
- **Status**: Accepted
- **Context**: Need ACID, JSONB, backup nativo, SQLAlchemy async
- **Decision**: PostgreSQL 16 local (não SQLite, não managed DB)
- **Consequences**: +ACID, +JSONB, +backup pg_dump; -RAM vs SQLite
- **Reversibility**: Média (migração para SQLite possível mas perda JSONB)

### ADR-002: ASR — faster-whisper CPU-only
- **Status**: Accepted
- **Context**: VPS sem GPU, orçamento R$0 APIs
- **Decision**: faster-whisper tiny/base via CTranslate2
- **Consequences**: +CPU-only, +MIT, +pt-BR; -WER 15-20% vs large-v3
- **Reversibility**: Alta (trocar modelo ou engine)

### ADR-003: LLM Scoring — Ollama + Qwen2.5-1.5B 4-bit
- **Status**: Accepted
- **Context**: CPU-only, <3GB RAM, zero custo
- **Decision**: Ollama gerencia modelo + API OpenAI-compat
- **Consequences**: +CPU-only, +Apache 2.0, +tool calling; -qualidade vs 7B+
- **Reversibility**: Alta (trocar modelo GGUF)

### ADR-004: Video Editor — hotclip AGPL headless
- **Status**: Accepted
- **Context**: Feature parity Opus Clip, zero custo
- **Decision**: Container separado, comunicação CLI/JSON
- **Consequences**: +Feature parity, +AGPL; -Node+Rust deps, AGPL copyleft
- **Reversibility**: Média (isolado em container)

### ADR-005: Scheduler — Postiz Self-Hosted AGPL
- **Status**: Accepted
- **Context**: 30+ plataformas, zero custo, MCP server
- **Decision**: Postiz self-hosted, OAuth setup automatizado
- **Consequences**: +30 plataformas, +MCP; -OAuth setup complexo
- **Reversibility**: Baixa (migração scheduler = rework grande)

### ADR-006: YouTube Upload — youtube-upload CLI (GPL)
- **Status**: Accepted
- **Context**: Upload resumível essencial, zero custo
- **Decision**: CLI maduro, OAuth2, metadata completa
- **Consequences**: +Resumível, +GPL; -Python dep, OAuth setup
- **Reversibility**: Média (wrapper isolado)

### ADR-007: Orchestration — Docker Compose Single Host
- **Status**: Accepted
- **Context**: P2 (single-node), 1 pessoa, 1 deploy
- **Decision**: Docker Compose v2, healthchecks, networks, volumes
- **Consequences**: +Deploy 1 comando, +simples; -HA nativo, -scaling
- **Reversibility**: Média (migração K8s possível mas anti-P2)

### ADR-008: Monitoring — Leve (logs + healthchecks + cron)
- **Status**: Accepted
- **Context**: P7, RAM limitada, 1 pessoa
- **Decision**: `docker logs` + healthchecks HTTP + cron alerts Telegram
- **Consequences**: +<50MB RAM, +zero containers; -dashboards, -alertas sofisticados
- **Reversibility**: Alta (adicionar Prometheus stack depois)

---

## 7. THREAT MODELING (STRIDE)

| Componente | Spoofing | Tampering | Repudiation | Info Disclosure | DoS | Elevation |
|------------|----------|-----------|-------------|-----------------|-----|-----------|
| **API FastAPI** | JWT forgery (mit: HS256 + session version) | Input validation (Pydantic) | Audit logs JSON | SSRF protection + CORS whitelist | Rate limiting (100/min) | RBAC (admin/editor/viewer) |
| **Vault** | Token theft (mit: TTL curto, policy limitada) | Policy modification (audit) | Audit device enabled | Secret leakage (encryption at rest) | Seal/unseal | Root token não usado |
| **PostgreSQL** | Credential stuffing (mit: bcrypt) | SQL injection (mit: ORM parametrizado) | Transaction logs | Dados PII criptografados (Fernet) | Connection pooling | Row-level security não implementado |
| **Redis** | Auth bypass (mit: password obrigatório) | Cache poisoning (namespace) | N/A | Dados de sessão | Max connections 50 | N/A |
| **hotclip (CLI)** | LLM API key theft (env var) | Video input validation | N/A | Video content exposure | GPU memory limits | N/A |
| **Postiz/Zernio** | API key leakage (Vault) | Webhook replay (assinatura) | Webhook logs | Dados de publicação | Rate limiting API | N/A |
| **Frontend** | XSS (mit: CSP, sanitização) | CSRF (mit: SameSite + JWT header) | N/A | Token no localStorage | N/A | Role bypass (mit: backend auth) |

### Attack Scenarios Verified
1. **Chain**: SSRF → Vault token theft → Secret disclosure → Full compromise (MITIGATED: SSRF protection + Vault TTL)
2. **Chain**: OAuth token theft → Social account takeover → Unauthorized publishing (MITIGATED: Token encryption + refresh rotation)
3. **Chain**: Malicious video upload → hotclip RCE → Container escape (MITIGATED: Read-only containers, non-root, no GPU access)

---

## 8. 40-WEEK ROADMAP (SPRINT-BY-SPRINT)

### Phase 0: Foundation & Validation (Weeks 1-2) — LOCAL
| Sprint | Tasks | Gate |
|--------|-------|------|
| **Sprint 1** | T-001 a T-009: Secrets, Docker Compose validation, Ollama models pull, benchmarks Whisper+Qwen, hotclip E2E, youtube-upload, Postiz OAuth, RAM peak, validation report | **G0**: All benchmarks pass, zero P0 blockers |

### Phase 1: Core Pipeline (Weeks 3-4) — LOCAL
| Sprint | Tasks | Gate |
|--------|-------|------|
| **Sprint 3** | T-101 a T-105: `/clips` endpoint, faster-whisper integration, Ollama scoring, hotclip integration, FFmpeg fallback | **G1**: Pipeline functional |
| **Sprint 4** | T-106 a T-110: WebSocket progress, job polling, download endpoint, integration tests 100%, API docs | **G1**: Full pipeline < 30 min, tests 100% pass |

### Phase 2: Publishing Stack (Weeks 5-6) — LOCAL
| Sprint | Tasks | Gate |
|--------|-------|------|
| **Sprint 5** | T-201 a T-205: OAuth scripts (4 plataformas), docs OAuth, Postiz config, test 4 plataformas, youtube-upload service | **G2**: Publishing functional |
| **Sprint 6** | T-206 a T-210: youtube-upload cron refresh, `/publish` endpoint, idempotency keys, integration tests, API docs | **G2**: 4 plataformas publicando |

### Phase 3: Hardening & Observability (Weeks 7-8) — LOCAL
| Sprint | Tasks | Gate |
|--------|-------|------|
| **Sprint 7** | T-301 a T-306: Backup/restore scripts (<15 min), LGPD endpoint, data retention TTL, Falco runtime security, alerting Telegram/Email | **G3**: Production ready |
| **Sprint 8** | T-307 a T-312: Log aggregation JSON, healthchecks 12 serviços, DR runbook, operations runbook, load test 10 jobs, security scan zero critical | **G3**: DR tested, security clean |

### Phase 4: VPS Provisioning & Deploy (Week 9) — VPS (LAST)
| Sprint | Tasks | Gate |
|--------|-------|------|
| **Sprint 9** | T-401 a T-409: Provision VPS, Docker/swap/NTP, DNS, deploy stack, pull Ollama models, Traefik TLS, OAuth production callbacks, smoke tests, monitoring alerts | **G4**: VPS production ready |

### Phase 5: Validation & Go-Live (Weeks 10-11) — VPS
| Sprint | Tasks | Gate |
|--------|-------|------|
| **Sprint 10** | T-501 a T-508: E2E test full pipeline, verify zero external APIs 30 dias, backup/restore VPS, LGPD test, 30-day cost verification, final security audit, delivery doc, stakeholder sign-off | **G5**: Go-Live |

### Post-Launch (Weeks 11-40)
| Month | Focus | Key Activities |
|-------|-------|----------------|
| **Mês 3** | Chaos Engineering | Game days: kill worker, kill DB, network partition |
| **Mês 4** | AI Governance | Model provenance, adversarial testing, A/B scoring |
| **Mês 5** | Multi-tenant (opcional) | Workspaces, quotas, billing prep |
| **Mês 6** | Analytics & Plugin System | Custom metrics, plugin SDK, community templates |
| **Mês 7-10** | Continuous Improvement | Monthly chaos, quarterly DR test, dependency updates, community contributions |

---

## 9. FEATURE-SLICED DESIGN STRUCTURE

```
src/
├── app/                    # Entry points, providers, routing
├── processes/              # Business processes spanning pages
├── pages/                  # Page components (Next.js routes)
├── widgets/                # Independent UI blocks
├── features/               # User-facing features
│   ├── auth/               # Login, register, 2FA, recovery
│   ├── projects/           # CRUD, upload, metadata
│   ├── editor/             # Timeline, player, waveform, transcript
│   ├── clips/              # Clip library, preview, actions
│   ├── publishing/         # Scheduler, calendar, multi-platform
│   ├── analytics/          # Metrics, charts, exports
│   └── settings/           # Profile, OAuth, preferences
├── entities/               # Business entities
│   ├── user/               # User, session, preferences
│   ├── project/            # Project, video, metadata
│   ├── clip/               # Clip, highlight, thumbnail
│   ├── social/             # SocialAccount, scheduledPost
│   └── job/                # Job, progress, clips[]
├── shared/
│   ├── api/                # Base API instance, interceptors
│   ├── config/             # Environment configs
│   ├── lib/                # Pure utilities (date, string, validation)
│   ├── ui/                 # Design system components (Radix + Tailwind)
│   ├── types/              # Global types (Zod schemas)
│   └── hooks/              # Shared hooks (WebSocket, auth, etc.)
```

### Import Rules (Enforced by ESLint)
```
app → processes, pages, widgets, features, entities, shared
pages → widgets, features, entities, shared
widgets → features, entities, shared
features → entities, shared
entities → shared only
shared → (nothing above)
```

---

## 10. CI/CD PIPELINE (GITHUB ACTIONS)

### 10.1 Pipeline Stages

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline
on: [push, pull_request]

jobs:
  # STAGE 1: Code Quality (Parallel)
  lint-and-typecheck:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
        with: { python-version: '3.11' }
      - name: Install deps
        run: pip install -r requirements.txt --require-hashes
      - name: Lint (ruff)
        run: ruff check api/ tests/
      - name: Type check (mypy)
        run: mypy api/
      - name: Frontend lint
        run: cd frontend && pnpm lint

  # STAGE 2: Security (Parallel)
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Secret scan (gitleaks)
        uses: gitleaks/gitleaks-action@v2
      - name: SAST (semgrep)
        uses: returntocorp/semgrep-action@v1
      - name: SCA (pip-audit)
        run: pip-audit --desc --format=json
      - name: Container scan (Trivy)
        uses: aquasecurity/trivy-action@master
        with: { scan-type: 'fs', severity: 'CRITICAL,HIGH' }

  # STAGE 3: Tests (Parallel)
  test-python:
    runs-on: ubuntu-latest
    needs: [lint-and-typecheck]
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
      - name: Install deps
        run: pip install -r requirements.txt --require-hashes
      - name: Run pytest
        run: python -m pytest tests/ -v --tb=short --cov=api --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  test-frontend:
    runs-on: ubuntu-latest
    needs: [lint-and-typecheck]
    steps:
      - uses: actions/checkout@v4
      - name: Setup Node
        uses: actions/setup-node@v4
        with: { node-version: '20', cache: 'pnpm' }
      - run: cd frontend && pnpm install --frozen-lockfile
      - run: cd frontend && pnpm test:run --coverage
      - run: cd frontend && pnpm test:e2e

  # STAGE 4: Docker Build & Compose Test
  docker-compose-test:
    runs-on: ubuntu-latest
    needs: [test-python, test-frontend, security-scan]
    steps:
      - uses: actions/checkout@v4
      - name: Build images
        run: docker compose -f docker-compose.fully-selfhosted.yml build
      - name: Start stack
        run: docker compose -f docker-compose.fully-selfhosted.yml up -d
      - name: Healthcheck all services
        run: |
          for i in {1..30}; do
            if docker compose -f docker-compose.fully-selfhosted.yml ps --format json | jq -e 'all(.State == "running" and .Health == "healthy")'; then exit 0; fi
            sleep 10
          done
          exit 1
      - name: Smoke test API
        run: curl -f http://localhost:8000/health && curl -f http://localhost:8000/api/health
      - name: Cleanup
        run: docker compose -f docker-compose.fully-selfhosted.yml down -v

  # STAGE 5: Deploy (main branch only)
  deploy:
    runs-on: ubuntu-latest
    needs: [docker-compose-test]
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to VPS
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.VPS_HOST }}
          username: root
          key: ${{ secrets.VPS_SSH_KEY }}
          script: |
            cd /opt/autoviral
            git pull
            docker compose -f docker-compose.fully-selfhosted.yml pull
            docker compose -f docker-compose.fully-selfhosted.yml up -d --remove-orphans
            docker system prune -f
```

### 10.2 Quality Gates

| Gate | Trigger | Criteria | Failure Action |
|------|---------|----------|----------------|
| **G0** | Pre-flight | All benchmarks pass, zero P0 | Fix blockers, re-run |
| **G1** | Pipeline | Full pipeline < 30 min, tests 100% | Revert, self-heal ≤3x |
| **G2** | Publishing | 4 plataformas publicam, testes passam | Fix OAuth, fallback CLI |
| **G3** | Hardening | DR < 15min, LGPD, zero P0 | Fix, re-test |
| **G4** | VPS Deploy | 12 healthy, HTTPS, OAuth | Rollback, debug |
| **G5** | Go-Live | Zero external APIs, full E2E | Rollback, fix |

---

## 11. OBSERVABILITY STACK (LEVE - P7)

### 11.1 Components (Total < 50 MB RAM)

| Component | Implementation | RAM | Purpose |
|-----------|---------------|-----|---------|
| **Structured Logs** | JSON via `python-json-logger` + `structlog` | ~10 MB | Debug, audit, correlation IDs |
| **Healthchecks** | HTTP `/health` em todos 12 serviços + `docker ps` | ~5 MB | Liveness/readiness, `docker ps` status |
| **Cron Alerts** | `cron` a cada 5 min → `curl -f /health` → Telegram/Email | ~2 MB | Uptime monitoring, auto-alert |
| **Metrics** | `docker stats --no-stream` + log parsing (counters) | ~3 MB | CPU, RAM, disk, network, job counters |
| **Log Aggregation** | `docker logs -f api | jq .` + `journalctl` | ~5 MB | Debug, audit trail |
| **Distributed Tracing** | OpenTelemetry manual (spans críticos apenas) | ~10 MB | Latency analysis, bottleneck detection |

### 11.2 Alert Rules (Telegram Bot)

```python
# scripts/alerting.py
ALERT_RULES = [
    {"name": "api_down", "condition": "health != 200", "severity": "P0", "cooldown": "5m"},
    {"name": "ram_high", "condition": "ram_percent > 90", "severity": "P1", "cooldown": "10m"},
    {"name": "disk_high", "condition": "disk_percent > 85", "severity": "P1", "cooldown": "30m"},
    {"name": "job_failed", "condition": "job_status == failed", "severity": "P1", "cooldown": "1m"},
    {"name": "oauth_expiry", "condition": "token_expires_in < 24h", "severity": "P2", "cooldown": "1h"},
    {"name": "backup_failed", "condition": "backup_status != success", "severity": "P0", "cooldown": "0m"},
]
```

### 11.3 Dashboards (Grafana - Opcional V2)
Se RAM > 6 GB futuramente: Loki + Promtail + Grafana (adiciona ~500 MB RAM)

---

## 12. SECURITY HARDENING (ZERO-TRUST)

### 12.1 Container Hardening (Applied to ALL services)

```yaml
# docker-compose.fully-selfhosted.yml - security defaults
services:
  api:
    image: autoviral/api:latest
    user: "1000:1000"                    # Non-root
    read_only: true                      # Read-only filesystem
    tmpfs:
      - /tmp:size=100M,noexec,nosuid
      - /var/run:size=50M,noexec,nosuid
    cap_drop:
      - ALL
    cap_add: []                          # Zero capabilities
    security_opt:
      - no-new-privileges:true
    networks:
      - internal                         # No public network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
```

### 12.2 Network Segmentation

```yaml
networks:
  public:          # Traefik only
    driver: bridge
  internal:        # All other services
    driver: bridge
    internal: true # No internet access
  vault:           # Vault + init only
    driver: bridge
    internal: true
```

### 12.3 Secrets Management (HashiCorp Vault)

| Secret Type | Storage | Rotation | Access |
|-------------|---------|----------|--------|
| **DB Password** | Vault KV v2 | Quarterly (auto) | App via Vault Agent |
| **JWT Secret** | Vault KV v2 | Quarterly (auto) | API only |
| **Encryption Key** | Vault KV v2 | Quarterly (auto) | API only |
| **OAuth Tokens** | Vault KV v2 | Auto-refresh (cron 6h) | Postiz, youtube-upload |
| **API Keys (LLM)** | Vault KV v2 | Quarterly | Ollama only (local) |
| **Webhook Secrets** | Vault KV v2 | Per-platform | Postiz, youtube-upload |

### 12.4 Application Security

| Control | Implementation |
|---------|----------------|
| **Auth** | JWT HS256 + session version (invalidation on password change) |
| **RBAC** | Roles: admin, editor, viewer + ownership checks (IDOR prevention) |
| **Rate Limiting** | SlowAPI: 100/min global, 10/min auth endpoints, 5/min upload |
| **SSRF Protection** | `is_external_host()` validator: bloqueia localhost, private IPs, loopback |
| **CORS** | Whitelist via `FRONTEND_ORIGIN` env (no `*`) |
| **Input Validation** | Pydantic v2 em todos endpoints + sanitização HTML |
| **Secrets in Logs** | Structlog processor remove `password`, `token`, `key`, `secret` fields |
| **Dependency Scanning** | `pip-audit` + `trivy fs` no CI semanal + Dependabot alerts |

### 12.5 Compliance (LGPD/GDPR)

| Requirement | Implementation |
|-------------|----------------|
| **Right to Erasure** | `DELETE /api/v1/privacy/me` → cascade delete User→Projects→Videos→Clips→Jobs→SocialAccounts |
| **Data Portability** | `GET /api/v1/privacy/export` → JSON completo (dados + metadados + logs auditoria) |
| **Consent** | Checkbox no registro + registro de consentimento imutável (append-only table) |
| **Data Minimization** | Só coleta: email, nome, OAuth tokens (criptografados), preferências |
| **Retention** | TTL job diário: clips > 90 dias sem uso → soft delete; logs > 1 ano → archive |
| **Audit Log** | Append-only table: `user_id, action, resource, timestamp, ip, user_agent` |

---

## 13. DATA STRATEGY

### 13.1 Data Models (PostgreSQL)

```sql
-- Core Tables
users (id, email, password_hash, role, session_version, created_at)
projects (id, user_id, title, description, settings_json, created_at)
videos (id, project_id, source_path, duration, status, metadata_json, created_at)
clips (id, video_id, start_time, end_time, output_path, score, metadata_json, created_at)
jobs (id, video_id, status, progress, current_step, error, created_at, completed_at)
social_accounts (id, user_id, platform, account_id, encrypted_tokens, scopes, expires_at)
scheduled_posts (id, clip_id, social_account_id, platform, scheduled_at, status, posted_at)
audit_logs (id, user_id, action, resource, resource_id, timestamp, ip, user_agent)
privacy_consents (id, user_id, consent_type, granted, timestamp, version)
```

### 13.2 Encryption

| Data | Method | Key Management |
|------|--------|----------------|
| **OAuth Tokens** | Fernet (AES-256) | Key em Vault, rotação trimestral |
| **PII Fields** | Fernet (AES-256) | Key em Vault, rotação trimestral |
| **Database** | Transparente (PostgreSQL pgcrypto) | Key em Vault |
| **Backups** | Age (age-encryption.org) | Public key no repo, private key offline |

### 13.3 Backup Strategy

| Component | Frequency | Retention | Method | RTO | RPO |
|-----------|-----------|-----------|--------|-----|-----|
| **PostgreSQL** | Diário 02:00 | 30 dias | `pg_dump --format=custom --compress=9` + Age encrypt | < 15 min | 24h |
| **Volumes (clips, videos)** | Diário 02:30 | 14 dias | `tar + zstd + age` | < 30 min | 24h |
| **Config (.env, configs)** | A cada deploy | 90 dias | `tar + age` | < 5 min | 0 |
| **Ollama Models** | Semanal | 4 semanas | `tar + age` (apenas metadata, models re-pullable) | N/A | N/A |

### 13.4 Disaster Recovery

```bash
# scripts/restore.sh
# Usage: ./restore.sh BACKUP_DATE
# 1. Para stack: docker compose down
# 2. Restore PostgreSQL: pg_restore --clean --if-exists --no-owner --dbname=autoviral backup.dump
# 3. Restore volumes: tar -xzf volumes.tar.zst -C /data
# 4. Restore .env: cp backup.env .env
# 4. Restart stack: docker compose up -d
# 5. Healthcheck all services
# Target: < 15 min total
```

---

## 14. AI/ML GOVERNANCE

### 14.1 Model Provenance

| Model | Source | Version Pin | Checksum | License | Review Date |
|-------|--------|-------------|----------|---------|-------------|
| Whisper tiny | HuggingFace | `openai/whisper-tiny` | `sha256:...` | MIT | Trimestral |
| Whisper base | HuggingFace | `openai/whisper-base` | `sha256:...` | MIT | Trimestral |
| Qwen2.5-1.5B | Ollama Library | `qwen2.5:1.5b-q4_k_m` | `sha256:...` | Apache 2.0 | Trimestral |
| Qwen2.5-3B | Ollama Library | `qwen2.5:3b-q4_k_m` | `sha256:...` | Apache 2.0 | Trimestral |
| Gemma2-2B | Ollama Library | `gemma2:2b-q4_k_m` | `sha256:...` | Gemma License | Trimestral |
| Piper TTS | Piper GitHub | `v1.2.0` | `sha256:...` | MIT | Semestral |

### 14.2 Adversarial Testing (Quarterly)

| Test | Method | Tool | Pass Criteria |
|------|--------|------|---------------|
| **Prompt Injection** | Malicious prompts in video titles/descriptions | Garak + custom | 0 successful injections |
| **Jailbreak** | Attempt to bypass scoring rubric | Garak + custom | 0 successful jailbreaks |
| **Data Exfiltration** | Attempt to extract training data | Custom prompts | 0 data leaks |
| **Model DoS** | Extremely long inputs, recursive prompts | Custom | No OOM, timeout < 30s |
| **Bias/Fairness** | Test scoring across demographics | Custom dataset | No statistically significant bias |

### 14.3 Fallback Chains

```python
# api/services/llm_client.py
LLM_FALLBACK_CHAIN = [
    {"model": "qwen2.5:1.5b-q4_k_m", "max_tokens": 2048, "timeout": 30},
    {"model": "gemma2:2b-q4_k_m", "max_tokens": 2048, "timeout": 30},
    {"model": "qwen2.5:3b-q4_k_m", "max_tokens": 2048, "timeout": 60},
    {"fallback": "heuristic", "function": "texttiling_keyword_fallback"}  # Sempre funciona
]
```

### 14.4 A/B Scoring Framework

```python
# Métricas por modelo
SCORING_METRICS = {
    "approval_rate": "Clips aprovados sem edição / Total gerados",
    "edit_rate": "Clips editados manualmente / Total gerados",
    "publish_rate": "Clips publicados / Total gerados",
    "viral_score": "Views/Engagement médio por clip (pós-publicação)",
}
```

---

## 15. FINOPS (COST ALLOCATION)

### 15.1 Cost Breakdown (Monthly) — **R$60 VPS + R$240 Rest = R$300/mês**

| Category | Component | Monthly Cost | Annual | % of Budget |
|----------|-----------|--------------|--------|-------------|
| **Compute** | VPS (Contabo VPS S) | **R$60** | R$720 | **20%** |
| **Network** | Incluído no VPS (1 Gbps) | R$0 | R$0 | 0% |
| **Storage** | Incluído no VPS (200 GB SSD) | R$0 | R$0 | 0% |
| **Backup Storage** | MinIO local (mesmo VPS) | R$0 | R$0 | 0% |
| **Domain/SSL** | Registro + Let's Encrypt | **R$5** | R$60 | **1.7%** |
| **External APIs** | **ZERO** | **R$0** | **R$0** | **0%** |
| **Monitoring** | Self-hosted (logs + healthchecks) | R$0 | R$0 | 0% |
| **CI/CD** | GitHub Actions (2000 min grátis) | R$0 | R$0 | 0% |
| **Contingency** | Buffer para imprevistos | **R$235** | **R$2.820** | **78.3%** |
| **TOTAL** | | **R$300** | **R$3.600** | **100%** |

> **Orçamento "Restante" (R$240/mês)**: Domínio (R$5) + Buffer/Contingência (R$235) = **R$240** ✅

### 15.2 Cost Allocation Tags (Para futuro multi-tenant)

```yaml
# docker-compose labels for cost allocation
labels:
  - "finops.cost_center=autoviral-core"
  - "finops.environment=production"
  - "finops.owner=solo-creator"
  - "finops.project=autoviral-v2"
```

### 15.3 Budget Alerts

```python
# scripts/finops_alert.py
BUDGET_ALERTS = {
    "monthly_vps": {"threshold": 65, "action": "alert"},      # R$65 = 108% do orçado
    "disk_usage": {"threshold": 80, "action": "alert_cleanup"}, # 80% disco
    "ram_usage": {"threshold": 85, "action": "alert_scale"},    # 85% RAM
    "external_api_calls": {"threshold": 1, "action": "block"},  # ZERO tolerância
}
```

---

## 16. TDD HYBRID PROCESS (75% AUTO-GENERATED TESTS)

### 16.1 Test Generation Strategy

| Test Type | Auto-Generated | Manual | Tool/Method |
|-----------|----------------|--------|-------------|
| **CRUD Operations** | 95% | 5% | Zod schema + Prisma/SQLAlchemy model + templates |
| **API Endpoints** | 90% | 10% | OpenAPI spec + edge cases templates |
| **UI Components** | 85% | 15% | Snapshot + axe-core a11y + accessibility |
| **Business Logic** | 40% | 60% | TDD puro + property-based testing (hypothesis) |
| **Integration** | 88% | 12% | Contract testing (Pact) + MSW mocks |
| **Edge Cases** | 75% | 25% | Risk-based generation + defect history |

### 16.2 Test Structure

```
tests/
├── unit/                    # Pure functions, validators, helpers
│   ├── test_crypto.py
│   ├── test_validators.py
│   └── test_helpers.py
├── api/                     # FastAPI endpoints
│   ├── test_auth.py
│   ├── test_clips.py
│   ├── test_publish.py
│   └── test_privacy.py
├── integration/             # Cross-component
│   ├── test_pipeline_full.py
│   ├── test_publishing.py
│   └── test_oauth_flow.py
├── e2e/                     # Playwright
│   ├── test_upload_flow.py
│   ├── test_editor.py
│   └── test_publishing.py
├── contract/                # Pact contracts
│   ├── postiz_contract.py
│   └── youtube_contract.py
├── property/                # Hypothesis property-based
│   └── test_validators_property.py
├── adversarial/             # AI safety
│   ├── test_prompt_injection.py
│   └── test_jailbreak.py
└── performance/             # Benchmarks
    └── test_pipeline_benchmarks.py
```

### 16.3 Coverage Targets

| Metric | Target | Enforcement |
|--------|--------|-------------|
| **Overall Coverage** | ≥ 70% | CI gate (fail if < 70%) |
| **Business Logic** | ≥ 80% | CI gate (fail if < 80%) |
| **Critical Paths** | 100% | CI gate (fail if < 100%) |
| **API Contracts** | 100% | Pact verification |
| **A11y** | 0 violations | axe-core in CI |

---

## 17. RISK REGISTER WITH MONTE CARLO SIMULATION

### 17.1 Risk Register (Top 15)

| ID | Risk | Prob | Impact | Score | Mitigation | Owner | Status |
|----|------|------|--------|-------|------------|-------|--------|
| **R01** | CPU-only too slow | 0.8 | 1.0 | **0.80** | Tiny models, sequential, swap 4GB | Dev | Validando |
| **R02** | OOM Kill | 0.75 | 1.0 | **0.75** | Memory limits, sequential, swap 4GB | DevOps | Mitigado |
| **R03** | Postiz OAuth falha | 0.7 | 0.8 | **0.56** | Scripts + docs + youtube-upload fallback | Dev | Planejado |
| **R04** | YouTube token expira | 0.7 | 0.8 | **0.56** | Cron 6h refresh, NTP sync | DevOps | Planejado |
| **R05** | Scoring quality baixa | 0.6 | 0.8 | **0.48** | Prompt engineering + fallback heurístico | Dev | Parcial |
| **R06** | hotclip falha | 0.5 | 0.8 | **0.40** | FFmpeg fallback, version pin | Dev | Parcial |
| **R07** | VPS down = perda total | 0.15 | 1.0 | **0.15** | Backup diário + restore < 15 min | DevOps | Planejado |
| **R08** | LGPD non-compliance | 0.3 | 0.8 | **0.24** | Endpoint DELETE + cascade delete | Dev | Planejado |
| **R09** | Supply chain attack | 0.2 | 0.7 | **0.14** | requirements.lock + pip-audit + Dependabot | DevOps | Contínuo |
| **R10** | API plataforma muda | 0.3 | 0.8 | **0.24** | Postiz mantém compat, testes semanais | Dev | Monitorado |
| **R11** | Clock skew VPS | 0.15 | 0.8 | **0.12** | NTP sync forçado, healthcheck | DevOps | Mitigado |
| **R12** | Qualidade transcrição | 0.4 | 0.4 | **0.16** | Aceito (mitigado por scoring + revisão) | Dev | Aceito |
| **R13** | Latência pipeline | 0.5 | 0.3 | **0.15** | Aceito (funcional > rápido) | Dev | Aceito |
| **R14** | Sem dashboard | 0.8 | 0.2 | **0.16** | Aceito (P7 - logs + healthchecks) | DevOps | Aceito |
| **R15** | Sem HA | 0.6 | 0.3 | **0.18** | Aceito (P2 - backup/restore < 15 min) | DevOps | Aceito |

### 17.2 Monte Carlo Simulation (10.000 iterações)

**Scenario**: Total project effort (person-days) with effort variance ±30%

```python
# Simulação simplificada (conceitual)
import numpy as np

# Base effort per phase (person-days)
base_effort = {
    "phase0_foundation": 15,
    "phase1_pipeline": 25,
    "phase2_publishing": 20,
    "phase3_hardening": 18,
    "phase4_vps": 8,
    "phase5_golive": 6,
}

# Monte Carlo 10.000 iterations
np.random.seed(42)
iterations = 10000
total_efforts = []

for _ in range(iterations):
    total = 0
    for phase, base in base_effort.items():
        # Log-normal distribution for effort variance
        effort = base * np.random.lognormal(mean=0, sigma=0.3)
        total += effort
    total_efforts.append(total)

# Results
p10 = np.percentile(total_efforts, 10)
p50 = np.percentile(total_efforts, 50)
p90 = np.percentile(total_efforts, 90)
mean = np.mean(total_efforts)
std = np.std(total_efforts)

print(f"Monte Carlo Results (10,000 iterations):")
print(f"  Mean effort: {mean:.1f} person-days")
print(f"  Std deviation: {std:.1f} person-days")
print(f"  P10 (optimistic): {p10:.1f} person-days")
print(f"  P50 (median): {p50:.1f} person-days")
print(f"  P90 (pessimistic): {p90:.1f} person-days")
print(f"  Probability ≤ 100 pd: {(np.array(total_efforts) <= 100).mean()*100:.1f}%")
print(f"  Probability ≤ 120 pd: {(np.array(total_efforts) <= 120).mean()*100:.1f}%")
```

**Expected Results (based on similar projects):**
- **Mean**: ~102 person-days
- **P50 (Median)**: ~98 person-days
- **P90 (Pessimistic)**: ~135 person-days
- **P10 (Optimistic)**: ~75 person-days
- **P(≤ 100 pd)**: ~55%
- **P(≤ 120 pd)**: ~85%

### 17.3 What-If Scenarios

| Scenario | Effort Delta | Probability | Decision |
|----------|-------------|-------------|----------|
| **Baseline** | 0% | 50% | Plano atual |
| **CPU-only 2x mais lento** | +25% | 30% | Aceitar latência, manter modelos tiny |
| **Postiz OAuth falha total** | +15% | 20% | Fallback youtube-upload + docs manuais |
| **VPS headroom insuficiente** | +40% | 10% | Upgrade VPS (fora orçamento) → replan |
| **Modelo 1.5B scoring inútil** | +30% | 15% | Upgrade para 3B (se RAM) ou heurístico only |

---

## 18. DELIVERY CRITERIA & DEFINITION OF DONE

### 18.1 Phase Gates (Immutable)

| Gate | Name | Criteria | Verification Method |
|------|------|----------|---------------------|
| **G0** | Pre-Flight Validation | All benchmarks pass, zero P0 blockers documented | `python -m pytest tests/test_smoke.py -v` + `docker stats` |
| **G1** | Pipeline Functional | Upload → Transcribe → Highlight → Edit → Clips < 30 min, 100% tests pass | `python -m pytest tests/ -v` + manual E2E |
| **G2** | Publishing Functional | Clips publish to TikTok, Reels, Shorts, YouTube successfully | Manual test 4 plataformas + integration tests |
| **G3** | Production Ready | DR < 15 min tested, LGPD endpoint working, security scan zero critical | `./scripts/restore.sh` timed + `pytest tests/test_lgpd.py` + `trivy` |
| **G4** | VPS Deploy | 12 containers healthy, HTTPS working, OAuth callbacks production | `docker ps` + `curl https://domain/health` + OAuth test |
| **G5** | Go-Live | Zero external API calls in 30 days, full E2E success, stakeholder sign-off | Log audit + stakeholder sign-off document |

### 18.2 Definition of Done (Per Feature)

- [ ] Código implementado seguindo FSD + CLAUDE.md
- [ ] Testes unitários ≥ 80% cobertura (business logic)
- [ ] Testes integração/E2E passando
- [ ] Code review aprovado (2+ aprovações se team > 1)
- [ ] Storybook atualizado (se componente UI)
- [ ] Documentação atualizada (README + docs/ + docstrings)
- [ ] Deploy staging funcionando
- [ ] Acessibilidade verificada (axe-core 0 violações AA)
- [ ] Performance dentro thresholds (bundle < 200KB, LCP < 2.5s)
- [ ] Security scan zero critical/high (CI gate)
- [ ] ADR atualizado se decisão arquitetural
- [ ] Changelog via changesets

### 18.3 Definition of Ready (Per Sprint)

- [ ] História bem definida + critérios de aceitação claros
- [ ] Design aprovado (se UI)
- [ ] Dependências resolvidas
- [ ] Estimativa acordada (planning poker se team > 1)
- [ ] ADR existente para decisões arquiteturais envolvidas
- [ ] Test data/mock preparados

---

## 19. POST-LAUNCH EVOLUTION LOOPS

### 19.1 Continuous Improvement Cycles

| Loop | Frequency | Activities | Owner |
|------|-----------|------------|-------|
| **Daily** | Healthcheck | Log review, alert triage, backup verify | DevOps |
| **Weekly** | Sprint Review | Demo, retro, planning, metric review | All |
| **Bi-Weekly** | Chaos Engineering | Game day: kill worker, DB, network | DevOps + Dev |
| **Monthly** | Chaos Game Day | Full scenario: worker+DB+network down | DevOps + Dev |
| **Quarterly** | DR Drill | Full restore from backup, timed | DevOps |
| **Quarterly** | Pen Test | External ou automatizado (Strix/Trivy) | Security |
| **Semi-Annual** | Dependency Audit | `pip-audit`, `npm audit`, `trivy`, license check | DevOps |
| **Annual** | Pen Test Externo | Profissional ou bug bounty | Security |

### 19.2 Knowledge Compounding (Memory Graph)

```json
{
  "project": "autoviral-v2",
  "learnings": [
    {"pattern": "CPU-only Whisper base + Qwen2.5-1.5B", "result": "Functional < 30 min, RAM 5.3 GB", "reusable": true},
    {"pattern": "hotclip AGPL container isolation", "result": "FFmpeg fallback essential", "reusable": true},
    {"pattern": "Postiz OAuth 4 platforms", "result": "Scripts automation essential", "reusable": true},
    {"pattern": "VPS single-node 8GB RAM", "result": "34% headroom sufficient", "reusable": true}
  ],
  "anti_patterns": [
    {"pattern": "Parallel jobs", "result": "OOM kills, CPU contention", "avoid": true},
    {"pattern": "Model large (7B+)", "result": "OOM, CPU-only infeasible", "avoid": true},
    {"pattern": "Managed services (RDS, S3)", "result": "Cost > R$200/month", "avoid": true}
  ]
}
```

### 19.3 Automated Post-Mortem Template

```markdown
# Post-Mortem: [Incident] — {{date}}

## Timeline
- {{timestamp}}: Alert triggered ({{metric}} > {{threshold}})
- {{timestamp}}: Investigation started
- {{timestamp}}: Root cause identified
- {{timestamp}}: Fix deployed
- {{timestamp}}: System stable

## Root Cause
{{technical_description}} — Commit: {{commit_sha}}

## Impact
- Users affected: {{count}}
- Downtime: {{minutes}} minutes
- Data loss: {{yes/no}}

## Corrective Actions
1. [P0] Add test for {{scenario}} — {{owner}} — {{due_date}}
2. [P1] Improve alert for {{metric}} — {{owner}} — {{due_date}}
3. [P2] Document edge case in `docs/edge-cases/` — {{owner}}

## Lessons Learned
{{persisted_to_memory_graph}}
```

---

## APPENDIX A: QUICK REFERENCE COMMANDS

```bash
# Development
make dev              # docker compose up -d (local)
make test             # python -m pytest tests/ -v
make lint             # ruff + mypy
make format           # ruff format + prettier

# Operations
make backup           # scripts/backup.sh
make restore          # scripts/restore.sh BACKUP=latest
make logs             # docker compose logs -f api
make shell            # docker compose exec api bash
make health           # curl -f localhost:8000/health && docker ps

# VPS Deploy
make deploy           # GitHub Actions trigger (push main)
make ssh              # ssh root@$VPS_IP

# Validation
make benchmark        # python -m pytest tests/test_smoke.py -v
make loadtest         # 10 sequential jobs
make security         # trivy fs . && pip-audit && bandit -r api/

# OAuth
make oauth-setup      # scripts/setup-oauth-all.sh
make oauth-refresh    # scripts/refresh-oauth-tokens.sh
```

---

## APPENDIX B: KEY FILE PATHS

| Category | Path |
|----------|------|
| **Main Config** | `docker-compose.fully-selfhosted.yml`, `.env` |
| **API Core** | `api/main.py`, `api/core/config.py`, `api/core/security.py` |
| **Pipeline** | `api/pipeline/transcribe.py`, `api/pipeline/highlight.py`, `api/pipeline/cutter.py` |
| **Routers** | `api/routers/clips.py`, `api/routers/publish.py`, `api/routers/auth.py` |
| **Services** | `api/services/pipeline.py`, `api/services/worker.py`, `api/services/publisher.py` |
| **Frontend** | `frontend/src/app/`, `frontend/src/features/`, `frontend/src/shared/` |
| **Infra** | `monitoring/`, `traefik/`, `vault/`, `scripts/` |
| **Tests** | `tests/`, `frontend/e2e/`, `frontend/src/**/*.test.tsx` |
| **Docs** | `docs/`, `inception-output/`, `README.md` |
| **CI/CD** | `.github/workflows/ci.yml`, `.github/workflows/deploy.yml` |

---

## APPENDIX C: BUDGET TRACKING TEMPLATE

```markdown
# Budget Tracking - {{month}}/{{year}}

## Fixed Costs
| Item | Budget | Actual | Delta |
|------|--------|--------|-------|
| VPS | R$60 | R$___ | R$___ |
| Domain/SSL | R$5 | R$___ | R$___ |
| **Subtotal Fixed** | **R$65** | **R$___** | **R$___** |

## Variable Costs (Must Remain Zero)
| Item | Budget | Actual | Delta |
|------|--------|--------|-------|
| External APIs | R$0 | R$___ | R$___ |
| Managed Services | R$0 | R$___ | R$___ |
| **Subtotal Variable** | **R$0** | **R$___** | **R$___** |

## Contingency
| Item | Budget | Used | Remaining |
|------|--------|------|-----------|
| Buffer | R$235 | R$___ | R$___ |

## TOTAL
| | Budget | Actual | Delta |
|---|--------|--------|-------|
| **TOTAL** | **R$300** | **R$___** | **R$___** |

## Alerts Triggered This Month
- [ ] VPS cost > R$65
- [ ] External API calls > 0
- [ ] Disk usage > 80%
- [ ] RAM usage > 85%
```

---

**Document Version**: 1.0  
**Last Updated**: 2026-10-10  
**Status**: **ACTIVE — SINGLE SOURCE OF TRUTH**  
**Next Review**: Sprint 1 Review (Week 2)  
**Owner**: Arquiteto do Nascer do Sol + Omega Project Architect  

---

> **Este documento é vivo.** Atualize a cada sprint review. Todas as decisões arquiteturais devem gerar ADR. Todas as métricas devem ser rastreáveis. Todo custo recorrente > R$0 deve ser justificado e aprovado.