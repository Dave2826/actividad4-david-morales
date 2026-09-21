from sqlalchemy.orm import Session

from services.user_service import UserService
from security.jwt import create_access_token


class AuthService:

    @staticmethod
    def login(
        db: Session,
        email: str,
        password: str
    ):
        user = UserService.authenticate(
            db=db,
            email=email,
            password=password
        )

        token = create_access_token(
            user_id=user.id,
            email=user.email
        )

        return {
            "token": token,
            "token_type": "bearer",
            "user": user
        }