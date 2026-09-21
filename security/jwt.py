import os
from datetime import datetime, timedelta, timezone

import jwt


JWT_SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "dev-secret-key"
)

JWT_ALGORITHM = os.getenv(
    "JWT_ALGORITHM",
    "HS256"
)

JWT_EXPIRE_MINUTES = int(
    os.getenv(
        "JWT_EXPIRE_MINUTES",
        "60"
    )
)


def create_access_token(user_id: int, email: str) -> str:
    now = datetime.now(timezone.utc)

    expire = now + timedelta(
        minutes=JWT_EXPIRE_MINUTES
    )

    payload = {
        "sub": str(user_id),
        "email": email,
        "iat": now,
        "exp": expire
    }

    return jwt.encode(
        payload,
        JWT_SECRET_KEY,
        algorithm=JWT_ALGORITHM
    )


def decode_access_token(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM]
        )
    except jwt.PyJWTError:
        raise ValueError("Token inválido o expirado")