import strawberry

from sqlalchemy.orm import Session

from database.database import SessionLocal

from graphql_api.types import (
    CompanyType,
    CompanyUserType
)

from services.company_service import CompanyService
from services.company_user_service import CompanyUserService


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


def to_company_user_type(company_user):
    return CompanyUserType(
        id=company_user.id,
        company_id=company_user.company_id,
        user_id=company_user.user_id,
        is_admin=company_user.is_admin,
        is_active=company_user.is_active,
        joined_at=company_user.joined_at,
    )


@strawberry.type
class Query:

    @strawberry.field
    def companies(
        self,
        active_only: bool | None = None
    ) -> list[CompanyType]:

        db: Session = SessionLocal()

        try:
            companies = CompanyService.get_all(
                db,
                active_only
            )

            return [
                to_company_type(company)
                for company in companies
            ]

        finally:
            db.close()

    @strawberry.field
    def company(
        self,
        id: int
    ) -> CompanyType | None:

        db: Session = SessionLocal()

        try:
            company = CompanyService.get_by_id(
                db,
                id
            )

            return (
                to_company_type(company)
                if company
                else None
            )

        finally:
            db.close()

    @strawberry.field
    def company_users(
        self,
        company_id: int
    ) -> list[CompanyUserType]:

        db: Session = SessionLocal()

        try:
            company_users = CompanyUserService.get_by_company(
                db,
                company_id
            )

            return [
                to_company_user_type(company_user)
                for company_user in company_users
            ]

        except ValueError as error:
            raise ValueError(str(error))

        finally:
            db.close()