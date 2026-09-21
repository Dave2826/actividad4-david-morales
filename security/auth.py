from sqlalchemy.orm import Session

from repositories.user_repository import UserRepository
from security.jwt import decode_access_token


def get_current_user(
    db: Session,
    token: str
):
    payload = decode_access_token(token)

    user_id = payload.get("sub")

    if not user_id:
        raise ValueError("Token inválido")

    user = UserRepository.get_by_id(
        db,
        int(user_id)
    )

    if not user:
        raise ValueError("Usuario no encontrado")

    if not user.is_active:
        raise ValueError("El usuario está inactivo")

    return user