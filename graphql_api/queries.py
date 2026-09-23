import strawberry

from sqlalchemy.orm import Session

from database.database import SessionLocal

from graphql_api.types import (
    CompanyType,
    CompanyUserType,
    UserType
)

from services.company_service import CompanyService
from services.company_user_service import CompanyUserService


def to_company_type(company):
    return CompanyType(
        id=strawberry.ID(str(company.id)),
        name=company.name,
        legal_name=company.legal_name,
        tax_id=company.tax_id,
        email=company.email,
        phone=company.phone,
        is_active=company.is_active,
        created_at=company.created_at,
        updated_at=company.updated_at,
    )


def to_user_type(user):
    return UserType(
        id=strawberry.ID(str(user.id)),
        name=user.name,
        email=user.email,
        email_verified=user.email_verified,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


def to_company_user_type(company_user):
    return CompanyUserType(
        id=strawberry.ID(str(company_user.id)),
        company_id=strawberry.ID(str(company_user.company_id)),
        user_id=strawberry.ID(str(company_user.user_id)),
        is_admin=company_user.is_admin,
        is_active=company_user.is_active,
        joined_at=company_user.joined_at,
        company=to_company_type(company_user.company),
        user=to_user_type(company_user.user),
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
        id: strawberry.ID
    ) -> CompanyType | None:

        db: Session = SessionLocal()

        try:
            company = CompanyService.get_by_id(
                db,
                int(id)
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
        company_id: strawberry.ID
    ) -> list[CompanyUserType]:

        db: Session = SessionLocal()

        try:
            company_users = CompanyUserService.get_by_company(
                db,
                int(company_id)
            )

            return [
                to_company_user_type(company_user)
                for company_user in company_users
            ]

        except ValueError as error:
            raise ValueError(str(error))

        finally:
            db.close()