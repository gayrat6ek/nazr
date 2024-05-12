from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time
from fastapi import Form
from uuid import UUID


class Actions(BaseModel):
    id: int
    name: Optional[str] = None
    status: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Pages(BaseModel):
    id: int
    name: Optional[str] = None
    status: int
    action: list[Actions] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Permissions(BaseModel):
    id: int
    action_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    status: int

    class Config:
        orm_mode = True


class Roles(BaseModel):
    id: int
    name: Optional[str] = None
    status: int
    permission: list[Permissions] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int
    name: Optional[str] = None
    phone_number: Optional[str] = None
    username: Optional[str] = None
    role_id: Optional[int] = None
    surname: Optional[str] = None
    language: Optional[str] = None
    photo: Optional[str] = None
    notification: Optional[bool] = None
    status: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class ResetPassword(BaseModel):
    password: str
    phone_number: Optional[str] = None


class RoleCreate(BaseModel):
    name: str
    status: Optional[int] = 1


class PermissionsGet(BaseModel):
    id: int
    action_id: int
    action: Actions
    role_id: int
    status: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class RoleGet(BaseModel):
    id: int
    name: str
    permission: list[PermissionsGet] = None
    status: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class RoleUpdate(BaseModel):
    id: int
    name: Optional[str] = None
    status: Optional[int] = None
    permissions: Optional[list[int]] = None


class ForgetPassword(BaseModel):
    username: str


class VerfiyOtp(BaseModel):
    username: str
    otp: str
