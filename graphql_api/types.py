import strawberry
from datetime import datetime
from typing import Optional


@strawberry.type
class CompanyType:
    id: int
    name: str
    legal_name: Optional[str]
    tax_id: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime


@strawberry.input
class CreateCompanyInput:
    name: str
    legal_name: Optional[str] = None
    tax_id: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None


@strawberry.input
class UpdateCompanyInput:
    id: int
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


@strawberry.type
class AuthUserType:
    id: int
    name: str
    email: str


@strawberry.type
class AuthPayloadType:
    token: str
    token_type: str
    user: AuthUserType


@strawberry.input
class CreateCompanyAdminInput:
    company_id: int
    name: str
    email: str
    password: str


@strawberry.type
class CompanyUserType:
    id: int
    company_id: int
    user_id: int
    is_admin: bool
    is_active: bool
    joined_at: datetime
    
@strawberry.input
class CreateCompanyUserInput:
    company_id: int
    name: str
    email: str
    password: str