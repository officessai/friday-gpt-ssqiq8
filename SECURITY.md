# Security Policy

## Supported Versions

Only the latest version of the `main` branch receives security updates.

## Reporting a Vulnerability

If you discover a security issue, report it privately using GitHub Security Advisories:

https://github.com/officessai/friday-gpt-ssqiq8/security/advisories

Do not open public issues for vulnerabilities, leaked credentials, API keys, tokens or potential security incidents.

## Handling Secrets

- Never commit `.env`, API keys, tokens, service account files or credentials.
- Do not use `VITE_*` variables for secrets. Anything prefixed with `VITE_` is exposed to the browser bundle.
- Gemini/OpenAI/Anthropic/xAI/API keys must remain server-side only.
- Use `.env.example` only as a placeholder reference.
- Real secrets belong in local `.env`, GitHub Encrypted Secrets or a provider secret manager.

## Public Repository Notice

This is a public repository. Treat all commits, pull requests and issues as visible to the internet.
