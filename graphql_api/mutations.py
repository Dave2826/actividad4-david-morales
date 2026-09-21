import strawberry
from sqlalchemy.orm import Session

from database.database import SessionLocal
from graphql_api.types import (
    AuthPayloadType,
    AuthUserType,
    CompanyType,
    CompanyUserType,
    CreateCompanyAdminInput,
    CreateCompanyInput,
    LoginInput,
    UpdateCompanyInput,
)
from services.auth_service import AuthService
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
class Mutation:

    @strawberry.mutation
    def create_company(
        self,
        input: CreateCompanyInput
    ) -> CompanyType:
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
    def update_company(
        self,
        input: UpdateCompanyInput
    ) -> CompanyType:
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
    def deactivate_company(
        self,
        id: int
    ) -> CompanyType:
        db: Session = SessionLocal()

        try:
            company = CompanyService.deactivate(
                db,
                id
            )

            return to_company_type(company)

        except ValueError as error:
            raise ValueError(str(error))

        finally:
            db.close()

    @strawberry.mutation
    def login(
        self,
        input: LoginInput
    ) -> AuthPayloadType:
        db: Session = SessionLocal()

        try:
            result = AuthService.login(
                db=db,
                email=input.email,
                password=input.password
            )

            user = result["user"]

            return AuthPayloadType(
                token=result["token"],
                token_type=result["token_type"],
                user=AuthUserType(
                    id=user.id,
                    name=user.name,
                    email=user.email
                )
            )

        except ValueError as error:
            raise ValueError(str(error))

        finally:
            db.close()

    @strawberry.mutation
    def create_company_admin(
        self,
        input: CreateCompanyAdminInput
    ) -> CompanyUserType:
        db: Session = SessionLocal()

        try:
            company_user = CompanyUserService.create_admin(
                db=db,
                company_id=input.company_id,
                name=input.name,
                email=input.email,
                password=input.password
            )

            return to_company_user_type(company_user)

        except ValueError as error:
            raise ValueError(str(error))

        finally:
            db.close()