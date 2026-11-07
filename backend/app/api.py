from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from sqlalchemy import select, update
from app.db import get_db
from app.models import User, Product, Inventory
from app.schemas import RegisterIn, LoginIn, ProductIn, ReserveIn
from app.security import hash_password, verify_password, create_token, decode_token
router=APIRouter()
def current_user(authorization: str|None=Header(default=None), db:Session=Depends(get_db)):
    if not authorization: raise HTTPException(401,"Authentication required")
    try: subject=decode_token(authorization.removeprefix("Bearer "))["sub"]
    except Exception: raise HTTPException(401,"Invalid token")
    user=db.get(User,subject)
    if not user or not user.active: raise HTTPException(401,"Invalid account")
    return user
def require_roles(*roles):
    def check(user=Depends(current_user)):
        if user.role not in roles: raise HTTPException(403,"Insufficient role")
        return user
    return check
@router.post("/auth/register",status_code=201)
def register(body:RegisterIn,db:Session=Depends(get_db)):
    if db.scalar(select(User).where(User.email==body.email)): raise HTTPException(409,"Email already registered")
    user=User(email=body.email,password_hash=hash_password(body.password)); db.add(user); db.commit(); return {"id":user.id,"email":user.email}
@router.post("/auth/login")
def login(body:LoginIn,db:Session=Depends(get_db)):
    user=db.scalar(select(User).where(User.email==body.email))
    if not user or not verify_password(body.password,user.password_hash): raise HTTPException(401,"Invalid credentials")
    return {"access_token":create_token(user.id),"token_type":"bearer"}
@router.get("/products")
def products(q:str|None=None,limit:int=50,offset:int=0,db:Session=Depends(get_db)):
    stmt=select(Product).where(Product.active.is_(True)).limit(min(limit,100)).offset(offset)
    if q: stmt=stmt.where(Product.name.ilike(f"%{q}%"))
    return db.scalars(stmt).all()
@router.get("/products/{product_id}")
def product(product_id:int,db:Session=Depends(get_db)):
    item=db.get(Product,product_id)
    if not item or not item.active: raise HTTPException(404,"Product not found")
    return item
@router.post("/products",status_code=201)
def create_product(body:ProductIn,db:Session=Depends(get_db),user=Depends(require_roles("admin"))):
    item=Product(**body.model_dump());db.add(item);db.commit();db.refresh(item);return item
@router.post("/inventory/reserve")
def reserve(body:ReserveIn,db:Session=Depends(get_db),user=Depends(current_user)):
    result=db.execute(update(Inventory).where(Inventory.product_id==body.product_id,Inventory.warehouse_id==body.warehouse_id,Inventory.on_hand-Inventory.reserved>=body.quantity).values(reserved=Inventory.reserved+body.quantity))
    if result.rowcount!=1: db.rollback();raise HTTPException(409,"Insufficient inventory")
    db.commit();return {"reserved":body.quantity}
@router.get("/inventory/{product_id}")
def inventory(product_id:int,db:Session=Depends(get_db)):
    return db.scalars(select(Inventory).where(Inventory.product_id==product_id)).all()
