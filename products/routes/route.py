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


ProductRouter = APIRouter()


@ProductRouter.post('/v1/shops', summary="Create Shop", tags=["Shops"],response_model=schema.ShopsList)
async def creat_shop(
    name_uz:Annotated[str,Form()],
    name_ru:Annotated[str,Form()]=None,
    description:Annotated[str,Form()]=None,
    goat:Annotated[bool,Form()]=None,
    cow:Annotated[bool,Form()]=None,
    camel:Annotated[bool,Form()]=None,
    sheep:Annotated[bool,Form()]=None,
    price:Annotated[float,Form()]=None,
    status:Annotated[int,Form()]=None,
    logo:UploadFile=None,
    region_id:Annotated[int,Form()]=None,
    portfolio:list[UploadFile]=None,
    user_id:Annotated[int,Form()]=None,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)
):
    if user_id is None:
        user_id = current_user.id
    if logo is not None:
        folder_name = f"files/{generate_random_filename()+logo.filename}"
        with open(folder_name, "wb") as buffer:
            while True:
                chunk = await logo.read(1024)
                if not chunk:
                    break
                buffer.write(chunk)
        logo = folder_name
    form_data = schema.Shopcreate(
        name_uz=name_uz,
        name_ru=name_ru,
        description=description,
        goat=goat,
        cow=cow,
        camel=camel,
        sheep=sheep,
        price=price,
        status=status,
        logo=logo,
        region_id=region_id,
        user_id=user_id
    )
    query = crud.create_shop(db=db,form_data=form_data)
    if portfolio is not None:
        for file in portfolio:
            folder_name = f"files/{generate_random_filename()+file.filename}"
            with open(folder_name, "wb") as buffer:
                while True:
                    chunk = await file.read(1024)
                    if not chunk:
                        break
                    buffer.write(chunk)

            crud.create_files(db=db,shop_id=query.id,url=folder_name)
    return query


@ProductRouter.delete('/v1/shops/portfolio', summary="Delete portfolio", tags=["Shops"])
async def delete_portfolio(
        id:int,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)
):
    query = crud.delete_portfolio(db=db,id=id)
    return query


@ProductRouter.put('/v1/shops', summary=" Update Shop", tags=["Shops"], response_model=schema.ShopsList)
async def update_shop(
        id:Annotated[int,Form()],
        name_uz:Annotated[str,Form()]=None,
        name_ru:Annotated[str,Form()]=None,
        description:Annotated[str,Form()]=None,
        goat:Annotated[bool,Form()]=None,
        cow:Annotated[bool,Form()]=None,
        camel:Annotated[bool,Form()]=None,
        sheep:Annotated[bool,Form()]=None,
        price:Annotated[str,Form()]=None,
        status:Annotated[int,Form()]=None,
        logo:UploadFile=None,
        region_id:Annotated[int,Form()]=None,
        user_id:Annotated[int,Form()]=None,
        portfolio:list[UploadFile]=None,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)
):
    if logo is not None:
        folder_name = f"files/{generate_random_filename()+logo.filename}"
        with open(folder_name, "wb") as buffer:
            while True:
                chunk = await logo.read(1024)
                if not chunk:
                    break
                buffer.write(chunk)
        logo = folder_name
    form_data = schema.Shopupdate(
        name_uz=name_uz,
        name_ru=name_ru,
        description=description,
        goat=goat,
        cow=cow,
        camel=camel,
        sheep=sheep,
        price=price,
        status=status,
        logo=logo,
        region_id=region_id,
        user_id=user_id,
        id=id
    )
    query = crud.update_shop(db=db, form_data=form_data)
    if portfolio is not None:
        for file in portfolio:
            folder_name = f"files/{generate_random_filename()+file.filename}"
            with open(folder_name, "wb") as buffer:
                while True:
                    chunk = await file.read(1024)
                    if not chunk:
                        break
                    buffer.write(chunk)
            crud.create_files(db=db,shop_id=query.id,url=folder_name)
    return query

@ProductRouter.get('/v1/shops', summary="Get all shops", tags=["Shops"], response_model=Page[schema.ShopsList])
async def get_shops(
        name:Optional[str]=None,
        id:Optional[int]=None,
        status:Optional[int]=None,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    shops = crud.get_shop(db=db,name=name,id=id,status=status)
    return paginate(shops)





@ProductRouter.get('/v1/countries', summary="Get all countries", tags=["Countries"], response_model=Page[schema.CountriesList])
async def get_countries(
        name:Optional[str]=None,
        id:Optional[int]=None,
        status:Optional[int]=None,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    countries = crud.get_country(db=db,name=name,id=id,status=status)
    return paginate(countries)

@ProductRouter.post('/v1/countries', summary="Create country", tags=["Countries"], response_model=schema.CountriesList)
async def create_country(
        form_data:schema.CountriesCreate,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    return crud.create_country(db=db,form_data=form_data)



@ProductRouter.put('/v1/countries', summary="Update country", tags=["Countries"], response_model=schema.CountriesList)
async def update_country(
        form_data:schema.CountriesUpdate,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    query = crud.update_country(db=db,form_data=form_data)
    return query



@ProductRouter.get('/v1/regions', summary="Get all regions", tags=["Countries"], response_model=Page[schema.RegionList])
async def get_regions(
        name:Optional[str]=None,
        id:Optional[int]=None,
        status:Optional[int]=None,
        country_id:Optional[int]=None,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    regions = crud.get_regions(db=db,name=name,id=id,status=status,country_id=country_id)
    return paginate(regions)

@ProductRouter.post('/v1/regions', summary="Create region", tags=["Countries"], response_model=schema.RegionList)
async def create_region(
        form_data:schema.CreateRegion,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    return crud.create_region(db=db,form_data=form_data)


@ProductRouter.put('/v1/regions',summary='Update region',tags=['Countries'],response_model=schema.UpdateRegion)
async def update_region(
        form_data:schema.UpdateRegion,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    query = crud.update_region(db=db,form_data=form_data)


    return query


@ProductRouter.post('/v1/districts',summary='Create district',tags=['Countries'],response_model=schema.DistrictList)
async def create_district(
        form_data:schema.CreateDistrict,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    return crud.create_district(db=db,form_data=form_data)


@ProductRouter.get('/v1/districts',summary='Get all districts',tags=['Countries'],response_model=Page[schema.DistrictList])
async def get_districts(
        name:Optional[str]=None,
        id:Optional[int]=None,
        status:Optional[int]=None,
        region_id:Optional[int]=None,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    districts = crud.get_districts(db=db,name=name,id=id,status=status,region_id=region_id)
    return paginate(districts)


@ProductRouter.put('/v1/districts',summary='Update district',tags=['Countries'],response_model=schema.DistrictList)
async def update_district(
        form_data:schema.UpdateDistrict,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    query = crud.update_district(db=db,form_data=form_data)
    return query



@ProductRouter.post('/v1/category',summary='Create category',tags=['Categories'],response_model=schema.CategoryList)
async def create_category(
        sphera_id: Annotated[int, Form()],
        name_uz:Annotated[str,Form()]=None,
        name_ru:Annotated[str,Form()]=None,
        status:Annotated[int,Form()]=None,
        image:UploadFile=None,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    if image is not None:
        folder_name = f"files/{generate_random_filename()+image.filename}"
        with open(folder_name, "wb") as buffer:
            while True:
                chunk = await image.read(1024)
                if not chunk:
                    break
                buffer.write(chunk)
        image = folder_name
    return crud.create_category(db=db,name_uz=name_uz,name_ru=name_ru,status=status,image=image,sphera_id=sphera_id)


@ProductRouter.get('/v1/category',summary='Get all categories',tags=['Categories'],response_model=Page[schema.CategoryList])
async def get_categories(
        name:Optional[str]=None,
        id:Optional[int]=None,
        status:Optional[int]=None,
        sphera_id:Optional[int]=None,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    categories = crud.get_categories(db=db,name=name,id=id,status=status,sphera_id=sphera_id)
    return paginate(categories)


@ProductRouter.put('/v1/category',summary='Update category',tags=['Categories'],response_model=schema.CategoryList)
async def update_category(
        id:Annotated[int,Form()],
        sphere_id: Annotated[int, Form()]=None,
        name_uz:Annotated[str,Form()]=None,
        name_ru:Annotated[str,Form()]=None,
        status:Annotated[int,Form()]=None,
        image:UploadFile=None,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    if image is not None:
        folder_name = f"files/{generate_random_filename()+image.filename}"
        with open(folder_name, "wb") as buffer:
            while True:
                chunk = await image.read(1024)
                if not chunk:
                    break
                buffer.write(chunk)
        image = folder_name
    return crud.update_category(db=db,id=id,name_uz=name_uz,name_ru=name_ru,status=status,image=image,sphere_id=sphere_id)



@ProductRouter.post('/v1/sphere',summary='Create sphere',tags=['Spheras'],response_model=schema.SpheraList)
async def create_sphere(
        name:Annotated[str,Form()],
        status:Annotated[int,Form()]=None,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    return crud.create_sphere(db=db,name=name,status=status)


@ProductRouter.get('/v1/sphere',summary='Get all spheres',tags=['Spheras'],response_model=Page[schema.SpheraList])
async def get_spheres(
        name:Optional[str]=None,
        id:Optional[int]=None,
        status:Optional[int]=None,
        db: Session = Depends(get_db),
        current_user: user_sch.User = Depends(get_current_user)):
    spheres = crud.get_spheras(db=db,name=name,id=id,status=status)
    return paginate(spheres)





# from fastapi import APIRouter





