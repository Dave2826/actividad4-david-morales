from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.company_user import CompanyUser
from repositories.company_repository import CompanyRepository
from repositories.company_user_repository import CompanyUserRepository
from security.auth import get_current_user
from services.user_service import UserService


class CompanyUserService:

    @staticmethod
    def create_admin(
        db: Session,
        company_id: int,
        name: str,
        email: str,
        password: str
    ):
        company = CompanyRepository.get_by_id(
            db,
            company_id
        )

        if not company:
            raise ValueError("La empresa no existe")

        if not company.is_active:
            raise ValueError("La empresa está inactiva")

        existing_admin = (
            CompanyUserRepository.get_admin_by_company(
                db,
                company_id
            )
        )

        if existing_admin:
            raise ValueError(
                "La empresa ya tiene un administrador principal"
            )

        user = UserService.create(
            db=db,
            name=name,
            email=email,
            password=password
        )

        company_user = CompanyUser(
            company_id=company_id,
            user_id=user.id,
            is_admin=True,
            is_active=True
        )

        try:
            return CompanyUserRepository.create(
                db,
                company_user
            )

        except IntegrityError:
            db.rollback()

            raise ValueError(
                "No se pudo crear el administrador principal"
            )

    @staticmethod
    def create_user(
        db: Session,
        company_id: int,
        name: str,
        email: str,
        password: str,
        token: str
    ):
        current_user = get_current_user(
            db,
            token
        )

        admin_relation = (
            CompanyUserRepository
            .get_admin_by_company_and_user(
                db,
                company_id,
                current_user.id
            )
        )

        if not admin_relation:
            raise ValueError(
                "El usuario no es administrador de esta empresa"
            )

        company = CompanyRepository.get_by_id(
            db,
            company_id
        )

        if not company:
            raise ValueError(
                "La empresa no existe"
            )

        if not company.is_active:
            raise ValueError(
                "La empresa está inactiva"
            )

        user = UserService.create(
            db=db,
            name=name,
            email=email,
            password=password
        )

        existing_relation = (
            CompanyUserRepository
            .get_by_company_and_user(
                db,
                company_id,
                user.id
            )
        )

        if existing_relation:
            raise ValueError(
                "El usuario ya pertenece a esta empresa"
            )

        company_user = CompanyUser(
            company_id=company_id,
            user_id=user.id,
            is_admin=False,
            is_active=True
        )

        try:
            return CompanyUserRepository.create(
                db,
                company_user
            )

        except IntegrityError:
            db.rollback()

            raise ValueError(
                "No se pudo registrar el usuario en la empresa"
            )