from typing import Optional

from sqlalchemy.orm import Session

from models.company import Company
from repositories.company_repository import CompanyRepository


class CompanyService:

    @staticmethod
    def get_all(db: Session, active_only: Optional[bool] = None):
        return CompanyRepository.get_all(db, active_only)

    @staticmethod
    def get_by_id(db: Session, company_id: int):
        return CompanyRepository.get_by_id(db, company_id)

    @staticmethod
    def create(db: Session, name: str, legal_name: Optional[str] = None, tax_id: Optional[str] = None, email: Optional[str] = None, phone: Optional[str] = None):
        if not name or not name.strip():
            raise ValueError("El nombre de la empresa es obligatorio")

        if tax_id:
            existing_company = CompanyRepository.get_by_tax_id(db, tax_id.strip())
            if existing_company:
                raise ValueError("El tax_id ya pertenece a otra empresa")

        company = Company(
            name=name.strip(),
            legal_name=legal_name.strip() if legal_name else None,
            tax_id=tax_id.strip() if tax_id else None,
            email=email.strip() if email else None,
            phone=phone.strip() if phone else None,
            is_active=True
        )

        return CompanyRepository.create(db, company)

    @staticmethod
    def update(db: Session, company_id: int, name: Optional[str] = None, legal_name: Optional[str] = None, tax_id: Optional[str] = None, email: Optional[str] = None, phone: Optional[str] = None, is_active: Optional[bool] = None):
        company = CompanyRepository.get_by_id(db, company_id)

        if not company:
            raise ValueError("La empresa no existe")

        if name is not None:
            if not name.strip():
                raise ValueError("El nombre de la empresa no puede estar vacío")
            company.name = name.strip()

        if tax_id is not None and tax_id != company.tax_id:
            existing_company = CompanyRepository.get_by_tax_id(db, tax_id.strip())
            if existing_company and existing_company.id != company.id:
                raise ValueError("El tax_id ya pertenece a otra empresa")
            company.tax_id = tax_id.strip() or None

        if legal_name is not None:
            company.legal_name = legal_name.strip() or None

        if email is not None:
            company.email = email.strip() or None

        if phone is not None:
            company.phone = phone.strip() or None

        if is_active is not None:
            company.is_active = is_active

        return CompanyRepository.update(db, company)

    @staticmethod
    def deactivate(db: Session, company_id: int):
        company = CompanyRepository.get_by_id(db, company_id)

        if not company:
            raise ValueError("La empresa no existe")

        return CompanyRepository.deactivate(db, company)
