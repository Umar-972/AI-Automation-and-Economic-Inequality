from datetime import datetime
from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator
from typing import Literal

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=10, max_length=128)
    timezone: str = "UTC"

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr
    timezone: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TransactionCreate(BaseModel):
    amount: float = Field(gt=0, le=1_000_000_000)
    kind: Literal["income", "expense"]
    category: str = Field(default="Uncategorized", max_length=80)
    description: str = Field(default="", max_length=300)
    occurred_at: datetime
    recurring: bool = False
    recurrence: Literal["weekly", "monthly", "yearly"] | None = None

    @field_validator("occurred_at")
    @classmethod
    def require_timezone(cls, v):
        if v.tzinfo is None or v.utcoffset() is None:
            raise ValueError("occurred_at must include a timezone offset")
        return v

class TransactionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    amount: float
    kind: str
    category: str
    description: str
    occurred_at: datetime
    recurring: bool
    recurrence: str | None

class EventCreate(BaseModel):
    title: str = Field(min_length=1, max_length=180)
    amount: float = Field(ge=0, le=1_000_000_000)
    kind: Literal["income", "expense"]
    scheduled_at: datetime
    notes: str = ""

    @field_validator("scheduled_at")
    @classmethod
    def require_timezone(cls, v):
        if v.tzinfo is None or v.utcoffset() is None:
            raise ValueError("scheduled_at must include a timezone offset")
        return v

class EventOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    amount: float
    kind: str
    scheduled_at: datetime
    notes: str
