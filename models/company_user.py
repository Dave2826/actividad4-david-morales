from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base


class CompanyUser(Base):
    __tablename__ = "company_users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    company_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("companies.id"),
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    is_admin: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True
    )

    joined_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    company = relationship(
        "Company",
        back_populates="company_users"
    )

    user = relationship(
        "User",
        back_populates="company_users"
    )

    __table_args__ = (
        UniqueConstraint(
            "company_id",
            "user_id",
            name="uq_company_user"
        ),
    )