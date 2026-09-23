from sqlalchemy.orm import Session
from pwdlib import PasswordHash

from models.user import User
from repositories.user_repository import UserRepository
from email_validator import EmailNotValidError, validate_email


password_hash = PasswordHash.recommended()


class UserService:

    @staticmethod
    def normalize_email(email: str) -> str:
        return email.strip().lower()

    @staticmethod
    def hash_password(password: str) -> str:
        if not password or len(password) < 8:
            raise ValueError(
                "La contraseña debe tener al menos 8 caracteres"
            )

        return password_hash.hash(password)

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return password_hash.verify(password, hashed_password)

    @staticmethod
    def create(
        db: Session,
        name: str,
        email: str,
        password: str
    ):
        if not name or not name.strip():
            raise ValueError("El nombre del usuario es obligatorio")

        if not email or not email.strip():
            raise ValueError("El correo electrónico es obligatorio")

        email = UserService.normalize_email(email)
        try:
            email = validate_email(email, check_deliverability=False).normalized
        except EmailNotValidError:
            raise ValueError("El correo electrónico no es válido")

        existing_user = UserRepository.get_by_email(db, email)

        if existing_user:
            raise ValueError(
                "El correo electrónico ya está registrado"
            )

        hashed_password = UserService.hash_password(password)

        user = User(
            name=name.strip(),
            email=email,
            password_hash=hashed_password,
            email_verified=False,
            is_active=True
        )

        return UserRepository.create(db, user)

    @staticmethod
    def get_by_email(db: Session, email: str):
        email = UserService.normalize_email(email)
        return UserRepository.get_by_email(db, email)

    @staticmethod
    def get_by_id(db: Session, user_id: int):
        return UserRepository.get_by_id(db, user_id)

    @staticmethod
    def authenticate(
        db: Session,
        email: str,
        password: str
    ):
        email = UserService.normalize_email(email)

        user = UserRepository.get_by_email(db, email)

        if not user:
            raise ValueError("Credenciales incorrectas")

        if not user.is_active:
            raise ValueError("El usuario está inactivo")

        if not UserService.verify_password(
            password,
            user.password_hash
        ):
            raise ValueError("Credenciales incorrectas")

        return user