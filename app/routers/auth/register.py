from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.user import UserCreate
from app.models.user import User
from app.core.security import hash_password

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):

    # ⚠ Vérifier email déjà utilisé
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # 🔐 Hacher password
    hashed_pwd = hash_password(user_data.password)

    # 👤 Créer l'utilisateur
    new_user = User(
        email=user_data.email,
        password=hashed_pwd,
        name=user_data.name,
        phone=user_data.phone,
        role=user_data.role,            # admin / client / fournisseur
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "email": new_user.email,
        "name": new_user.name,
        "role": new_user.role,
        "phone": new_user.phone,
        "is_active": new_user.is_active
    }
