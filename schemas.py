from datetime import datetime

from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str = ""
    price: float
    category: str = "general"

class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    category: str
    updated_at: datetime