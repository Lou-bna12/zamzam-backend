from fastapi import APIRouter, Depends
from app.core.auth_utils import role_required

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/dashboard")
def admin_dashboard(payload = Depends(role_required("admin"))):
    return {
        "message": "Bienvenue dans le dashboard admin",
        "user": payload
    }
