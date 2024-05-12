from pydantic import BaseModel, validator
from fastapi import Form, UploadFile, File
from typing import Optional, Annotated, Dict
from datetime import datetime, time
from fastapi import Form
from uuid import UUID
from users.schemas import user_sch




class Shopcreate(BaseModel):
    name_uz:Optional[str]=None
    name_ru:Optional[str]=None
    user_id :Optional[int]=None



class Shopupdate(BaseModel):
    name_uz:Optional[str]=None
    name_ru:Optional[str]=None
    user_id :Optional[int]=None
    status: Optional[int]=None
    id:int


class ShopsList(BaseModel):
    id:int
    name_uz:Optional[str]=None
    name_ru:Optional[str]=None
    status: Optional[int]=None
    user_id :Optional[int]=None
    created_at: Optional[datetime]=None
    updated_at: Optional[datetime]=None
    user:Optional[user_sch.User] =None

    class Config:
        orm_mode = True


class CountriesCreate(BaseModel):
    name_uz:Optional[str]=None
    name_ru:Optional[str]=None
    status: Optional[int]=None


class CountriesUpdate(BaseModel):
    name_uz:Optional[str]=None
    name_ru:Optional[str]=None
    status: Optional[int]=None
    id:int

class CountriesList(BaseModel):
    id:int
    name_uz:Optional[str]=None
    name_ru:Optional[str]=None
    status:Optional[int]=None
    created_at: Optional[datetime]=None
    updated_at: Optional[datetime]=None

    class Config:
        orm_mode = True



class CreateRegion(BaseModel):
    name_uz:Optional[str]=None
    name_ru:Optional[str]=None
    status: Optional[int]=None
    country_id:Optional[int]=None


class UpdateRegion(BaseModel):
    name_uz:Optional[str]=None
    name_ru:Optional[str]=None
    status: Optional[int]=None
    country_id:Optional[int]=None
    id:int



class RegionList(BaseModel):
    id:int
    name_uz:Optional[str]=None
    name_ru:Optional[str]=None
    status:Optional[int]=None
    country_id:Optional[int]=None
    country:Optional[CountriesList]=None
    created_at: Optional[datetime]=None
    updated_at: Optional[datetime]=None

    class Config:
        orm_mode = True






