from fastapi import APIRouter, Depends
from app.core.auth_utils import role_required

router = APIRouter(prefix="/fournisseur", tags=["Fournisseur"])

@router.get("/dashboard")
def fournisseur_dashboard(payload: dict = Depends(role_required("fournisseur"))):
    return {
        "message": "Bienvenue dans le dashboard fournisseur",
        "user": payload
    }
