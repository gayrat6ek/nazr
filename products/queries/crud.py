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
        user_id=form_data.user_id
    )
    db.add(query)
    db.commit()
    db.refresh(query)
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