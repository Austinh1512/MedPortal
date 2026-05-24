from extensions import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey
from datetime import date, datetime

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
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
    
    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "race": self.race,
            "ethnicity": self.ethnicity,
            "gender": self.gender,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "zip": self.zip,
            "birth_date": self.birth_date.isoformat(),
            "death_date": self.death_date.isoformat() if self.death_date else None
        }
    
class Condition(Base):
    __tablename__ = "conditions"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[str] = mapped_column(String(36), ForeignKey("patients.id"), nullable=False)
    start_date: Mapped[date] = mapped_column(nullable=False)
    stop_date: Mapped[date] = mapped_column(nullable=True)
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)

    def __repr__(self):
        return f"<Condition {self.id}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "start_date": self.start_date.isoformat(),
            "stop_date": self.stop_date.isoformat() if self.stop_date else None,
            "code": self.code,
            "description": self.description
        }
    
class Medication(Base):
    __tablename__ = "medications"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[str] = mapped_column(String(36), ForeignKey("patients.id"), nullable=False)
    start_date: Mapped[date] = mapped_column(nullable=False)
    stop_date: Mapped[date] = mapped_column(nullable=True)
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    reason_code: Mapped[str] = mapped_column(String(20), nullable=True)
    reason_description: Mapped[str] = mapped_column(String(500), nullable=True)

    def __repr__(self):
        return f"<Medication {self.id}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "start_date": self.start_date.isoformat(),
            "stop_date": self.stop_date.isoformat() if self.stop_date else None,
            "code": self.code,
            "description": self.description,
            "reason_code": self.reason_code,
            "reason_description": self.reason_description
        }
    
class Observation(Base):
    __tablename__ = "observations"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[str] = mapped_column(String(36), ForeignKey("patients.id"), nullable=False)
    observation_date: Mapped[date] = mapped_column(nullable=False)
    category: Mapped[str] = mapped_column(String(255), nullable=True)
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    value: Mapped[str] = mapped_column(String(255), nullable=True)
    units: Mapped[str] = mapped_column(String(50), nullable=True)
    type: Mapped[str] = mapped_column(String(50), nullable=True)

    def __repr__(self):
        return f"<Observation {self.id}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "observation_date": self.observation_date.isoformat(),
            "category": self.category,
            "code": self.code,
            "description": self.description,
            "value": self.value,
            "units": self.units,
            "type": self.type
        }
    
class Encounter(Base):
    __tablename__ = "encounters"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    patient_id: Mapped[str] = mapped_column(String(36), ForeignKey("patients.id"), nullable=False)
    start_date: Mapped[date] = mapped_column(nullable=False)
    encounter_class: Mapped[str] = mapped_column(String(100), nullable=False)
    code: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    reason_code: Mapped[str] = mapped_column(String(20), nullable=True)
    reason_description: Mapped[str] = mapped_column(String(255), nullable=True)

    def __repr__(self):
        return f"<Encounter {self.id}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "start_date": self.start_date.isoformat(),
            "encounter_class": self.encounter_class,
            "code": self.code,
            "description": self.description,
            "reason_code": self.reason_code,
            "reason_description": self.reason_description
        }