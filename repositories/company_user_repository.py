from sqlalchemy.orm import Session

from models.company_user import CompanyUser


class CompanyUserRepository:

    @staticmethod
    def get_by_id(
        db: Session,
        company_user_id: int
    ):
        return (
            db.query(CompanyUser)
            .filter(CompanyUser.id == company_user_id)
            .first()
        )

    @staticmethod
    def get_by_company_and_user(
        db: Session,
        company_id: int,
        user_id: int
    ):
        return (
            db.query(CompanyUser)
            .filter(
                CompanyUser.company_id == company_id,
                CompanyUser.user_id == user_id
            )
            .first()
        )

    @staticmethod
    def get_admin_by_company(
        db: Session,
        company_id: int
    ):
        return (
            db.query(CompanyUser)
            .filter(
                CompanyUser.company_id == company_id,
                CompanyUser.is_admin.is_(True),
                CompanyUser.is_active.is_(True)
            )
            .first()
        )

    @staticmethod
    def get_admin_by_company_and_user(
        db: Session,
        company_id: int,
        user_id: int
    ):
        return (
            db.query(CompanyUser)
            .filter(
                CompanyUser.company_id == company_id,
                CompanyUser.user_id == user_id,
                CompanyUser.is_admin.is_(True),
                CompanyUser.is_active.is_(True)
            )
            .first()
        )

    @staticmethod
    def get_by_company(
        db: Session,
        company_id: int
    ):
        return (
            db.query(CompanyUser)
            .filter(
                CompanyUser.company_id == company_id
            )
            .order_by(CompanyUser.id)
            .all()
        )

    @staticmethod
    def create(
        db: Session,
        company_user: CompanyUser
    ):
        db.add(company_user)
        db.commit()
        db.refresh(company_user)
        return company_user

    @staticmethod
    def update(
        db: Session,
        company_user: CompanyUser
    ):
        db.commit()
        db.refresh(company_user)
        return company_user