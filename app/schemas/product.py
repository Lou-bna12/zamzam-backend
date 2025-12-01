from pydantic import BaseModel

class ProductBase(BaseModel):
    title: str
    description: str | None = None
    price: float
    image: str | None = None
    stock: int = 0

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
