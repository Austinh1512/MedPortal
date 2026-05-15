from app import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from datetime import date, datetime

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), Punique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    date_created: Mapped[datetime] = mapped_column(default=datetime.now)

    def __repr__(self):
        return f"<User {self.id}>"
    
class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    race: Mapped[str] = mapped_column(String(100), nullable=False)
    ethnicity: Mapped[str] = mapped_column(String(100), nullable=False)
    gender: Mapped[str] = mapped_column(String(1), nullable=False)
    address: Mapped[str] = mapped_column(String(100), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    zip: Mapped[str] = mapped_column(String(10), nullable=False)
    birth_date: Mapped[date] = mapped_column(nullable=False)
    death_date: Mapped[date] = mapped_column(nullable=True)

    def __repr__(self):
        return f"<Patient {self.id}>"