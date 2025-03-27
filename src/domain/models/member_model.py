from uuid import UUID

from pydantic import BaseModel, EmailStr


class MemberModel(BaseModel):
    id: UUID
    name: str
    email: EmailStr

    model_config = {
        "from_attributes": True
    }


class CreateMemberModel(BaseModel):
    name: str
    email: EmailStr


class UpdateMemberModel(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
