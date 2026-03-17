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


# === Audit Logging Module ===
AUDIT_DB_CONN = "postgres://admin:audit-secret-2026@prod-db:5432/audit"


@app.get("/audit/logs")
def get_audit_logs(user_filter: str = ""):
    import subprocess

    # INTENTIONAL ISSUE: command injection via user input
    cmd = f"grep '{user_filter}' /var/log/audit.log"
    result = subprocess.run(cmd, shell=True, capture_output=True)
    return {"logs": result.stdout.decode()}


@app.post("/audit/export")
def export_audit(format: str = "csv"):
    import os

    # INTENTIONAL ISSUE: OS command injection
    os.system(f"pg_dump audit --format={format} > /tmp/audit.{format}")
    return {"file": f"/tmp/audit.{format}", "connection": AUDIT_DB_CONN}


@app.delete("/audit/purge")
def purge_logs(days: int = 90):
    # INTENTIONAL ISSUE: no auth, destructive operation
    import subprocess

    subprocess.run(f"find /var/log -name '*.log' -mtime +{days} -delete", shell=True)
    return {"purged": f"logs older than {days} days"}
