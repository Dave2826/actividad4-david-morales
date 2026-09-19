from typing import Optional

from sqlalchemy.orm import Session

from models.company import Company


class CompanyRepository:

    @staticmethod
    def get_all(db: Session, active_only: Optional[bool] = None):
        query = db.query(Company)

        if active_only is not None:
            query = query.filter(Company.is_active == active_only)

        return query.order_by(Company.id).all()

    @staticmethod
    def get_by_id(db: Session, company_id: int):
        return db.query(Company).filter(Company.id == company_id).first()

    @staticmethod
    def get_by_tax_id(db: Session, tax_id: str):
        return db.query(Company).filter(Company.tax_id == tax_id).first()

    @staticmethod
    def create(db: Session, company: Company):
        db.add(company)
        db.commit()
        db.refresh(company)
        return company

    @staticmethod
    def update(db: Session, company: Company):
        db.commit()
        db.refresh(company)
        return company

    @staticmethod
    def deactivate(db: Session, company: Company):
        company.is_active = False
        db.commit()
        db.refresh(company)
        return company
