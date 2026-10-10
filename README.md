# AutoViral v2 — clipes + publicação multi-conta/multi-plataforma

Reescrita "zero + best-of": une o melhor do `autoclip` (pipeline de highlights via LLM),
do `clip-forge`/`hotclip` (edição 9:16 estilo Opus Clip) e do `postiz`/`zernio`
(agendamento/publicação multi-conta), sob uma API FastAPI segura.

## Estrutura

```
api/            FastAPI (JWT+RBAC, SSRF-safe, CORS whitelist)
  routers/      clips · publish · youtube_dl · analyze · auth · metrics
  pipeline/     transcribe (whisper) · highlight (LLM scoring) · thumbnail
  functions/    ab_testing · smart_hashtags · competitor · copyright · thumbnail
  security.py   senhas, JWT, e validação SSRF de URLs
  config.py     pydantic-settings (nada hardcoded)
integrations/
  scheduler_postiz/   cliente REST do Postiz
  scheduler_zernio/   wrapper do CLI Zernio
  latewiz/            scheduler OSS do Zernio (referência)
desktop/        motores de edição clonados (clip-forge, hotclip)
n8n/            workflow clip → edit → schedule (+ node Postiz)
infra/          docker-compose (traefik HTTP edge, minio, redis) + Dockerfile
```

## Arquitetura do fluxo

```
URL (YouTube/Bilibili) ──SSRF-safe──▶ yt-dlp ──▶ api/pipeline: transcribe
   ─▶ highlight scoring (LLM) ─▶ export 9:16 (hotclip CLI) ─▶ /clips
   ─▶ /publish ─▶ Postiz (REST) OU Zernio (CLI) ─▶ agendado/multi-conta
```

## Rodando

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
export AUTOVIRAL_JWT_SECRET=$(openssl rand -hex 32)
uvicorn api.main:app --port 8000
```

Primeiro login: `admin@local` (senha seed é logada no arranque — troque em `/auth/rotate-password`).

## Decisões de segurança (obrigatórias aqui)

- **Sem CORS `*`** — whitelist via `FRONTEND_ORIGIN`.
- **Auth em toda rota sensível** — do autoclip ficou o pipeline; corrigimos o "zero auth".
- **SSRF-safe** em downloads e media URLs — só `http/https`, host público, allowlist
  `youtube.com | bilibili.com | vimeo.com` (localhost/loopback/privado/reservado são rejeitados).
- **Secrets via env/vault** — nunca hardcoded (a chave de LLM do autoclip que vazava em
  `llm_providers.py:115` não existe aqui; logs não incluem chaves).

## Metricool — sim ou não?

**Não é a melhor escolha** para multi-conta/desktop: free é 1 perfil + 20 posts/mês;
pago começa em ~R$100 (5 perfis). Para "editar e publicar em várias contas", o par
**clip-forge/hotclip (edição) + Postiz/Zernio (publicação)** cobre o mesmo papel,
auto-hospedado e sem teto de perfis. Metricool só se justifica se você precisar do
analytics de concorrente que ele tem pronto.