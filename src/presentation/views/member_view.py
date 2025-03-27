import uuid
from typing import List

from fastapi import APIRouter, HTTPException

from src.application.members_services import MembersService
from src.domain.members_entity import MemberEntity
from src.domain.models.member_model import (CreateMemberModel, MemberModel,
                                            UpdateMemberModel)

router = APIRouter()
service = MembersService()


@router.get("/", response_model=List[MemberModel])
def get_all_members():
    members = service.get_all() or []

    try:
        return [member.to_model() for member in members]
    except Exception as e:
        print("DEBUG to_model() failed:", e)
        raise HTTPException(
            status_code=500, detail="Failed to serialize members")


@router.get("/{member_id}", response_model=MemberModel)
def get_member(member_id: str):
    try:
        member_uuid = uuid.UUID(member_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID")

    member = service.get_by_id(member_uuid)
    if member is None:
        raise HTTPException(status_code=404, detail="Member not found")

    try:
        return member.to_model()
    except Exception as e:
        print("DEBUG single to_model() failed:", e)
        raise HTTPException(
            status_code=500, detail="Failed to serialize member")


@router.post("/", response_model=MemberModel, status_code=201)
def create_member(member_data: CreateMemberModel):
    member = MemberEntity(name=member_data.name, email=member_data.email)
    result = service.add(member)
    if not result:
        raise HTTPException(status_code=500, detail="Error adding member")

    try:
        return result.to_model()
    except Exception as e:
        print("DEBUG create to_model() failed:", e)
        raise HTTPException(
            status_code=500, detail="Failed to serialize created member")


@router.put("/{member_id}", response_model=dict)
def update_member(member_id: str, update_data: UpdateMemberModel):
    update_dict = update_data.dict(exclude_unset=True)
    result = service.update(member_id, update_dict)
    if not result:
        raise HTTPException(status_code=404, detail="Member not found")
    return {"message": "Member updated successfully"}


@router.delete("/{member_id}", response_model=dict)
def delete_member(member_id: str):
    result = service.delete(member_id)
    if not result:
        raise HTTPException(status_code=404, detail="Member not found")
    return {"message": "Member deleted successfully"}
