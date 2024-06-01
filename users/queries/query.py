from sqlalchemy.orm import Session
from typing import Optional
import bcrypt

import pytz
from sqlalchemy.sql import func
from datetime import datetime,timedelta
from sqlalchemy import or_, and_, Date, cast
from uuid import UUID
from users.models.user_model import Users  
from users.models import user_model
from users.schemas import user_sch


def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed_password.decode("utf-8")

def get_user(db: Session, username: str):
    return db.query(Users).filter(Users.username == username).first()

def get_user_byphone(db: Session, username:Optional[str]=None):
    query = db.query(Users)
    if username is not None:

        query = query.filter(Users.username == username)
    return query.first()

def user_create(db: Session,form_data:user_sch.Register,status,otp):
    hashed_password = hash_password(form_data.password)

    db_user = Users(
        username=form_data.username,
        password=hashed_password,
        name=form_data.name,
        otp=otp,
        status=status

    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def user_update(db:Session,id:int,status:Optional[int]=None,password:Optional[str]=None,username:Optional[str]=None,name:Optional[str]=None,surname:Optional[str]=None,language:Optional[str]=None,photo:Optional[str]=None,notification:Optional[bool]=None,otp:Optional[int]=None):
    db_user = db.query(Users).filter(Users.id == id).first()
    if status is not None:
        db_user.status = status
    if password is not None:
        db_user.password = hash_password(password)
    if username is not None:
        username = username.replace(" ","")
        username = username.replace("+","")
        db_user.username = username
    if name is not None:
        db_user.name = name
    if surname is not None:
        db_user.surname = surname
    if language is not None:
        db_user.language = language
    if photo is not None:
        db_user.photo = photo
    if notification is not None:
        db_user.notification = notification
    if otp is not None:
        db_user.otp=otp
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session,name,id,status,role_id):
    query = db.query(Users)
    if name is not None:
        query = query.filter(Users.name.ilike(f"%{name}%"))
    if id is not None:
        query = query.filter(Users.id == id)
    if status is not None:
        query = query.filter(Users.status == status)
    if role_id is not None:
        query = query.filter(Users.role_id == role_id)
    return query.all()


#create role 

def create_role(db:Session,form_data:user_sch.RoleCreate):  
    query = user_model.Roles(
        name=form_data.name,
        status=form_data.status
    )
    db.add(query)
    db.commit()
    db.refresh(query)
    return query

def get_roles(db:Session,name,status,id):
    query = db.query(user_model.Roles)
    if name is not None:
        query = query.filter(user_model.Roles.name.ilike(f"%{name}%"))
    if status is not None:
        query = query.filter(user_model.Roles.status == status)
    if id is not None:
        query = query.filter(user_model.Roles.id == id)
    return query.all()


def update_role(db:Session,form_data:user_sch.RoleUpdate):
    db_role = db.query(user_model.Roles).filter(user_model.Roles.id == form_data.id).first()
    if form_data.name is not None:
        db_role.name = form_data.name
    if form_data.status is not None:
        db_role.status = form_data.status
    db.commit()
    db.refresh(db_role)
    return db_role


def delete_permissions(db:Session,role_id:int):
    db.query(user_model.Permissions).filter(user_model.Permissions.role_id == role_id).delete()
    db.commit()
    return {"message":"Permissions deleted successfully",'success':True}

def create_permissions(db:Session,role_id:int,action_id:int):
    query = user_model.Permissions(
        role_id=role_id,
        action_id=action_id)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query

def get_pages(db:Session):
    return db.query(user_model.Pages).all()

