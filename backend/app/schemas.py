from pydantic import BaseModel, EmailStr, Field
class RegisterIn(BaseModel): email: EmailStr; password: str = Field(min_length=10)
class LoginIn(BaseModel): email: EmailStr; password: str
class ProductIn(BaseModel): name: str; price: float = Field(gt=0); description: str = ""; category_id: int|None=None
class ReserveIn(BaseModel): product_id: int; warehouse_id: int; quantity: int = Field(gt=0)
class OrderIn(BaseModel): items: list[dict]
