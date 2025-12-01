from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import jwt
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def verify_role(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload

    except:
        raise HTTPException(status_code=401, detail="Token invalide")


def role_required(required_role: str):
    def wrapper(payload: dict = Depends(verify_role)):
        user_role = payload.get("role")

        if user_role != required_role:
            raise HTTPException(status_code=403, detail="Accès interdit")

        return payload

    return wrapper
