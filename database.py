from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./crud.db"  # creates crud.db in your back/ folder

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class ItemModel(Base):
    __tablename__ = "items"
    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String, nullable=False)
    description = Column(String, nullable=True)
    owner       = Column(String, nullable=False)

class UserModel(Base):
    __tablename__ = "users"
    username  = Column(String, primary_key=True)
    password  = Column(String, nullable=False)
    full_name = Column(String, nullable=True)
    email     = Column(String, nullable=True)
    phone     = Column(String, nullable=True)
    age       = Column(Integer, nullable=True)

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if not db.query(UserModel).first():
        db.add_all([
            UserModel(username="jack",  password="111"),
            UserModel(username="admin", password="admin123"),
        ])
        db.commit()
    db.close()