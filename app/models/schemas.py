from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List

# User Schemas
class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Project Schemas
class ProjectBase(BaseModel):
    name: str
    client_name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    name: str
    user_id: int
    description: Optional[str] = None
    created_at: datetime
    file_count: int

    class Config:
        from_attributes = True

# File Schemas
class FileBase(BaseModel):
    filename: str
    fyle_type: str
    size: int

class FileResponse(FileBase):
    id: int
    project_id: int 
    tags: List[str] = []
    created_at: datetime

    class Config:
        from_attributes = True

