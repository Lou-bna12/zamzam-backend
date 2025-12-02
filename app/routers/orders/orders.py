from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.database.session import get_db
from app.models.cart import CartItem
from app.models.order import Order, OrderItem
from app.services.email import send_order_confirmation, send_email

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

    # 🔥 Récupérer les items créés
    order_items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()

    # 🔥 Envoi de l'email automatique
    send_order_confirmation(order, order_items)

    return {
        "detail": "Commande créée avec succès",
        "order_id": order.id,
        "total": total_price
    }


# 2️⃣ Voir les commandes de l'utilisateur
@router.get("/")
def get_my_orders(db: Session = Depends(get_db), user=Depends(get_current_user)):
    orders = db.query(Order).filter(Order.user_id == user.id).all()
    return orders


# 3️⃣ Voir détails d'une commande
@router.get("/{order_id}")
def get_order_detail(order_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):

    order = db.query(Order).filter(Order.id == order_id, Order.user_id == user.id).first()

    if not order:
        raise HTTPException(404, "Commande introuvable")

    return {
        "order_id": order.id,
        "total": order.total_price,
        "status": order.status,
        "created_at": order.created_at,
        "items": [
            {
                "product_id": item.product_id,
                "quantity": item.quantity,
                "price": item.price
            }
            for item in order.items
        ]
    }


# 4️⃣ Admin : changer le statut d'une commande
@router.patch("/status/{order_id}")
def update_order_status(order_id: int, status: str, db: Session = Depends(get_db)):

    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(404, "Commande introuvable")

    valid_status = ["pending", "paid", "shipped", "delivered"]

    if status not in valid_status:
        raise HTTPException(400, f"Statut invalide. Statuts autorisés : {valid_status}")

    # Mettre à jour le statut
    order.status = status
    db.commit()
    db.refresh(order)

    # ⚡ Envoi de la notification email
    from app.services.email import send_status_notification
    send_status_notification(order)

    return {
        "detail": f"Statut mis à jour : {status}",
        "order_id": order.id
    }

