# Friday API

Friday is now organized as a deployable, testable FastAPI service with clearer boundaries between API routes, schemas, business logic, and runtime configuration.

## Project structure

```
.
├── src/friday_app
│   ├── api
│   │   ├── routes
│   │   │   ├── chat.py
│   │   │   └── health.py
│   │   └── router.py
│   ├── core
│   │   └── settings.py
│   ├── schemas
│   │   └── chat.py
│   ├── services
│   │   └── chat_service.py
│   ├── app.py
│   └── main.py
├── tests
├── Dockerfile
├── .github/workflows/ci.yml
└── requirements.txt
```

## Quick start

1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure environment variables:
   ```bash
   cp .env.example .env
   ```
4. Run locally:
   ```bash
   PYTHONPATH=src uvicorn friday_app.main:app --reload
   ```

## Deployment

Build and run with Docker:

```bash
docker build -t friday-api .
docker run --rm -p 8000:8000 --env-file .env friday-api
```

## Endpoints

- `GET /api/v1/health`
- `POST /api/v1/chat`
