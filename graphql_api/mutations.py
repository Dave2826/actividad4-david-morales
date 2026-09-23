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
    CreateCompanyUserInput,
    LoginInput,
    UpdateCompanyInput,
)

from services.auth_service import AuthService
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


def to_auth_user_type(user):
    return AuthUserType(
        id=strawberry.ID(str(user.id)),
        name=user.name,
        email=user.email,
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
        user=graphql_user_type(company_user.user),
    )


def graphql_user_type(user):
    from graphql_api.types import UserType

    return UserType(
        id=strawberry.ID(str(user.id)),
        name=user.name,
        email=user.email,
        email_verified=user.email_verified,
        is_active=user.is_active,
        created_at=user.created_at,
        updated_at=user.updated_at,
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
                company_id=int(input.id),
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
        id: strawberry.ID
    ) -> CompanyType:

        db: Session = SessionLocal()

        try:
            company = CompanyService.deactivate(
                db,
                int(id)
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
                user=to_auth_user_type(user)
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
                company_id=int(input.company_id),
                name=input.name,
                email=input.email,
                password=input.password
            )

            return to_company_user_type(company_user)

        except ValueError as error:
            raise ValueError(str(error))

        finally:
            db.close()

    @strawberry.mutation
    def create_company_user(
        self,
        input: CreateCompanyUserInput,
        info: strawberry.Info
    ) -> CompanyUserType:

        db: Session = SessionLocal()

        try:
            authorization = info.context.get(
                "request"
            ).headers.get(
                "Authorization"
            )

            if not authorization:
                raise ValueError(
                    "Se requiere autenticación"
                )

            if not authorization.startswith("Bearer "):
                raise ValueError(
                    "Formato de autorización inválido"
                )

            token = authorization.replace(
                "Bearer ",
                "",
                1
            ).strip()

            if not token:
                raise ValueError(
                    "Se requiere un token válido"
                )

            company_user = CompanyUserService.create_user(
                db=db,
                company_id=int(input.company_id),
                name=input.name,
                email=input.email,
                password=input.password,
                token=token
            )

            return to_company_user_type(company_user)

        except ValueError as error:
            raise ValueError(str(error))

        finally:
            db.close()

    @strawberry.mutation
    def deactivate_company_user(
        self,
        id: strawberry.ID,
        info: strawberry.Info
    ) -> CompanyUserType:

        db: Session = SessionLocal()

        try:
            authorization = info.context.get(
                "request"
            ).headers.get(
                "Authorization"
            )

            if not authorization:
                raise ValueError(
                    "Se requiere autenticación"
                )

            if not authorization.startswith("Bearer "):
                raise ValueError(
                    "Formato de autorización inválido"
                )

            token = authorization.replace(
                "Bearer ",
                "",
                1
            ).strip()

            if not token:
                raise ValueError(
                    "Se requiere un token válido"
                )

            company_user = CompanyUserService.deactivate_user(
                db=db,
                company_user_id=int(id),
                token=token
            )

            return to_company_user_type(company_user)

        except ValueError as error:
            raise ValueError(str(error))

        finally:
            db.close()