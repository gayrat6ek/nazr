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


@ProductCreateRouter.post('/v1/currency',summary="Create currency",tags=["Currency"])
async def create_currency(
    form_data: productschema.CurrencyCreate,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)
):
    return productcrud.create_currency(db,form_data)


@ProductCreateRouter.put('/v1/currency',summary="Update currency",tags=["Currency"])
async def update_currency(
    form_data: productschema.CurrencyUpdate,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)
):
    return productcrud.update_currency(db,form_data)


@ProductCreateRouter.get('/v1/currency',summary="Get currency by id",tags=["Currency"],response_model=Page[productschema.CurrencyList])
async def get_currency(
    id:Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)
):
    return paginate(productcrud.get_currency(db,id))


@ProductCreateRouter.post("/v1/product", summary="Create product",tags=["Product"])
async def create_product(
    title: Annotated[str,Form()],
    comment: Annotated[str,Form()]=None,
    price: Annotated[float,Form()]=None,
    status: Annotated[int,Form()]=None,
    shop_id: Annotated[int,Form()]=None,
    phone_number: Annotated[str,Form()]=None,
    district: Annotated[int,Form()]=None,
    currency_id: Annotated[int,Form()]=None,
    category_id: Annotated[int,Form()]=None,
    images:list[UploadFile] = None,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)
):
    query =  productcrud.create_product(db=db,
                                        title=title,
                                        comment=comment,
                                        price=price,
                                        status=status,
                                        shop_id=shop_id,
                                        phone_number=phone_number,
                                        district_id=district,
                                        currency_id=currency_id,
                                        category_id=category_id,
                                        creator_id=current_user.id)
    if images:
        for image in images:
            filename = "files/"+generate_random_filename()+image.filename
            with open(f"{filename}", "wb") as buffer:
                while True:
                    chunk = await image.read(1024)
                    if not chunk:
                        break
                    buffer.write(chunk)
            crud.create_files(db,url=filename,product_id=query.id)
    return {'success':True,'message':'Product created successfully','id':query.id}


@ProductCreateRouter.put("/v1/product", summary="Update product",tags=["Product"])
async def update_product(
    id: Annotated[int,Form()],
    title: Annotated[str,Form()],
    comment: Annotated[str,Form()]=None,
    price: Annotated[float,Form()]=None,
    status: Annotated[int,Form()]=None,
    shop_id: Annotated[int,Form()]=None,
    phone_number: Annotated[str,Form()]=None,
    district: Annotated[int,Form()]=None,
    currency: Annotated[int,Form()]=None,
    category_id: Annotated[int,Form()]=None,
    images:list[UploadFile] = None,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)
):
    if images:
        for image in images:
            filename = "files/"+generate_random_filename()+image.filename
            with open(f"files/{filename}", "wb") as buffer:
                while True:
                    chunk = await image.read(1024)
                    if not chunk:
                        break
                    buffer.write(chunk)
            crud.create_files(db,url=filename,product_id=id)
    return productcrud.update_product(db=db,
                                      id=id,
                                      title=title,
                                      comment=comment,
                                      price=price,
                                      status=status,
                                      shop_id=shop_id,
                                      phone_number=phone_number,
                                      district_id=district,
                                      currency_id=currency,
                                      category_id=category_id)


@ProductCreateRouter.get("/v1/product", summary="Get product by id",tags=["Product"],response_model=Page[productschema.ProductList])
async def get_product(
    id:Optional[int] = None,
    any_text:Optional[str] = None,
    sphera_id:Optional[int] = None,
    category_id:Optional[int] = None,
    shop_id:Optional[int] = None,
    district_id:Optional[int] = None,
    status:Optional[int] = None,
    currency_id:Optional[int] = None,
    db: Session = Depends(get_db),
    creator_id:Optional[int] = None,
    current_user: user_sch.User = Depends(get_current_user)
):
    return paginate(productcrud.get_product(db=db,id=id,any_text=any_text,sphera_id=sphera_id,category_id=category_id,shop_id=shop_id,district_id=district_id,status=status,currency_id=currency_id,creator_id=creator_id))

@ProductCreateRouter.delete("/v1/product/image", summary="Delete product image",tags=["Product"],)
async def delete_prod_image(
    id: int,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)
):
    return productcrud.delete_prod_image(db=db,id=id)









