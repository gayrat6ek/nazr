from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time
from fastapi import Form
from uuid import UUID
from users.schemas import user_sch



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
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


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
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
