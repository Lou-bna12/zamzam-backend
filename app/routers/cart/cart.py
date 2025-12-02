from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.database.session import get_db
from app.models.cart import CartItem
from app.models.product import Product

router = APIRouter(prefix="/cart", tags=["Cart"])


# 🛒 1 — Voir le panier
@router.get("/")
def get_cart(db: Session = Depends(get_db), user=Depends(get_current_user)):
    items = db.query(CartItem).filter(CartItem.user_id == user.id).all()
    return items


# 🛒 2 — Ajouter un produit au panier
@router.post("/add/{product_id}")
def add_to_cart(product_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):

    # vérifier existence produit
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(404, "Produit introuvable")

    # vérifier si déjà dans le panier
    item = (
        db.query(CartItem)
        .filter(CartItem.user_id == user.id, CartItem.product_id == product_id)
        .first()
    )

    if item:
        item.quantity += 1
        db.commit()
        return {"detail": "Quantité mise à jour"}

    new_item = CartItem(
        user_id=user.id,
        product_id=product_id,
        quantity=1
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return {"detail": "Produit ajouté au panier"}


# 🛒 3 — Modifier quantité
@router.put("/update/{item_id}")
def update_cart_item(item_id: int, quantity: int, db: Session = Depends(get_db), user=Depends(get_current_user)):

    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.user_id == user.id).first()
    if not item:
        raise HTTPException(404, "Item introuvable")

    if quantity <= 0:
        db.delete(item)
        db.commit()
        return {"detail": "Item supprimé du panier"}

    item.quantity = quantity
    db.commit()
    return {"detail": "Quantité mise à jour"}


# 🛒 4 — Supprimer un item
@router.delete("/remove/{item_id}")
def remove_cart_item(item_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):

    item = db.query(CartItem).filter(CartItem.id == item_id, CartItem.user_id == user.id).first()
    if not item:
        raise HTTPException(404, "Item introuvable")

    db.delete(item)
    db.commit()
    return {"detail": "Item supprimé"}


# 🛒 5 — Vider tout le panier
@router.delete("/clear")
def clear_cart(db: Session = Depends(get_db), user=Depends(get_current_user)):

    db.query(CartItem).filter(CartItem.user_id == user.id).delete()
    db.commit()
    return {"detail": "Panier vidé"}
