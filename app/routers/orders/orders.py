from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.database.session import get_db
from app.models.cart import CartItem
from app.models.order import Order, OrderItem

router = APIRouter(prefix="/orders", tags=["Orders"])


# 1️⃣ Créer une commande depuis le panier
@router.post("/create")
def create_order(db: Session = Depends(get_db), user=Depends(get_current_user)):

    # récupérer les items du panier
    cart_items = db.query(CartItem).filter(CartItem.user_id == user.id).all()

    if not cart_items:
        raise HTTPException(400, "Votre panier est vide")

    # calcul du total
    total_price = sum(item.quantity * item.product.price for item in cart_items)

    # créer la commande
    order = Order(
        user_id=user.id,
        total_price=total_price,
        status="pending"
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    # créer les items de commande
    for item in cart_items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.product.price
        )
        db.add(order_item)

    # vider le panier
    db.query(CartItem).filter(CartItem.user_id == user.id).delete()

    db.commit()

    return {
        "detail": "Commande créée avec succès",
        "order_id": order.id,
        "total": total_price
    }
