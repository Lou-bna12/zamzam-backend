from fastapi import APIRouter, Depends
from app.core.auth_utils import role_required

router = APIRouter(prefix="/client", tags=["Client"])

@router.get("/dashboard")
def client_dashboard(payload: dict = Depends(role_required("client"))):
    return {
        "message": "Bienvenue dans le dashboard client",
        "user": payload
    }
