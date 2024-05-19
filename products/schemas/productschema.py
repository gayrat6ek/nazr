from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time
from fastapi import Form
from uuid import UUID
from users.schemas import user_sch
from . import schema



class FilesGet(BaseModel):
    id: int
    image: Optional[str] = None
    status: int


class ColorCreate(BaseModel):
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    status: Optional[int] = None

class ColorUpdate(BaseModel):
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    id: int
    status: Optional[int] = None


class ColorList(BaseModel):
    id: int
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    status: int


class SizeCreate(BaseModel):
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    status: Optional[int] = None

class SizeUpdate(BaseModel):
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    id: int
    status: Optional[int] = None

class SizeList(BaseModel):
    id: int
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    status: int


class CurrencyCreate(BaseModel):
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    status: Optional[int] = None

class CurrencyUpdate(BaseModel):
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    id: int
    status: Optional[int] = None

class CurrencyList(BaseModel):
    id: int
    name_uz: Optional[str] = None
    name_ru: Optional[str] = None
    status: int



class ProductList(BaseModel):
    id: int
    title: Optional[str] = None
    comment: Optional[str] = None
    price: Optional[float] = None
    status: int
    phone_number: Optional[str] = None
    category: Optional[schema.CategoryList] = None
    currency: Optional[CurrencyList] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    file: Optional[list[FilesGet]] = None
    shop: Optional[schema.ShopsList] = None
    creator: Optional[user_sch.User] = None
    district: Optional[schema.DistrictList] = None
    class Config:
        orm_mode = True
