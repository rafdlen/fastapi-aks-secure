from fastapi import Request, HTTPException
from jose import jwt
import httpx

class JWKSCache:
    _jwks = None
    _jwks_uri = None

cache = JWKSCache()

async def validate_jwt(request: Request, tenant_id: str, audience: str):
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = auth.split()[1]
    # Fetch OpenID config and JWKS (cache for simplicity)
    if not cache._jwks:
        oidc = f"https://login.microsoftonline.com/{tenant_id}/v2.0/.well-known/openid-configuration"
        async with httpx.AsyncClient(timeout=5) as c:
            oidc_doc = (await c.get(oidc)).json()
            cache._jwks_uri = oidc_doc["jwks_uri"]
            cache._jwks = (await c.get(cache._jwks_uri)).json()

    try:
        claims = jwt.decode(
            token,
            cache._jwks,
            algorithms=["RS256"],
            audience=audience,
            options={"verify_at_hash": False}
        )
        return claims
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token validation failed: {e}")
