from fastapi import APIRouter
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status,Form,UploadFile
from fastapi_pagination import paginate, Page, add_pagination
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional,Annotated
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from uuid import UUID
import random
from services import (
    create_access_token,
    create_refresh_token,
    get_db,
    get_current_user,
    verify_password,
    verify_refresh_token,
    generate_random_filename,
    generate_otp
)
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from typing import Union, Any
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database import engine, SessionLocal

from dotenv import load_dotenv
import os
load_dotenv()
from products.queries import crud,productcrud
from products.schemas import schema,productschema
from users.schemas import user_sch


ProductCreateRouter = APIRouter()


@ProductCreateRouter.post("/v1/size", summary="Create size",tags=["Size"])
async def create_size(
    form_data: productschema.SizeCreate,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user),
):
    return productcrud.create_size(db,form_data)

@ProductCreateRouter.put("/v1/size", summary="Update size",tags=["Size"])
async def update_size(
    form_data: productschema.SizeUpdate,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user),

):
    return productcrud.update_size(db,form_data)

@ProductCreateRouter.get("/v1/size", summary="Get size by id",tags=["Size"],response_model=Page[productschema.SizeList])
async def get_size(
    id:Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user),

):
    return paginate(productcrud.get_size(db,id))


@ProductCreateRouter.post("/v1/color", summary="Create color",tags=["Color"])
async def create_color(
    form_data: productschema.ColorCreate,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user),
):
    return productcrud.create_color(db,form_data)

@ProductCreateRouter.put("/v1/color", summary="Update color",tags=["Color"])
async def update_color(
    form_data: productschema.ColorUpdate,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)
):
    return productcrud.update_color(db,form_data)

@ProductCreateRouter.get("/v1/color", summary="Get color by id",tags=["Color"],response_model=Page[productschema.ColorList])
async def get_color(
    id:Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)
):
    return paginate(productcrud.get_color(db,id))





