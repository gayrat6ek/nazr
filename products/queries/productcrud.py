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