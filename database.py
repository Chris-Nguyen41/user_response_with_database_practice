from sqlalchemy import create_engine, Integer, String
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from dotenv import load_dotenv
import streamlit as st
from urllib.parse import quote_plus
import os



load_dotenv()


USER = os.getenv("user")
RAW_PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

ENCODED_PASSWORD = quote_plus(RAW_PASSWORD)

DATABASE_URL = f"postgresql+psycopg2://{USER}:{ENCODED_PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

@st.cache_resource
def get_engine():
    return create_engine(DATABASE_URL, poolclass=NullPool, pool_pre_ping=True, connect_args={"options" : "-c statment_timeout=5000"})

engine = get_engine()

class Base(DeclarativeBase):
    pass

class User_Response(Base):
    __tablename__ = "user_responses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    response: Mapped[str] = mapped_column(String(3), nullable=False)

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)