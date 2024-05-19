from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast
from uuid import UUID
from products.models import products
from products.schemas import productschema



def create_size(db:Session,form_data :productschema.SizeCreate):
    query = products.Sizes(
        name_uz=form_data.name_uz,
        name_ru=form_data.name_ru,
        status=form_data.status
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def update_size(db:Session,form_data :productschema.SizeUpdate):
    query = db.query(products.Sizes).filter(products.Sizes.id==form_data.id).first()
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
    return None


def get_size(db:Session,id):
    query = db.query(products.Sizes)
    if id is not None:
        query = query.filter(products.Sizes.id==id)
    return query.all()



def create_color(db:Session,form_data :productschema.ColorCreate):
    query = products.Colors(
        name_uz=form_data.name_uz,
        name_ru=form_data.name_ru,
        status=form_data.status
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def update_color(db:Session,form_data :productschema.ColorUpdate):
    query = db.query(products.Colors).filter(products.Colors.id==form_data.id).first()
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
    return None


def get_color(db:Session,id):
    query = db.query(products.Colors)
    if id is not None:
        query = query.filter(products.Colors.id==id)
    return query.all()


def create_currency(db:Session,form_data :productschema.CurrencyCreate):
    query = products.Currencies(
        name_uz=form_data.name_uz,
        name_ru=form_data.name_ru,
        status=form_data.status
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def update_currency(db:Session,form_data :productschema.CurrencyUpdate):
    query = db.query(products.Currencies).filter(products.Currencies.id==form_data.id).first()
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
    return None


def get_currency(db:Session,id):
    query = db.query(products.Currencies)
    if id is not None:
        query = query.filter(products.Currencies.id==id)
    return query.all()


def create_product(db:Session,
                title,
                comment,
                price,
                status,
                category_id,
                currency_id,
                shop_id,
                phone_number,
                district_id,
                creator_id
                   ):
    query = products.Products(
        title=title,
        comment=comment,
        price=price,
        status=status,
        category_id=category_id,
        currency_id=currency_id,
        shop_id=shop_id,
        phone_number=phone_number,
        district_id=district_id,
        creator_id=creator_id
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query


def update_product(db:Session,
                    id,
                    title,
                    comment,
                    price,
                    status,
                    category_id,
                    currency_id,
                    shop_id,
                    phone_number,
                    district_id,
                   ):
    query = db.query(products.Products).filter(products.Products.id==id).first()
    if query:
        if title is not None:
            query.title = title
        if comment is not None:
            query.comment = comment
        if price is not None:
            query.price = price
        if status is not None:
            query.status = status
        if category_id is not None:
            query.category_id = category_id
        if currency_id is not None:
            query.currency_id = currency_id
        if shop_id is not None:
            query.shop_id = shop_id
        if phone_number is not None:
            query.phone_number = phone_number
        if district_id is not None:
            query.district_id = district_id
        db.commit()
        db.refresh(query)
        return query
    return None


def get_product(db:Session,id,any_text,currency_id,category_id,shop_id,district_id,status,creator_id,sphera_id):
    query = db.query(products.Products)
    if id is not None:
        query = query.filter(products.Products.id==id)
    if any_text is not None:
        query = query.filter(or_(products.Products.title.ilike(f"%{any_text}%"),

                                 products.Products.comment.ilike(f"%{any_text}%"),
                                 products.Products.phone_number.ilike(f"%{any_text}%"),
                                 products.Categories.name_ru.ilike(f"%{any_text}%"),
                                 products.Categories.name_uz.ilike(f"%{any_text}%"),
                                 ))
    if currency_id is not None:
        query = query.filter(products.Products.currency_id==currency_id )
    if category_id is not None:
        query = query.filter(products.Products.category_id==category_id)
    if shop_id is not None:
        query = query.filter(products.Products.shop_id==shop_id)
    if district_id is not None:
        query = query.filter(products.Products.district_id==district_id)
    if status is not None:
        query = query.filter(products.Products.status==status)
    if creator_id is not None:
        query = query.filter(products.Products.creator_id==creator_id)
    if sphera_id is not None:
        query = query.filter(products.Categories.sphera_id==sphera_id)
    return query.all()


def delete_prod_image(db:Session,id):
    query = db.query(products.Files).filter(products.Files.id==id).first()
    if query:
        db.delete(query)
        db.commit()
        return query
    return None
