import os
from fastapi import FastAPI, Request, Depends
from auth import validate_jwt

TENANT = os.environ.get("TENANT", "")
AUD = os.environ.get("AUD", "")

app = FastAPI(title="fastapi-aks-secure")

async def auth_dep(request: Request):
    if not TENANT or not AUD:
        # In prod, these should always be set via env/KeyVault CSI
        raise Exception("TENANT/AUD not configured")
    return await validate_jwt(request, TENANT, AUD)

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/whoami")
async def whoami(claims=Depends(auth_dep)):
    return {
        "name": claims.get("name"),
        "oid": claims.get("oid"),
        "preferred_username": claims.get("preferred_username"),
        "roles": claims.get("roles", [])
    }
