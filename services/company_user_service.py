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

        existing_admin = CompanyUserRepository.get_admin_by_company(
            db,
            company_id
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

        company = CompanyRepository.get_by_id(
            db,
            company_id
        )

        if not company:
            raise ValueError("La empresa no existe")

        if not company.is_active:
            raise ValueError("La empresa está inactiva")

        admin_relation = (
            CompanyUserRepository.get_admin_by_company_and_user(
                db,
                company_id,
                current_user.id
            )
        )

        if not admin_relation:
            raise ValueError(
                "El usuario no es administrador de esta empresa"
            )

        user = UserService.create(
            db=db,
            name=name,
            email=email,
            password=password
        )

        existing_relation = (
            CompanyUserRepository.get_by_company_and_user(
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

    @staticmethod
    def get_by_company(
        db: Session,
        company_id: int
    ):
        company = CompanyRepository.get_by_id(
            db,
            company_id
        )

        if not company:
            raise ValueError("La empresa no existe")

        return CompanyUserRepository.get_by_company(
            db,
            company_id
        )

    @staticmethod
    def deactivate_user(
        db: Session,
        company_user_id: int,
        token: str
    ):
        current_user = get_current_user(
            db,
            token
        )

        company_user = CompanyUserRepository.get_by_id(
            db,
            company_user_id
        )

        if not company_user:
            raise ValueError(
                "La relación empresa-usuario no existe"
            )

        admin_relation = (
            CompanyUserRepository.get_admin_by_company_and_user(
                db,
                company_user.company_id,
                current_user.id
            )
        )

        if not admin_relation:
            raise ValueError(
                "El usuario no es administrador de esta empresa"
            )

        if company_user.is_admin:
            raise ValueError(
                "No se puede desactivar al administrador principal"
            )

        if not company_user.is_active:
            raise ValueError(
                "El usuario ya está inactivo"
            )

        company_user.is_active = False

        return CompanyUserRepository.update(
            db,
            company_user
        )