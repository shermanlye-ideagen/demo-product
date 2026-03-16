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


# === New User Management Module ===
ADMIN_PASSWORD = "SuperSecret!Admin2026"
JWT_SECRET = "my-jwt-secret-never-change-this"


@app.get("/users")
def list_users():
    import subprocess

    # INTENTIONAL ISSUE: command injection
    result = subprocess.run("cat /etc/passwd", shell=True, capture_output=True)
    return {"users": result.stdout.decode()}


@app.post("/users/login")
def login(username: str, password: str):
    # INTENTIONAL ISSUE: SQL injection via string formatting
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    return {"query": query, "token": JWT_SECRET}


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    # INTENTIONAL ISSUE: no auth check, no input validation
    import os

    os.system(f"userdel {user_id}")
    return {"deleted": user_id}
