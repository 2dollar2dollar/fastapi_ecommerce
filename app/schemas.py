from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Optional
from decimal import Decimal
from datetime import datetime

class CategoryCreate(BaseModel):
    """
    Модель для создания и обновления категории.
    Используется в POST и PUT запросах.
    """
    name: str = Field(min_length=3, max_length=50,
                      description="Название категории (3-50 символов)")
    parent_id: Optional[int] = Field(None, description="ID родительской категории, если есть")


class Category(BaseModel):
    """
    Модель для ответа с данными категории.
    Используется в GET-запросах.
    """
    id: int = Field(description="Уникальный идентификатор категории")
    name: str = Field(description="Название категории")
    parent_id: Optional[int] = Field(None, description="ID родительской категории, если есть")
    is_active: bool = Field(description="Активность категории")

    model_config = ConfigDict(from_attributes=True)


class ProductCreate(BaseModel):
    """
    Модель для создания и обновления товара.
    Используется в POST и PUT запросах.
    """
    name: str = Field(min_length=3, max_length=100,
                      description="Название товара (3-100 символов)")
    description: Optional[str] = Field(None, max_length=500,
                                       description="Описание товара (до 500 символов)")
    price: Decimal = Field(gt=0, description="Цена товара (больше 0)", decimal_places=2)
    image_url: Optional[str] = Field(None, max_length=200, description="URL изображения товара")
    stock: int = Field(ge=0, description="Количество товара на складе (0 или больше)")
    category_id: int = Field(description="ID категории, к которой относится товар")
    rating: Decimal = Field(description="Рейтинг товара")


class Product(BaseModel):
    """
    Модель для ответа с данными товара.
    Используется в GET-запросах.
    """
    id: int = Field(description="Уникальный идентификатор товара")
    name: str = Field(description="Название товара")
    description: Optional[str] = Field(None, description="Описание товара")
    price: Decimal = Field(description="Цена товара в рублях", gt=0, decimal_places=2)
    image_url: Optional[str] = Field(None, description="URL изображения товара")
    stock: int = Field(description="Количество товара на складе")
    category_id: int = Field(description="ID категории")
    is_active: bool = Field(description="Активность товара")
    seller_id: int = Field(description="ID продавца")
    rating: Decimal = Field(None, description="Рейтинг товара")
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    email: EmailStr = Field(description="Email пользователя")
    password: str = Field(min_length=8, description="Пароль (минимум 8 символов)")
    role: str = Field(default="buyer", pattern="^(buyer|seller|admin)$", description="Роль: 'buyer' / 'seller' / 'admin'")


class User(BaseModel):
    id: int = Field(description="Уникальный идентификатор пользователя")
    email: EmailStr = Field("Почта пользователя")
    is_active: bool = Field("Активность пользователя")
    role: str = Field("Роль пользователя")
    model_config = ConfigDict(from_attributes=True)

class ReviewCreate(BaseModel):
    comment: str = Field(description="Комментарий пользователя")
    grade: int = Field(ge=1, le=5, description="Оценка товара пользователем")
    product_id: int = Field(description="ID товара, на который пользователь оставляет отзыв")

class Review(BaseModel):
    id: int = Field(description="Уникальный идентификатор отзыва")
    user_id: int = Field(description="ID покупателя")
    product_id: int = Field(description="ID товара")
    comment: str = Field(description="Текст отзыва")
    comment_date: datetime = Field(description="Время создания отзыва")
    grade: int = Field("Оценка товара")
    is_active: bool = Field(description="Активность отзыва")

    model_config = ConfigDict(from_attributes=True)