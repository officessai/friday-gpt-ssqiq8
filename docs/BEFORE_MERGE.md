# Before Merge Checklist

Use this checklist before merging any pull request that changes code, configuration, deployment, security-sensitive files or integration logic.

## Security

- [ ] `.env` and `.env.*` are not committed.
- [ ] No API key, token, credential or service account file appears in the diff.
- [ ] No secrets are exposed through `VITE_*` variables.
- [ ] Frontend code does not call APIs requiring private keys directly.
- [ ] `.env.example` contains placeholders only.
- [ ] `.gitignore` includes environment files, credentials, local databases and key files.
- [ ] `SECURITY.md` exists and is current.
- [ ] README contains a Security section.

## Scope Control

- [ ] The PR changes only the files required for its stated purpose.
- [ ] No unrelated formatting, refactors or generated files are included.
- [ ] Public files do not expose private project IDs, service account emails, tokens, screenshots or operational details.

## Review

- [ ] The PR title clearly describes the change.
- [ ] The PR description includes Summary, Scope and Testing sections.
- [ ] At least one final owner check is completed before merge.

## Testing

- [ ] Config/docs-only changes explain why runtime tests are not required.
- [ ] Code changes include the relevant checks or manual testing notes.
