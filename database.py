from sqlalchemy import create_engine, Integer, String
from sqlalchemy.pool import NullPool
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
import streamlit as st
from urllib.parse import quote_plus


USER = st.secrets['user']
RAW_PASSWORD = st.secrets['password']
HOST = st.secrets['host']
PORT = st.secrets['port']
DBNAME = st.secrets['dbname']

ENCODED_PASSWORD = quote_plus(RAW_PASSWORD)

DATABASE_URL = f"postgresql+psycopg2://{USER}:{ENCODED_PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"


@st.cache_resource(validate=False)
def get_engine():
    return create_engine(DATABASE_URL,
                         poolclass=NullPool, 
                         pool_pre_ping=True, 
                         connect_args={"options" : "-c statement_timeout=5000"})

class Base(DeclarativeBase):
    pass

class User_Response(Base):
    __tablename__ = 'user_responses'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    response: Mapped[str] = mapped_column(String(3), nullable=False)

engine = get_engine()

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine, expire_on_commit=False)
