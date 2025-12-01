from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse
from app.core.security import get_current_user

router = APIRouter(prefix="/products", tags=["Products"])

# ------------------------------
# CREATE PRODUCT
# ------------------------------
@router.post("/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    new_product = Product(
        title=product.title,
        description=product.description,
        price=product.price,
        image=product.image,
        stock=product.stock,
        is_active=True
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


# ------------------------------
# GET ALL PRODUCTS
# ------------------------------
@router.get("/", response_model=list[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    return db.query(Product).filter(Product.is_active == True).all()


# ------------------------------
# GET ONE PRODUCT BY ID
# ------------------------------
@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id, Product.is_active == True).first()

    if not product:
        raise HTTPException(status_code=404, detail="Produit introuvable")

    return product


# ------------------------------
# UPDATE PRODUCT
# ------------------------------
@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, update_data: ProductCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Produit introuvable")

    product.title = update_data.title
    product.description = update_data.description
    product.price = update_data.price
    product.image = update_data.image
    product.stock = update_data.stock

    db.commit()
    db.refresh(product)

    return product


# ------------------------------
# DELETE PRODUCT (Soft Delete)
# ------------------------------
@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Produit introuvable")

    product.is_active = False
    db.commit()

    return {"message": "Produit désactivé avec succès"}
