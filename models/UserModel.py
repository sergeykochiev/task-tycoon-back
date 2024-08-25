from typing import Optional
from uuid import uuid4

from sqlalchemy.sql import func
from sqlalchemy import DateTime, String, UUID
from sqlalchemy.orm import Mapped, mapped_column
from models.BaseModel import BaseModel
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_utils import EmailType


class UserModel(BaseModel):
    __tablename__ = "users"

    UUID: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    email: Mapped[EmailType] = mapped_column(EmailType, unique=True)
    hashed_password: Mapped[str] = mapped_column(String)
    name: Mapped[Optional[str]] = mapped_column(String)
    surname: Mapped[Optional[str]] = mapped_column(String)
    nickname: Mapped[Optional[str]] = mapped_column(String, unique=True)
    create_date: Mapped[datetime] = mapped_column(DateTime(timezone=False), server_default=func.now())


    def __init__(self, **kwargs):
        kwargs['UUID'] = uuid4()
        super().__init__(**kwargs)

    @property
    def password(self):
        raise ValueError("user contains only hashed password")

    @password.setter
    def password(self, password: str):
        self.hashed_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.hashed_password_password, password)