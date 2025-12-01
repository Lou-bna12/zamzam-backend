from sqlalchemy import Column, Integer, String, Float, Boolean
from app.database.session import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    image = Column(String, nullable=True)
    stock = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
