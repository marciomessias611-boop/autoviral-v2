# AutoViral v2 — comandos de segurança, teste, deploy e editor.
.PHONY: install test secure up down logs ps verify vault-init editor build-n8n lint

install:
	pip install -r requirements.txt

# Rodar a suíte de testes (smoke, schedulers, youtube publisher).
test:
	python -m pytest tests/ -v

# Scanners do CI localmente (SAAST + SCA). Instala sob demanda.
saast:
	pip install semgrep >/dev/null 2>&1 || true
	semgrep --config=auto api integrations tests || true

sca:
	pip install pip-audit >/dev/null 2>&1 || true
	pip-audit -r requirements.txt || true

secure: saast sca

# Deploy via docker compose (ordenado com health gates via scripts/start.sh).
up:
	bash scripts/start.sh up

down:
	bash scripts/start.sh down

logs:
	bash scripts/start.sh logs $(S)

ps:
	bash scripts/start.sh ps

# Verifica conexões dos serviços após o up.
verify:
	python scripts/verify_connections.py

# Semeia segredos no Vault (rodar 1x após subir vault).
vault-init:
	python scripts/init_vault.py

# Instala o motor de edição de alta qualidade (hotclip, CLI headless).
# Requer Node >= 18 + pnpm.
editor:
	cd desktop/hotclip && corepack enable pnpm && pnpm install --no-audit --no-fund

# Compila os custom nodes do n8n (TypeScript -> dist).
build-n8n:
	cd n8n/custom-nodes/hotclip && npm install --no-audit --no-fund && npm run build

# Checagem de imports Python (sem executar).
lint:
	python -m compileall -q api integrations tests