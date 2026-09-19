import strawberry
from sqlalchemy.orm import Session

from database.database import SessionLocal
from graphql_api.types import CompanyType
from services.company_service import CompanyService


def to_company_type(company):
    return CompanyType(
        id=company.id,
        name=company.name,
        legal_name=company.legal_name,
        tax_id=company.tax_id,
        email=company.email,
        phone=company.phone,
        is_active=company.is_active,
        created_at=company.created_at,
        updated_at=company.updated_at,
    )


@strawberry.type
class Query:

    @strawberry.field
    def companies(self, active_only: bool | None = None) -> list[CompanyType]:
        db: Session = SessionLocal()
        try:
            companies = CompanyService.get_all(db, active_only)
            return [to_company_type(company) for company in companies]
        finally:
            db.close()

    @strawberry.field
    def company(self, id: int) -> CompanyType | None:
        db: Session = SessionLocal()
        try:
            company = CompanyService.get_by_id(db, id)
            return to_company_type(company) if company else None
        finally:
            db.close()