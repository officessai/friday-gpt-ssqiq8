# Friday

Friday is now organized as a deployable web app with a clearer, scalable structure.

## Project structure

```text
.
├── apps/
│   └── web/                  # React + TypeScript app
│       ├── src/
│       │   ├── components/   # UI components split by responsibility
│       │   ├── App.tsx
│       │   └── main.tsx
│       └── package.json
├── .github/workflows/ci.yml  # Lint + build checks
├── Dockerfile                # Production image (nginx)
├── docker-compose.yml        # Local deployment wrapper
└── package.json              # Workspace scripts
```

## Quick start

```bash
npm install
npm run dev
```

## Build for production

```bash
npm run build
```

## Deploy with Docker

```bash
docker compose up --build
```

The app will be available at `http://localhost:8080`.
