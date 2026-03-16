# Demo Product

Sample product demonstrating the [AI-Powered CI/CD Platform](https://github.com/shermanlye-ideagen/demo-cicd-platform).

## Features

- FastAPI application with tenant management
- Multi-tenant architecture (bronze/silver/gold tiers)
- Platform-managed CI/CD via reusable GitHub Actions
- AI code review on every PR via Claude

## Architecture

| Property | Value |
|----------|-------|
| Stack | Python (FastAPI) |
| Tier | Silver |
| Deploy Target | EKS (auto-detected) |
| Tenancy | Multi-tenant |

## Local Development

```bash
pip install -r src/requirements.txt
uvicorn src.app:app --reload
```

## CI/CD

This repo uses the AI-Powered CI/CD Platform:

- **PRs** trigger AI code review via Claude
- **Tags** trigger AI-enhanced releases (release notes + JIRA + Confluence)
- **Self-service PRs** are validated against platform policies

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/tenants` | GET | List all tenants |
| `/tenants` | POST | Create a new tenant |
| `/config` | GET | Get product config |
