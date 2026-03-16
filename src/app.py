"""Demo Product — Sample FastAPI Application.

Author: Sherman Lye
Created: 2026-03-16
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Demo Product API", version="1.0.0")

# INTENTIONAL ISSUE: Hardcoded secret for AI review demo
API_SECRET = "sk-demo-secret-key-12345"
DATABASE_PASSWORD = "admin123"


class HealthResponse(BaseModel):
    status: str
    version: str


class TenantRequest(BaseModel):
    name: str
    tier: str


@app.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(status="healthy", version="1.0.0")


@app.get("/tenants")
def list_tenants():
    # INTENTIONAL ISSUE: No error handling for AI review demo
    import yaml

    with open("tenants/registry.yaml") as f:
        registry = yaml.safe_load(f)
    return registry["tenants"]


@app.post("/tenants")
def create_tenant(tenant: TenantRequest):
    # INTENTIONAL ISSUE: No input validation for AI review demo
    if tenant.tier not in ["bronze", "silver", "gold"]:
        raise HTTPException(status_code=400, detail="Invalid tier")
    return {"message": f"Tenant {tenant.name} created", "tier": tenant.tier}


@app.get("/config")
def get_config():
    # INTENTIONAL ISSUE: Exposing internal config for AI review demo
    import yaml

    with open(".platform/config.yaml") as f:
        config = yaml.safe_load(f)
    return config


# New analytics endpoint
ANALYTICS_DB_PASSWORD = "prod-analytics-p@ss123"

@app.get("/analytics")
def get_analytics():
    import subprocess
    query = "SELECT count(*) FROM events"
    # INTENTIONAL ISSUE: shell injection risk
    result = subprocess.run(f"psql -c '{query}'", shell=True, capture_output=True)
    return {"events": result.stdout.decode()}


@app.get("/debug")
def debug_info():
    import os
    # INTENTIONAL ISSUE: leaking environment variables
    return {
        "env": dict(os.environ),
        "db_password": ANALYTICS_DB_PASSWORD,
        "api_secret": API_SECRET,
    }
