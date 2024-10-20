from sqlalchemy.orm import Session
from app.infrastructure.database.models.category import Category
from app.domain.models.category import CategoryCreate, CategoryRead
from fastapi import HTTPException, status
from app.infrastructure.database.models.user import User

class CategoryService:
    def __init__(self, db: Session):
        self.db = db

    def create_category(self, current_user: User, category_data: CategoryCreate) -> CategoryRead:
        new_category = Category(
            user_id=current_user.id,
            name=category_data.name,
            planned_amount=category_data.planned_amount,
            remaining_amount=category_data.remaining_amount,
            period=category_data.period
        )

        self.db.add(new_category)
        self.db.commit()
        self.db.refresh(new_category)

        return CategoryRead(
            id=new_category.id,
            name=new_category.name,
            planned_amount=new_category.planned_amount,
            remaining_amount=new_category.remaining_amount,
            period=new_category.period
        )

    def get_category_by_id(self, category_id: int, current_user: User) -> CategoryRead:
        category = self.db.query(Category).filter(Category.id == category_id, Category.user_id == current_user.id).first()
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

        return CategoryRead(
            id=category.id,
            name=category.name,
            planned_amount=category.planned_amount,
            remaining_amount=category.remaining_amount,
            period=category.period
        )

    def get_user_categories(self, current_user: User) -> list[CategoryRead]:
        categories = self.db.query(Category).filter(Category.user_id == current_user.id).all()

        return [
            CategoryRead(
                id=category.id,
                name=category.name,
                planned_amount=category.planned_amount,
                remaining_amount=category.remaining_amount,
                period=category.period
            ) for category in categories
        ]

    def update_category(self, category_id: int, category_data: CategoryCreate, current_user: User) -> CategoryRead:
        category = self.db.query(Category).filter(Category.id == category_id, Category.user_id == current_user.id).first()
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

        category.name = category_data.name
        category.planned_amount = category_data.planned_amount
        category.remaining_amount = category_data.remaining_amount
        category.period = category_data.period

        self.db.commit()
        self.db.refresh(category)

        return CategoryRead(
            id=category.id,
            name=category.name,
            planned_amount=category.planned_amount,
            remaining_amount=category.remaining_amount,
            period=category.period
        )

    def delete_category(self, category_id: int, current_user: User):
        category = self.db.query(Category).filter(Category.id == category_id, Category.user_id == current_user.id).first()
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

        self.db.delete(category)
        self.db.commit()

        return {"detail": "Category deleted successfully"}

    def reset_monthly_categories(self):
        categories = self.db.query(Category).filter(Category.period == "monthly").all()
        for category in categories:
            category.remaining_amount = category.planned_amount
        self.db.commit()

    def reset_weekly_categories(self):
        categories = self.db.query(Category).filter(Category.period == "weekly").all()
        for category in categories:
            category.remaining_amount = category.planned_amount
        self.db.commit()
