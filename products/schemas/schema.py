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


class Shopcreate(BaseModel):
    name_uz:Optional[str]=None
    name_ru:Optional[str]=None
    user_id :Optional[int]=None
    status: Optional[int]=None
    description: Optional[str]=None
    categories: Optional[list[int]]=None
    price: Optional[float]=None
    logo: Optional[str]=None
    region_id: Optional[int]=None
    files:Optional[list[str]] = None




class Shopupdate(BaseModel):
    name_uz:Optional[str]=None
    name_ru:Optional[str]=None
    user_id :Optional[int]=None
    status: Optional[int]=None
    id:int
    description: Optional[str]=None
    price: Optional[float]=None
    logo: Optional[str]=None
    region_id: Optional[int]=None
    files:Optional[list[str]] = None
    categories: Optional[list[int]]=None






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

    class Config:
        orm_mode = True







class CreateDistrict(BaseModel):
    name_uz:Optional[str]=None
    name_ru:Optional[str]=None
    status: Optional[int]=None
    region_id:Optional[int]=None

class UpdateDistrict(BaseModel):
    name_uz:Optional[str]=None
    name_ru:Optional[str]=None
    status: Optional[int]=None
    region_id:Optional[int]=None
    id:int

class DistrictList(BaseModel):
    id:int
    name_uz:Optional[str]=None
    name_ru:Optional[str]=None
    status:Optional[int]=None
    region_id:Optional[int]=None
    region:Optional[RegionList]=None

    class Config:
        orm_mode = True


class SphereCreate(BaseModel):
    name:Optional[str]=None
    status: Optional[int]=None

class SpheraList(BaseModel):
    id:int
    name:Optional[str]=None
    status:Optional[int]=None
    class Config:
        orm_mode = True


class  CategoryCreate(BaseModel):
    name_uz:Optional[str]=None
    name_ru:Optional[str]=None
    status: Optional[int]=None
    image:Optional[str]=None
    sphera_id:Optional[int]=None



class CategoryUpdate(BaseModel):
    name_uz:Optional[str]=None
    name_ru:Optional[str]=None
    status: Optional[int]=None
    image:Optional[str]=None
    sphera_id:Optional[int]=None
    id:int





class CategoryList(BaseModel):
    id:int
    name_uz:Optional[str]=None
    name_ru:Optional[str]=None
    status:Optional[int]=None
    image:Optional[str]=None
    sphera:Optional[SpheraList]=None
    file : Optional[list[FilesGet]]=None
    class Config:
        orm_mode = True

class ShopCategory(BaseModel):
    id:int
    category:Optional[CategoryList]=None

class ShopsList(BaseModel):
    id:int
    name_uz:Optional[str]=None
    name_ru:Optional[str]=None
    status: Optional[int]=None
    user_id :Optional[int]=None
    description: Optional[str]=None
    price: Optional[float]=None
    logo: Optional[str]=None
    region_id: Optional[int]=None
    region:Optional[RegionList]=None
    user:Optional[user_sch.User] =None
    file:Optional[list[FilesGet]]=None
    shopcategory:Optional[list[ShopCategory]]=None
    class Config:
        orm_mode = True


