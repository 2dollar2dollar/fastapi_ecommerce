from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.reviews import Review as ReviewModel
from app.models.products import Product as ProductModel
from app.schemas import Review as ReviewSchema, ReviewCreate
from app.db_depends import get_async_db
from app.models.users import User as UserModel
from app.auth import get_current_buyer, get_current_admin, get_current_admin_or_buyer

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"]
)

@router.get("/", response_model=list[ReviewSchema])
async def get_all_reviews(db: AsyncSession = Depends(get_async_db)):
    """
    Возвращает список всех активных отзывов
    """
    reviews = await db.scalars(select(ReviewModel).where(ReviewModel.is_active == True))
    return reviews.all()

@router.get("/products/{product_id}", response_model=list[ReviewSchema])
async def get_product_reviews(product_id: int, db: AsyncSession = Depends(get_async_db)):
    """
    Возвращает список отзыва у указанного товара
    """
    # Проверяем, существует ли активный товар
    product = await db.scalars(
        select(ProductModel)
        .where(
            ProductModel.id == product_id,
            ProductModel.is_active == True))
    product = product.first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found or inactive")

    # Получаем активные отзывы товара
    reviews = await db.scalars(
        select(ReviewModel)
        .where(
            ReviewModel.product_id == product_id,
            ReviewModel.is_active == True))
    return reviews.all()

@router.post("/", response_model=ReviewSchema)
async def create_review(
    review: ReviewCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_buyer)
):
    """
    Создает новый отзыв о товаре, привязанный к текущему покупателю (только для 'buyer')
    """
    # Проверяем существование товара
    product_result = await db.scalars(
        select(ProductModel).where(ProductModel.id == review.product_id, ProductModel.is_active == True)
    )
    if not product_result.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found or inactive")

    # Проверямм, писал ли пользователь отзыв на этот товар ранее
    db_review = await db.scalars(
        select(ReviewModel)
        .where(
            ReviewModel.product_id == review.product_id,
            ReviewModel.user_id == current_user.id,
            ReviewModel.is_active == True)
    )
    if db_review.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have already reviewed this product")

    # Создание нового отзыва
    new_review = ReviewModel(**review.model_dump(), user_id = current_user.id)
    db.add(new_review)

    # Обновление рейтинга товара
    new_rating = await db.scalar(select(func.avg(ReviewModel.grade)).where(ReviewModel.product_id == review.product_id, ReviewModel.is_active == True))
    await db.execute(
        update(ProductModel).where(ProductModel.id == review.product_id).values(rating=new_rating)
    )
    await db.commit()
    await db.refresh(new_review)
    return new_review

@router.delete("/{review_id}", response_model=ReviewSchema)
async def delete_review(
    review_id: int,
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_admin_or_buyer)
):
    """
    Выполняет мягкое удаление отзыва, если пользователь - админ 'admin', либо этот пользователь - покупатель 'buyer' и это его отзыв
    - Админ может удалить ЛЮБОЙ отзыв
    - Покупатель может удалить ТОЛЬКО СВОЙ отзыв
    - Продавец НЕ МОЖЕТ удалять отзывы
    """
    review = await db.scalar(select(ReviewModel).where(ReviewModel.id == review_id, ReviewModel.is_active == True))
    if not review:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found or inactive")

    # Проверка, что отзыв принадлежит аутентифицированному покупателю
    if current_user.role == "buyer" and review.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only delete your own reviews")
    # Админ удаляет отзыв без проверок

    await db.execute(
        update(ReviewModel).where(ReviewModel.id == review_id).values(is_active=False)
    )

    # Обновление рейтинга товара
    new_rating = await db.scalar(select(func.avg(ReviewModel.grade)).where(ReviewModel.product_id == review.product_id, ReviewModel.is_active == True))
    await db.execute(
        update(ProductModel).where(ProductModel.id == review.product_id).values(rating=new_rating)
    )

    await db.commit()
    await db.refresh(review)
    return review