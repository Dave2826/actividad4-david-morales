import strawberry
from datetime import datetime
from typing import Optional

@strawberry.scalar(
    serialize=lambda value: value.isoformat(),
    parse_value=lambda value: datetime.fromisoformat(value)
)
def Time(value: datetime) -> datetime:
    return value


@strawberry.type(name="Company")
class CompanyType:
    id: strawberry.ID
    name: str
    legal_name: Optional[str]
    tax_id: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    is_active: bool
    created_at: Time  
    updated_at: Time


@strawberry.type(name="User")
class UserType:
    id: strawberry.ID
    name: str
    email: str
    email_verified: bool
    is_active: bool
    created_at: Time
    updated_at: Time


@strawberry.type(name="AuthUser")
class AuthUserType:
    id: strawberry.ID
    name: str
    email: str


@strawberry.type(name="AuthPayload")
class AuthPayloadType:
    token: str
    token_type: str
    user: AuthUserType


@strawberry.type(name="CompanyUser")
class CompanyUserType:
    id: strawberry.ID
    company_id: strawberry.ID
    user_id: strawberry.ID
    is_admin: bool
    is_active: bool
    joined_at: Time
    company: CompanyType
    user: UserType


@strawberry.input
class CreateCompanyInput:
    name: str
    legal_name: Optional[str] = None
    tax_id: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


@strawberry.input
class UpdateCompanyInput:
    id: strawberry.ID
    name: Optional[str] = None
    legal_name: Optional[str] = None
    tax_id: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None


@strawberry.input
class LoginInput:
    email: str
    password: str


@strawberry.input
class CreateCompanyAdminInput:
    company_id: strawberry.ID
    name: str
    email: str
    password: str


@strawberry.input
class CreateCompanyUserInput:
    company_id: strawberry.ID
    name: str
    email: str
    password: str