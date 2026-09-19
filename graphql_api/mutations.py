import strawberry
from sqlalchemy.orm import Session

from database.database import SessionLocal
from graphql_api.types import CompanyType, CreateCompanyInput, UpdateCompanyInput
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
class Mutation:

    @strawberry.mutation
    def create_company(self, input: CreateCompanyInput) -> CompanyType:
        db: Session = SessionLocal()
        try:
            company = CompanyService.create(
                db=db,
                name=input.name,
                legal_name=input.legal_name,
                tax_id=input.tax_id,
                email=input.email,
                phone=input.phone,
            )
            return to_company_type(company)
        except ValueError as error:
            raise ValueError(str(error))
        finally:
            db.close()

    @strawberry.mutation
    def update_company(self, input: UpdateCompanyInput) -> CompanyType:
        db: Session = SessionLocal()
        try:
            company = CompanyService.update(
                db=db,
                company_id=input.id,
                name=input.name,
                legal_name=input.legal_name,
                tax_id=input.tax_id,
                email=input.email,
                phone=input.phone,
                is_active=input.is_active,
            )
            return to_company_type(company)
        except ValueError as error:
            raise ValueError(str(error))
        finally:
            db.close()

    @strawberry.mutation
    def deactivate_company(self, id: int) -> CompanyType:
        db: Session = SessionLocal()
        try:
            company = CompanyService.deactivate(db, id)
            return to_company_type(company)
        except ValueError as error:
            raise ValueError(str(error))
        finally:
            db.close()