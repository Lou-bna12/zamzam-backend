from fastapi import FastAPI
from app.database.session import engine, Base
from app.routers.products.products import router as products_router

# Import modèles
import app.models.user

# Import routes AUTH
from app.routers.auth.register import router as register_router
from app.routers.auth.login import router as login_router

# Import routes PROTECTED
from app.routers.protected.admin import router as admin_router
from app.routers.protected.fournisseur import router as fournisseur_router
from app.routers.protected.client import router as client_router

app = FastAPI()

# Création tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "ZamZam API is running"}

# ROUTES AUTH
app.include_router(register_router)
app.include_router(login_router)
app.include_router(products_router)


# ROUTES PROTECTED (avec rôles)
app.include_router(admin_router)
app.include_router(fournisseur_router)
app.include_router(client_router)
