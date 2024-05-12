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
from products.queries import crud
from products.schemas import schema
from users.schemas import user_sch


Products = APIRouter()


@Products.post('/v1/shops', summary="Create Shop", tags=["Shops"],response_model=schema.ShopsList)
async def creat_shop(
        form_data:schema.Shopcreate,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)
):
    if form_data.user_id is None:
        form_data.user_id = current_user.id
    return crud.create_shop(db=db, form_data=form_data)



@Products.put('/v1/shops', summary=" Update Shop", tags=["Shops"], response_model=schema.ShopsList)
async def update_shop(
        form_data:schema.Shopupdate,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)
):
    query = crud.update_shop(db=db, form_data=form_data)
    return query

@Products.get('/v1/shops', summary="Get all shops", tags=["Shops"], response_model=Page[schema.ShopsList])
async def get_shops(
        name:Optional[str]=None,
        id:Optional[int]=None,
        status:Optional[int]=None,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    shops = crud.get_shop(db=db,name=name,id=id,status=status)
    return paginate(shops)





@Products.get('/v1/countries', summary="Get all countries", tags=["Countries"], response_model=Page[schema.CountriesList])
async def get_countries(
        name:Optional[str]=None,
        id:Optional[int]=None,
        status:Optional[int]=None,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    countries = crud.get_country(db=db,name=name,id=id,status=status)
    return paginate(countries)

@Products.post('/v1/countries', summary="Create country", tags=["Countries"], response_model=schema.CountriesList)
async def create_country(
        form_data:schema.CountriesCreate,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    return crud.create_country(db=db,form_data=form_data)



@Products.put('/v1/countries', summary="Update country", tags=["Countries"], response_model=schema.CountriesList)
async def update_country(
        form_data:schema.CountriesUpdate,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    query = crud.update_country(db=db,form_data=form_data)
    return query



@Products.get('/v1/regions', summary="Get all regions", tags=["Countries"], response_model=Page[schema.RegionsList])
async def get_regions(
        name:Optional[str]=None,
        id:Optional[int]=None,
        status:Optional[int]=None,
        country_id:Optional[int]=None,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    regions = crud.get_region(db=db,name=name,id=id,status=status,country_id=country_id)
    return paginate(regions)

@Products.post('/v1/regions', summary="Create region", tags=["Countries"], response_model=schema.RegionsList)
async def create_region(
        form_data:schema.RegionsCreate,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    return crud.create_region(db=db,form_data=form_data)


@Products.put('/v1/regions',summary='Update region',tags=['Countries'],response_model=schema.UpdateRegion)
async def update_region(
        form_data:schema.UpdateRegion,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    query = crud.update_region(db=db,form_data=form_data)








