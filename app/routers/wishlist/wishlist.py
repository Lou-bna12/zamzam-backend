from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.database.session import get_db
from app.models.wishlist import WishlistItem
from app.models.product import Product

router = APIRouter(prefix="/wishlist", tags=["Wishlist"])


# 1️⃣ Voir les favoris
@router.get("/")
def get_wishlist(db: Session = Depends(get_db), user=Depends(get_current_user)):
    items = db.query(WishlistItem).filter(WishlistItem.user_id == user.id).all()
    return items


# 2️⃣ Ajouter un produit aux favoris
@router.post("/add/{product_id}")
def add_to_wishlist(product_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):

    # Vérifier existence produit
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(404, "Produit introuvable")

    # Vérifier s'il est déjà dans les favoris
    exist = db.query(WishlistItem).filter(
        WishlistItem.user_id == user.id,
        WishlistItem.product_id == product_id
    ).first()

    if exist:
        return {"detail": "Déjà dans les favoris"}

    new_item = WishlistItem(user_id=user.id, product_id=product_id)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return {"detail": "Ajouté aux favoris"}


# 3️⃣ Supprimer un favori
@router.delete("/remove/{product_id}")
def remove_from_wishlist(product_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):

    item = db.query(WishlistItem).filter(
        WishlistItem.user_id == user.id,
        WishlistItem.product_id == product_id
    ).first()

    if not item:
        raise HTTPException(404, "Ce produit n'est pas dans vos favoris")

    db.delete(item)
    db.commit()

    return {"detail": "Supprimé des favoris"}
