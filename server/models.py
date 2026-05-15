from app import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), Punique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    date_created: Mapped[datetime] = mapped_column(default=datetime.now)

    def __repr__(self):
        return f"<User {self.id}?"