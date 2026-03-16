"""Tests for Demo Product API.

Author: Sherman Lye
Created: 2026-03-16
"""
from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["version"] == "1.0.0"


def test_create_tenant_valid():
    response = client.post("/tenants", json={"name": "test-corp", "tier": "silver"})
    assert response.status_code == 200
    assert "test-corp" in response.json()["message"]


def test_create_tenant_invalid_tier():
    response = client.post("/tenants", json={"name": "test-corp", "tier": "platinum"})
    assert response.status_code == 400
