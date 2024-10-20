from sqlalchemy.orm import Session
from app.infrastructure.database.models.installment import Installment
from app.infrastructure.database.models.category import Category
from app.domain.models.installment import InstallmentCreate, InstallmentRead
from fastapi import HTTPException, status
from app.infrastructure.database.models.user import User

class InstallmentService:
    def __init__(self, db: Session):
        self.db = db

    def create_installment(self, current_user: User, installment_data: InstallmentCreate) -> InstallmentRead:
        if installment_data.category_id:
            category = self.db.query(Category).filter(Category.id == installment_data.category_id, Category.user_id == current_user.id).first()
            if not category:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found or doesn't belong to user")
            
            if category.remaining_amount < installment_data.installment_amount:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough budget in category")
            
            category.remaining_amount -= installment_data.installment_amount
            self.db.commit()
            self.db.refresh(category)

        new_installment = Installment(
            user_id=current_user.id,
            category_id=installment_data.category_id,
            total_amount=installment_data.total_amount,
            installment_amount=installment_data.installment_amount,
            total_installments=installment_data.total_installments,
            description=installment_data.description
        )
        
        self.db.add(new_installment)
        self.db.commit()
        self.db.refresh(new_installment)

        return InstallmentRead(
            id=new_installment.id,
            total_amount=new_installment.total_amount,
            installment_amount=new_installment.installment_amount,
            total_installments=new_installment.total_installments,
            current_installment=new_installment.current_installment,
            description=new_installment.description,
            purchased_at=str(new_installment.purchased_at)
        )

    def get_installment_by_id(self, installment_id: int, current_user: User) -> InstallmentRead:
        installment = self.db.query(Installment).filter(Installment.id == installment_id, Installment.user_id == current_user.id).first()
        if not installment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Installment not found")

        return InstallmentRead(
            id=installment.id,
            total_amount=installment.total_amount,
            installment_amount=installment.installment_amount,
            total_installments=installment.total_installments,
            current_installment=installment.current_installment,
            description=installment.description,
            purchased_at=str(installment.purchased_at)
        )

    def get_user_installments(self, current_user: User) -> list[InstallmentRead]:
        installments = self.db.query(Installment).filter(Installment.user_id == current_user.id).all()
        return [
            InstallmentRead(
                id=installment.id,
                total_amount=installment.total_amount,
                installment_amount=installment.installment_amount,
                total_installments=installment.total_installments,
                current_installment=installment.current_installment,
                description=installment.description,
                purchased_at=str(installment.purchased_at)
            ) for installment in installments
        ]

    def update_installment(self, installment_id: int, installment_data: InstallmentCreate, current_user: User) -> InstallmentRead:
        installment = self.db.query(Installment).filter(Installment.id == installment_id, Installment.user_id == current_user.id).first()
        if not installment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Installment not found")

        if installment_data.category_id:
            category = self.db.query(Category).filter(Category.id == installment_data.category_id, Category.user_id == current_user.id).first()
            if not category:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found or doesn't belong to user")

            category.remaining_amount -= installment_data.installment_amount
            self.db.commit()
            self.db.refresh(category)

        installment.category_id = installment_data.category_id
        installment.total_amount = installment_data.total_amount
        installment.installment_amount = installment_data.installment_amount
        installment.total_installments = installment_data.total_installments
        installment.description = installment_data.description

        self.db.commit()
        self.db.refresh(installment)

        return InstallmentRead(
            id=installment.id,
            total_amount=installment.total_amount,
            installment_amount=installment.installment_amount,
            total_installments=installment.total_installments,
            current_installment=installment.current_installment,
            description=installment.description,
            purchased_at=str(installment.purchased_at)
        )

    def pay_installment(self, installment_id: int, current_user: User):
        installment = self.db.query(Installment).filter(Installment.id == installment_id, Installment.user_id == current_user.id).first()
        if not installment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Installment not found")

        if installment.current_installment >= installment.total_installments:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="All installments are already paid")

        installment.current_installment += 1

        if installment.current_installment == installment.total_installments:
            self.db.delete(installment)
            self.db.commit()
            return {"detail": "Installment fully paid and deleted"}

        self.db.commit()
        self.db.refresh(installment)

        return InstallmentRead(
            id=installment.id,
            total_amount=installment.total_amount,
            installment_amount=installment.installment_amount,
            total_installments=installment.total_installments,
            current_installment=installment.current_installment,
            description=installment.description,
            purchased_at=str(installment.purchased_at)
        )

    def delete_installment(self, installment_id: int, current_user: User):
        installment = self.db.query(Installment).filter(Installment.id == installment_id, Installment.user_id == current_user.id).first()
        if not installment:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Installment not found")

        if installment.category_id:
            category = self.db.query(Category).filter(Category.id == installment.category_id).first()
            if category:
                category.remaining_amount += installment.installment_amount

        self.db.delete(installment)
        self.db.commit()

        return {"detail": "Installment deleted successfully"}
