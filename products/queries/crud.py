from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast
from uuid import UUID
from products.models import products
from products.schemas import schema



def create_shop(db:Session,form_data :schema.Shopcreate):
    query = products.Shops(
        name_uz=form_data.name_uz,
        name_ru=form_data.name_ru,
        user_id=form_data.user_id,
        status=form_data.status,
        description=form_data.description,
        price=form_data.price,
        region_id=form_data.region_id,
        logo=form_data.logo,
        sphera_id=form_data.sphera_id
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def create_shopcategory(db:Session,shop_id:int,category_id:int):
    query = products.ShopCategories(
        shop_id=shop_id,
        category_id=category_id
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def delete_shopcategory(db:Session,id):
    query = db.query(products.ShopCategories).filter(products.ShopCategories.id==id).first()
    if query:
        db.delete(query)
        db.commit()
        return query
    return query

def update_shop(db:Session,form_data :schema.Shopupdate):
    query = db.query(products.Shops).filter(products.Shops.id==form_data.id).first()
    if query:
        if form_data.name_uz is not None:
            query.name_uz = form_data.name_uz
        if form_data.name_ru is not None:
            query.name_ru = form_data.name_ru
        if form_data.user_id is not None:
            query.user_id = form_data.user_id
        if form_data.status is not None:
            query.status = form_data.status
        if form_data.description is not None:
            query.description = form_data.description
        if form_data.price is not None:
            query.price = form_data.price
        if form_data.region_id is not None:
            query.region_id = form_data.region_id
        if form_data.logo is not None:
            query.logo = form_data.logo
        if form_data.sphera_id is not None:
            query.sphera_id = form_data.sphera_id
        db.commit()
        db.refresh(query)
        return query
    return query






def get_shop(db:Session,name,id,status):
    query = db.query(products.Shops)
    if name is not None:
        query = query.filter(or_(products.Shops.name_uz==name,products.Shops.name_ru==name))
    if id is not None:
        query = query.filter(products.Shops.id==id)
    if status is not None:
        query = query.filter(products.Shops.status==status)
    return query.all()


def delete_portfolio(db:Session,id):
    query = db.query(products.Files).filter(products.Files.id==id).first()
    if query:
        db.delete(query)
        db.commit()
        return query
    return query


def create_country(db:Session,form_data:schema.CountriesCreate):
    query = products.Countries(
        name_uz=form_data.name_uz,
        name_ru=form_data.name_ru,
        status=form_data.status
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def update_country(db:Session,form_data:schema.CountriesUpdate):
    query = db.query(products.Countries).filter(products.Countries.id==form_data.id).first()
    if query:
        if form_data.name_uz is not None:
            query.name_uz = form_data.name_uz
        if form_data.name_ru is not None:
            query.name_ru = form_data.name_ru
        if form_data.status is not None:
            query.status = form_data.status
        db.commit()
        db.refresh(query)
        return query
    return query


def get_country(db:Session,name,id,status):
    query = db.query(products.Countries)
    if name is not None:
        query = query.filter(or_(products.Countries.name_uz==name,products.Countries.name_ru==name))
    if id is not None:
        query = query.filter(products.Countries.id==id)
    if status is not None:
        query = query.filter(products.Countries.status==status)
    return query.all()


def create_region(db:Session,form_data:schema.CreateRegion):
    query = products.Regions(
        name_uz=form_data.name_uz,
        name_ru=form_data.name_ru,
        status=form_data.status,
        country_id=form_data.country_id
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def update_region(db:Session,form_data:schema.UpdateRegion):
    query = db.query(products.Regions).filter(products.Regions.id==form_data.id).first()
    if query:
        if form_data.name_uz is not None:
            query.name_uz = form_data.name_uz
        if form_data.name_ru is not None:
            query.name_ru = form_data.name_ru
        if form_data.status is not None:
            query.status = form_data.status
        if form_data.country_id is not None:
            query.country_id = form_data.country_id
        db.commit()
        db.refresh(query)
        return query
    return query


def get_regions(db:Session,name,country_id,status,id):
    query = db.query(products.Regions)
    if name is not None:
        query = query.filter(or_(products.Regions.name_uz==name,products.Regions.name_ru==name))
    if country_id is not None:
        query = query.filter(products.Regions.country_id==country_id)
    if status is not None:
        query = query.filter(products.Regions.status==status)
    if id is not None:
        query = query.filter(products.Regions.id==id)
    return query.all()


def create_files(db:Session,url:Optional[str],shop_id:Optional[int]=None,detail_id:Optional[int]=None,product_id:Optional[int]=None,category_id:Optional[int]=None):
    query = products.Files(
        image=url,
        shop_id=shop_id,
        detail_id=detail_id,
        product_id=product_id,
        category_id=category_id
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query



def create_district(db:Session,form_data:schema.CreateDistrict):
    query = products.Districts(
        name_uz=form_data.name_uz,
        name_ru=form_data.name_ru,
        status=form_data.status,
        region_id=form_data.region_id
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def update_district(db:Session,form_data:schema.UpdateDistrict):
    query = db.query(products.Districts).filter(products.Districts.id==form_data.id).first()
    if query:
        if form_data.name_uz is not None:
            query.name_uz = form_data.name_uz
        if form_data.name_ru is not None:
            query.name_ru = form_data.name_ru
        if form_data.status is not None:
            query.status = form_data.status
        if form_data.region_id is not None:
            query.region_id = form_data.region_id
        db.commit()
        db.refresh(query)
        return query
    return query


def get_districts(db:Session,name,region_id,status,id):
    query = db.query(products.Districts)
    if name is not None:
        query = query.filter(or_(products.Districts.name_uz==name,products.Districts.name_ru==name))
    if region_id is not None:
        query = query.filter(products.Districts.region_id==region_id)
    if status is not None:
        query = query.filter(products.Districts.status==status)
    if id is not None:
        query = query.filter(products.Districts.id==id)
    return query.all()


def create_category(db:Session,name_uz,name_ru,status, sphera_id):
    query = products.Categories(
        name_uz=name_uz,
        name_ru=name_ru,
        status=status,
        sphera_id=sphera_id
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def update_category(db:Session,id,name_uz,name_ru,status,sphera_id):
    query = db.query(products.Categories).filter(products.Categories.id==id).first()
    if query:
        if name_uz is not None:
            query.name_uz = name_uz
        if name_ru is not None:
            query.name_ru = name_ru
        if status is not None:
            query.status = status

        if sphera_id is not None:
            query.sphera_id = sphera_id
        db.commit()
        db.refresh(query)
        return query
    return query



def get_categories(db:Session,name,status,id,sphera_id):
    query = db.query(products.Categories)
    if name is not None:
        query = query.filter(or_(products.Categories.name_uz==name
                                 ,products.Categories.name_ru==name))
    if status is not None:
        query = query.filter(products.Categories.status==status)
    if id is not None:
        query = query.filter(products.Categories.id==id)
    if sphera_id is not None:
        query = query.filter(products.Categories.sphera_id==sphera_id)

    return query.all()


def create_sphere(db:Session,name,status):
    query = products.Spheras(
        name=name,
        status=status
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query



def get_spheras(db:Session,name,status,id):
    query = db.query(products.Spheras)
    if name is not None:
        query = query.filter(products.Spheras.name==name)
    if status is not None:
        query = query.filter(products.Spheras.status==status)
    if id is not None:
        query = query.filter(products.Spheras.id==id)
    return query.all()


