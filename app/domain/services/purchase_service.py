from sqlalchemy.orm import Session
from app.infrastructure.database.models.purchase import Purchase
from app.infrastructure.database.models.category import Category
from app.domain.models.purchase import PurchaseCreate, PurchaseRead
from fastapi import HTTPException, status
from app.infrastructure.database.models.user import User

class PurchaseService:
    def __init__(self, db: Session):
        self.db = db

    def create_purchase(self, current_user: User, purchase_data: PurchaseCreate) -> PurchaseRead:
        category = self.db.query(Category).filter(Category.id == purchase_data.category_id, Category.user_id == current_user.id).first()
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found or doesn't belong to user")

        if category.remaining_amount < purchase_data.amount:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough budget in category")

        category.remaining_amount -= purchase_data.amount
        self.db.commit()
        self.db.refresh(category)

        new_purchase = Purchase(
            user_id=current_user.id,
            category_id=purchase_data.category_id,
            description=purchase_data.description,
            amount=purchase_data.amount
        )

        self.db.add(new_purchase)
        self.db.commit()
        self.db.refresh(new_purchase)

        return PurchaseRead(
            id=new_purchase.id,
            description=new_purchase.description,
            amount=new_purchase.amount,
            purchased_at=str(new_purchase.purchased_at)
        )

    def get_purchase_by_id(self, purchase_id: int, current_user: User) -> PurchaseRead:
        purchase = self.db.query(Purchase).filter(Purchase.id == purchase_id, Purchase.user_id == current_user.id).first()
        if not purchase:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase not found")

        return PurchaseRead(
            id=purchase.id,
            description=purchase.description,
            amount=purchase.amount,
            purchased_at=str(purchase.purchased_at)
        )

    def get_user_purchases(self, current_user: User) -> list[PurchaseRead]:
        purchases = self.db.query(Purchase).filter(Purchase.user_id == current_user.id).all()

        return [
            PurchaseRead(
                id=purchase.id,
                description=purchase.description,
                amount=purchase.amount,
                purchased_at=str(purchase.purchased_at)
            ) for purchase in purchases
        ]

    def update_purchase(self, purchase_id: int, purchase_data: PurchaseCreate, current_user: User) -> PurchaseRead:
        purchase = self.db.query(Purchase).filter(Purchase.id == purchase_id, Purchase.user_id == current_user.id).first()
        if not purchase:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase not found")

        category = self.db.query(Category).filter(Category.id == purchase_data.category_id, Category.user_id == current_user.id).first()
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found or doesn't belong to user")

        category.remaining_amount -= purchase_data.amount
        self.db.commit()
        self.db.refresh(category)

        purchase.category_id = purchase_data.category_id
        purchase.description = purchase_data.description
        purchase.amount = purchase_data.amount

        self.db.commit()
        self.db.refresh(purchase)

        return PurchaseRead(
            id=purchase.id,
            description=purchase.description,
            amount=purchase.amount,
            purchased_at=str(purchase.purchased_at)
        )

    def delete_purchase(self, purchase_id: int, current_user: User):
        purchase = self.db.query(Purchase).filter(Purchase.id == purchase_id, Purchase.user_id == current_user.id).first()
        if not purchase:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Purchase not found")

        category = self.db.query(Category).filter(Category.id == purchase.category_id).first()
        if category:
            category.remaining_amount += purchase.amount

        self.db.delete(purchase)
        self.db.commit()

        return {"detail": "Purchase deleted successfully"}
