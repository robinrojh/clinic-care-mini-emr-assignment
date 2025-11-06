from sqlalchemy import String, Integer, Text, ForeignKey, PrimaryKeyConstraint, create_engine, Table, Column, ForeignKeyConstraint
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

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(255), nullable=False)
    last_name: Mapped[str] = mapped_column(String(255), nullable=False)
    notes: Mapped[List["Note"]] = relationship("Note", back_populates="user")

    def __repr__(self) -> str:
        return f"<User(email={self.email!r})>"
    
notes_codes_table = Table(
    "notes_codes",
    Base.metadata,
    Column("note_id", Integer, ForeignKey("notes.note_id"), primary_key=True),
    
    Column("chapter_code", String(1), primary_key=True),
    Column("category_code", String(2), primary_key=True),
    Column("subcategory_code", String(1), primary_key=True, default='-'),
    
    ForeignKeyConstraint(
        ["chapter_code", "category_code", "subcategory_code"],
        ["codes.chapter_code", "codes.category_code", "codes.subcategory_code"],
    )
)
class Note(Base):
    __tablename__ = "notes"
    
    note_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=True)
    

    email: Mapped[str] = mapped_column(ForeignKey("users.email"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="notes")

    codes: Mapped[List["Code"]] = relationship(
            "Code",
            secondary=notes_codes_table,
            back_populates="notes"
        )

    def __repr__(self) -> str:
        return f"<Note(note_id={self.note_id!r}, title={self.title!r})>"


class Code(Base):
    __tablename__ = "codes"

    chapter_code: Mapped[str] = mapped_column(String(1), primary_key=True)
    category_code: Mapped[str] = mapped_column(String(2), primary_key=True)
    subcategory_code: Mapped[str] = mapped_column(String(1), primary_key=True, default='-')
    
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    notes: Mapped[List["Note"]] = relationship(
            "Note",
            secondary=notes_codes_table,
            back_populates="codes"
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
        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully.")
    except Exception as e:
        print(f"An error occurred during DB initialization: {e}")

if __name__ == "__main__":
    print("Initializing database...")
    init_db()