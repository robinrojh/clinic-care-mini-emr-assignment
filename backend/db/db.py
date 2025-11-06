from sqlalchemy import String, Integer, Text, ForeignKey, PrimaryKeyConstraint, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker, Session
from typing import List, Generator

DB_NAME = "clinic_care"
DB_USER = "postgres"
DB_PASS = "asdfasdf"
DB_HOST = "localhost"
DB_PORT = "5432"

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    notes: Mapped[List["Note"]] = relationship("Note", back_populates="user")

    def __repr__(self) -> str:
        return f"<User(user_id={self.user_id!r}, email={self.email!r})>"


class Note(Base):
    __tablename__ = "notes"
    
    note_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=True)
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="notes")

    def __repr__(self) -> str:
        return f"<Note(note_id={self.note_id!r}, title={self.title!r})>"


class Code(Base):
    __tablename__ = "codes"

    chapter_code: Mapped[str] = mapped_column(String(1), nullable=False)
    category_code: Mapped[str] = mapped_column(String(2), nullable=False)
    subcategory_code: Mapped[str] = mapped_column(String(1), nullable=False, default='X')
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    __table_args__ = (
        PrimaryKeyConstraint("chapter_code", "category_code", "subcategory_code"),
    )

    def __repr__(self) -> str:
        return f"<Code(code={self.chapter_code}{self.category_code}.{self.subcategory_code})>"


try:
    database_url = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(url=database_url)

    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    print("Database session created successfully!")
except:
    print("Database session creation failed.")

def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a database session.
    It ensures the session is always closed after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    Initializes the database by creating all tables.
    """
    try:
        print("Importing models...")
        from models.models import UserModel, NoteModel, CodeModel 

        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully.")
    except ImportError:
        print("Error: Could not import models. Make sure 'models/models.py' exists.")
    except Exception as e:
        print(f"An error occurred during DB initialization: {e}")

if __name__ == "__main__":
    print("Initializing database...")
    init_db()