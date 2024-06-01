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
from users.queries import query
from users.schemas import user_sch


user_router = APIRouter()



@user_router.post("/login", summary="Create access and refresh tokens for user",tags=["User"])
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(OAuth2PasswordRequestForm),
    db: Session = Depends(get_db),
):
    form_data.username = form_data.username.replace(" ","")
    form_data.username = form_data.username.replace("+","")
    user = query.get_user(db, form_data.username)
    if user is None or user.status == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password or user is inactive",
        )


    hashed_pass = user.password
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )

    return {
        "access_token": create_access_token(user.username),
        "refresh_token": create_refresh_token(user.username),
        "user": {'id':user.id,'name':user.name,'surname':user.surname,'username':user.username,'photo':user.photo,'notification':user.notification,'language':user.language,'status':user.status,}
    }


@user_router.post("/v2/login", summary="Create access and refresh tokens for user",tags=["User"])
async def login(
    form_data: user_sch.Login,
    db: Session = Depends(get_db),
):
    form_data.username = form_data.username.replace(" ","")
    form_data.username = form_data.username.replace("+","")
    user = query.get_user(db, form_data.username)
    if user is None or user.status == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password or user is inactive",
        )


    hashed_pass = user.password
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )

    return {
        "access_token": create_access_token(user.username),
        "refresh_token": create_refresh_token(user.username),
        "user": {'id':user.id,'name':user.name,'surname':user.surname,'username':user.username,'photo':user.photo,'notification':user.notification,'language':user.language,'status':user.status,}
    }






@user_router.post("/refresh",response_model=user_sch.User, summary="Refresh access token",tags=["User"])
async def refresh(
    refresh_token: str,
    db: Session = Depends(get_db),
):
    username = verify_refresh_token(refresh_token)
    if username is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid refresh token",
        )
    return {"access_token": create_access_token(username)}



@user_router.post("/register",response_model=user_sch.User, summary="Register a new user",tags=["User"])
async def register(
    username:Annotated[str, Form()],
    password:Annotated[str, Form()],
    name:Annotated[str, Form()]=None,
    surname:Annotated[str, Form()]=None,
    language:Annotated[str, Form()]=None,
    email :Annotated[str,Form()]=None,
    photo:UploadFile = None,
    notification:Annotated[bool, Form()]=None,
    db: Session = Depends(get_db)):
    if photo is not None:
        folder_name = f"files/{generate_random_filename()+photo.filename}"
        with open(folder_name, "wb") as buffer:
            while True:
                chunk = await photo.read(1024)
                if not chunk:
                    break
                buffer.write(chunk)
        photo = folder_name
    otp = 1111#generate_otp()

    #get_user = query.get_user_byphone(db, email=form_data.email,phone_number=form_data.phone)
    #if get_user:
    username = username.replace(" ","")
    username = username.replace("+","")
    user = query.user_create(db=db,username=username,password=password,name=name,surname=surname,photo=photo,notification=notification,language=language,status=0,email=email,otp=otp)

    #current_user: user_sch.User = Depends(get_current_user)
    return user

@user_router.get("/me", response_model=user_sch.User, summary="Get current user",tags=["User"])
async def current_user(db:Session=Depends(get_db),current_user: user_sch.User = Depends(get_current_user)):
    return current_user


@user_router.put('/update',summary="Reset password",tags=["User"])
async def reset_password(
    username:Annotated[str, Form()],
    password:Annotated[str, Form()],
    name:Annotated[str, Form()]=None,
    surname:Annotated[str, Form()]=None,
    language:Annotated[str, Form()]=None,
    photo:UploadFile = None,
    notification:Annotated[bool, Form()]=None,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)

):
    
    if photo is not None:
        folder_name = f"files/{generate_random_filename()+photo.filename}"
        with open(folder_name, "wb") as buffer:
            while True:
                chunk = await photo.read(1024)
                if not chunk:
                    break
                buffer.write(chunk)
        photo = folder_name
    query.user_update(db=db,
                      id=current_user.id,
                      password=password,
                      name=name,
                      username=username,
                      surname=surname,
                      language=language,
                      photo=photo,
                      notification=notification
                      )
    
    return {"message":"User updated successfully ",'success':True}


@user_router.get('/users',summary="Get all users",tags=["User"],response_model=Page[user_sch.User])
async def get_users(name: Optional[str]=None,
                    id: Optional[int]=None,
                    phone_number: Optional[str]=None,
                    status: Optional[int]=None,
                    role_id: Optional[int]=None,

                    db: Session = Depends(get_db),
                    current_user: user_sch.User = Depends(get_current_user)):
    users = query.get_users(db,name=name,id=id,phone_number=phone_number,status=status,role_id=role_id)
    return paginate(users)



@user_router.post('/forget',summary="Forget password",tags=['User'])
async def forget_password(
    form_data :user_sch.ForgetPassword,
    db:Session= Depends(get_db)
):
    user = query.get_user(db=db,username=form_data.username)
    if user:
        otp=1111#generate_otp()
        query.user_update(db=db,status=0,otp=otp)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )


@user_router.post('/roles',summary="Create a new role",tags=["User"],response_model=user_sch.RoleGet)
async def create_role(
    name:str,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)
):
    
    return query.create_role(db=db,name=name)



@user_router.get('/roles',summary="Get all roles",tags=["User"],response_model=Page[user_sch.RoleGet])
async def get_roles(
    name:Optional[str]=None,
    status:Optional[int]=None,
    id:Optional[int]=None,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)
):
    roles = query.get_roles(db,name=name,status=status,id=id)
    return paginate(roles)


@user_router.put('/roles',summary="Update role",tags=["User"],response_model=user_sch.RoleGet)
async def update_role(
    form_data:user_sch.RoleUpdate,
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)
):
    
    if form_data.permissions is not None:
        query.delete_permissions(db=db,role_id=form_data.id)
        for permission in form_data.permissions:
            query.create_permissions(db=db,role_id=form_data.id,action_id=permission)
    role_update = query.update_role(db=db,form_data=form_data)
    return role_update


@user_router.get('/permissions',summary="Get all permissions",tags=["User"],response_model=Page[user_sch.Pages])
async def get_permissions(
    db: Session = Depends(get_db),
    current_user: user_sch.User = Depends(get_current_user)
):
    permissions = query.get_pages(db)
    return paginate(permissions)



@user_router.post('/verify',summary="verify user otp",tags=['User'])
async def verify_user(
    form_data :user_sch.VerfiyOtp,
    db:Session=Depends(get_db)):
    form_data.username = form_data.username.replace(" ","")
    form_data.username = form_data.username.replace("+","")
    get_user = query.get_user(db=db,username=form_data.username)
    if get_user and get_user.otp == form_data.otp:
        otp =1111 #generate_otp()
        update_user = query.user_update(db=db,id=get_user.id,status=1)
        return {
        "access_token": create_access_token(get_user.username),
        "refresh_token": create_refresh_token(get_user.username)}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="otp does not match or user not found",
        )














