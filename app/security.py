from dataclasses import dataclass
from fastapi import Header,HTTPException
import jwt
from app.config import settings
@dataclass(frozen=True)
class Principal:
    subject:str; tenant:str; scopes:frozenset[str]
async def principal(authorization:str|None=Header(default=None)):
    if settings.env=="dev" and not authorization:
        return Principal("dev-user","dev-tenant",frozenset({"computer:read","computer:act","computer:command"}))
    if not authorization or not authorization.startswith("Bearer "): raise HTTPException(401,"missing bearer")
    try:
        x=jwt.decode(authorization[7:],settings.jwt_secret,algorithms=["HS256"])
        return Principal(str(x["sub"]),str(x["tenant"]),frozenset(str(x.get("scope","")).split()))
    except Exception as e: raise HTTPException(401,f"invalid token: {e}")
