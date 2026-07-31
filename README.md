# OfficeSSAI + Friday

Pierwsza wdrażalna wersja strony OfficeSSAI: frontend React/Vite, backend FastAPI, formularz kontaktowy z trwałym zapisem leadów oraz asystent Friday korzystający z OpenAI Responses API albo Azure OpenAI.

## Co jest gotowe

- responsywna strona sprzedażowa w języku polskim,
- demo Friday pod `/api/v1/chat`,
- przełączanie dostawcy `demo | openai | azure` przez zmienne środowiskowe,
- formularz kontaktowy zapisujący każde zgłoszenie do SQLite,
- opcjonalne powiadomienie SMTP na `s.szarpak@officessai.com`,
- Docker Compose dla frontendu i API,
- testy backendu oraz CI dla frontendu i API,
- klucze pozostają wyłącznie po stronie serwera.

## Szybki start

```bash
cp .env.example .env
docker compose up --build
```

Strona: `http://localhost:8080`  
API: `http://localhost:8080/api/v1/health`

## Lokalny development

Frontend:

```bash
npm install
npm run dev
```

Backend:

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src uvicorn friday_app.main:app --reload
```

Vite przekazuje lokalne zapytania `/api` do `http://localhost:8000`.

## Konfiguracja AI

### OpenAI

```env
AI_PROVIDER=openai
AI_MODEL=gpt-5-mini
OPENAI_API_KEY=...
```

### Azure OpenAI / Microsoft Foundry

```env
AI_PROVIDER=azure
AI_MODEL=NAZWA_WDROZENIA_MODELU
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_BASE_URL=https://NAZWA-ZASOBU.openai.azure.com/openai/v1/
```

Na produkcji przechowuj sekrety w Azure Key Vault, AWS Secrets Manager albo w sekretach platformy wdrożeniowej. Nigdy nie dodawaj pliku `.env` ani kluczy do repozytorium.

## Formularz kontaktowy

Każde poprawne zgłoszenie jest najpierw zapisywane w `data/leads.sqlite3`. Po uzupełnieniu ustawień `SMTP_*` API wysyła również powiadomienie e-mail. Katalog `data` należy objąć kopią zapasową i ograniczyć do administratora.

## Testy

```bash
PYTHONPATH=src pytest -q
npm run lint
npm run build
```

## Wdrożenie

Obrazy `Dockerfile.web` i `Dockerfile.api` można wdrożyć między innymi do Azure Container Apps, Azure App Service, AWS App Runner albo zwykłego serwera z Dockerem. `docker-compose.yml` uruchamia cały zestaw lokalnie i na pojedynczym VPS.

## Security

Repozytorium jest publiczne. Nie commituj kluczy API, tokenów, plików kont usługowych ani `.env`. Frontend wywołuje wyłącznie własne endpointy `/api`; sekrety są odczytywane przez backend z bezpiecznego środowiska. Zgłoszenia bezpieczeństwa wysyłaj prywatnie przez GitHub Security Advisories.
