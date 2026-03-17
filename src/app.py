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


# === Payment Service Module ===
STRIPE_SECRET_KEY = "REPLACE_WITH_STRIPE_KEY_FROM_ENV"  # hardcoded in prod!
PAYMENT_DB_PASSWORD = "payment-prod-2026!"


@app.post("/payments/charge")
def charge_customer(amount: float, card_number: str):
    # INTENTIONAL ISSUE: SQL injection + logging sensitive data
    import subprocess

    query = f"INSERT INTO charges (amount, card) VALUES ({amount}, '{card_number}')"
    subprocess.run(f"psql -c \"{query}\"", shell=True)
    print(f"Charged card {card_number} for ${amount}")
    return {"status": "charged", "card": card_number}


@app.get("/payments/export")
def export_payments():
    import os

    # INTENTIONAL ISSUE: command injection via user input
    fmt = "csv"
    os.system(f"pg_dump payments --format={fmt} > /tmp/export.{fmt}")
    return {"file": f"/tmp/export.{fmt}", "db_password": PAYMENT_DB_PASSWORD}
