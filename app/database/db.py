from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Mapped
from datetime import datetime
from app.config import settings
from typing import Optional, List

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)  # type: ignore
    name: Mapped[str] = Column(String, nullable=False)  # type: ignore
    email: Mapped[str] = Column(String, unique=True, index=True, nullable=False)  # type: ignore
    hashed_password: Mapped[str] = Column(String, nullable=False)  # type: ignore
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)  # type: ignore

    projects: Mapped[List["Project"]] = relationship("Project", back_populates="owner")  # type: ignore

class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)  # type: ignore
    name: Mapped[str] = Column(String, nullable=False)  # type: ignore
    client_name: Mapped[str] = Column(String, nullable=False)  # type: ignore
    description: Mapped[Optional[str]] = Column(Text, nullable=True)  # type: ignore
    user_id: Mapped[int] = Column(Integer, ForeignKey("users.id"))  # type: ignore
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)  # type: ignore
    owner: Mapped["User"] = relationship("User", back_populates="projects")  # type: ignore
    files: Mapped[List["File"]] = relationship("File", back_populates="project")  # type: ignore

class File(Base):
    __tablename__ = "files"

    id: Mapped[int] = Column(Integer, primary_key=True, index=True)  # type: ignore
    filename: Mapped[str] = Column(String, nullable=False)  # type: ignore
    file_path: Mapped[str] = Column(String, nullable=False)  # type: ignore
    file_type: Mapped[str] = Column(String, nullable=False)  # type: ignore
    size: Mapped[int] = Column(Integer, nullable=False)  # type: ignore
    project_id: Mapped[int] = Column(Integer, ForeignKey("projects.id"))  # type: ignore
    secondary_file_id: Mapped[Optional[int]] = Column(Integer, nullable=True)  # type: ignore
    created_at: Mapped[datetime] = Column(DateTime, default=datetime.utcnow)  # type: ignore

    project: Mapped["Project"] = relationship("Project", back_populates="files")  # type: ignore

def get_db():
    # Fornece sessão do banco de dados
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()

def init_db():
    # Cria tabelas do banco de dados
    Base.metadata.create_all(bind=engine)

