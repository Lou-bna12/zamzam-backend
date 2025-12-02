from sqlalchemy import Column, Integer, String, Boolean
from app.database.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    role = Column(String, default="client")
    is_active = Column(Boolean, default=True)
    cart_items = relationship("CartItem", back_populates="user", cascade="all, delete-orphan")

