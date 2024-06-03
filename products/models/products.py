from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Float,
    DateTime,
    Boolean,
    BIGINT,
    Table,
    Time,
    JSON,
    VARCHAR,
    Date
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB
from datetime import datetime
import pytz
import uuid
from users.models.user_model import Base


timezonetash = pytz.timezone("Asia/Tashkent")


class Shops(Base):
    __tablename__ = "shops"
    id = Column(BIGINT, primary_key=True, index=True)
    name_uz = Column(String, nullable=True)
    name_ru = Column(String, nullable=True)
    description = Column(String, nullable=True)
    goat = Column(Boolean,default=False)
    cow = Column(Boolean,default=False)
    camel = Column(Boolean,default=False)
    sheep = Column(Boolean,default=False)
    price = Column(Float,nullable=True)
    status = Column(Integer,default=1)
    logo = Column(String,nullable=True)
    user_id = Column(BIGINT,ForeignKey('users.id'))
    region_id = Column(BIGINT,ForeignKey('regions.id'))
    region = relationship("Regions",back_populates="shop")
    user = relationship("Users",back_populates="shop")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    product = relationship("Products",back_populates="shop")
    file = relationship("Files",back_populates="shop")
    shopcategory = relationship("ShopCategories",back_populates="shop")





class Countries(Base):
    __tablename__ = "countries"
    id = Column(BIGINT, primary_key=True, index=True)
    name_uz = Column(String, nullable=True)
    name_ru = Column(String, nullable=True)
    status = Column(Integer,default=1)
    region = relationship("Regions",back_populates="country")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())



class Regions(Base):
    __tablename__ = "regions"
    id = Column(BIGINT, primary_key=True, index=True)
    name_uz = Column(String, nullable=True)
    name_ru = Column(String, nullable=True)
    status = Column(Integer,default=1)
    country_id = Column(BIGINT,ForeignKey('countries.id'))
    country = relationship("Countries",back_populates="region")
    district = relationship("Districts",back_populates="region")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    shop = relationship("Shops",back_populates="region")

class Districts(Base):
    __tablename__ = "districts"
    id = Column(BIGINT, primary_key=True, index=True)
    name_uz = Column(String, nullable=True)
    name_ru = Column(String, nullable=True)
    status = Column(Integer,default=1)
    region_id = Column(BIGINT,ForeignKey('regions.id'))
    region = relationship("Regions",back_populates="district")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    product = relationship("Products",back_populates="district")



class Currencies(Base):
    __tablename__ = "currencies"
    id = Column(BIGINT, primary_key=True, index=True)
    name_uz = Column(String, nullable=True)
    name_ru = Column(String, nullable=True)
    status = Column(Integer,default=1)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    product = relationship("Products",back_populates="currency")



class Spheras(Base):
    __tablename__ = "spheras"
    id = Column(BIGINT, primary_key=True, index=True)
    name = Column(String, nullable=True)
    status = Column(Integer,default=1)
    category = relationship("Categories",back_populates="sphera")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class ShopCategories(Base):
    __tablename__ = "shop_categories"
    id = Column(BIGINT, primary_key=True, index=True)
    shop_id = Column(BIGINT,ForeignKey('shops.id'))
    shop = relationship("Shops",back_populates="shopcategory")
    category_id = Column(BIGINT,ForeignKey('categories.id'))
    category = relationship("Categories",back_populates="categoryshop")
    status = Column(Integer,default=1)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())



class Categories(Base):
    __tablename__ = "categories"
    id = Column(BIGINT, primary_key=True, index=True)
    name_uz = Column(String, nullable=True)
    name_ru = Column(String, nullable=True)
    status = Column(Integer, default=1)
    sphera_id = Column(BIGINT,ForeignKey('spheras.id'))
    sphera = relationship("Spheras",back_populates="category")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    file = relationship("Files",back_populates="category")
    categoryshop = relationship("ShopCategories",back_populates="category")
    product = relationship("Products",back_populates="category")


class Colors(Base):
    __tablename__ = "colors"
    id = Column(BIGINT, primary_key=True, index=True)
    name_uz = Column(String, nullable=True)
    name_ru = Column(String, nullable=True)
    status = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    detail = relationship("Details",back_populates="color")

class Sizes(Base):
    __tablename__ = "sizes"
    id = Column(BIGINT, primary_key=True, index=True)
    name_uz = Column(String, nullable=True)
    name_ru = Column(String, nullable=True)
    status = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    detail = relationship("Details",back_populates="size")


class Products(Base):
    __tablename__ = "products"
    id = Column(BIGINT, primary_key=True, index=True)
    title = Column(String, nullable=True)
    comment = Column(String,nullable=True)
    price = Column(Float,nullable=True)
    status = Column(Integer, default=1)
    creator_id = Column(BIGINT, ForeignKey("users.id"))
    creator = relationship("Users",back_populates="product")
    shop_id = Column(BIGINT, ForeignKey("shops.id"))
    shop = relationship("Shops",back_populates="product")
    phone_number = Column(String,nullable=True)
    district_id = Column(BIGINT, ForeignKey("districts.id"))
    district = relationship("Districts",back_populates="product")
    currency_id = Column(BIGINT, ForeignKey("currencies.id"))
    currency = relationship("Currencies",back_populates="product")
    category_id = Column(BIGINT, ForeignKey("categories.id"))
    category = relationship("Categories",back_populates="product")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    detail = relationship("Details",back_populates="product")
    file = relationship("Files",back_populates="product")



class Details(Base):
    __tablename__ = "details"
    id = Column(BIGINT, primary_key=True, index=True)
    amount = Column(BIGINT,nullable=True)
    status = Column(Integer,nullable=True)
    product_id = Column(BIGINT, ForeignKey("products.id"))
    product = relationship("Products",back_populates="detail")
    color_id = Column(BIGINT, ForeignKey("colors.id"))
    color = relationship("Colors",back_populates="detail")
    size_id = Column(BIGINT, ForeignKey("sizes.id"))
    size = relationship("Sizes",back_populates="detail")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    file = relationship("Files",back_populates="detail")





class Files(Base):
    __tablename__ = "files"
    id = Column(BIGINT, primary_key=True, index=True)
    image = Column(String, nullable=True)
    status = Column(Integer, default=1)
    detail_id = Column(BIGINT,ForeignKey('details.id'),nullable=True)
    detail = relationship("Details",back_populates="file")
    shop_id = Column(BIGINT, ForeignKey("shops.id"),nullable=True)
    shop = relationship("Shops",back_populates="file")
    product_id = Column(BIGINT, ForeignKey("products.id"),nullable=True)
    product = relationship("Products",back_populates="file")
    category_id = Column(BIGINT, ForeignKey("categories.id"),nullable=True)
    category = relationship("Categories",back_populates="file")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
















