from app.db.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True)
    username = Column(String(100), unique=True)
    password = Column(String(100))


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    type = Column(String(100))
    balance = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"))


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    user_id = Column(Integer, ForeignKey("users.id"))


class Transaction(Base):

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Integer)
    date = Column(Date)
    category = Column(String(100))
    transaction_type = Column(String(50))
    remarks = Column(String(100))
    user_id = Column(Integer, ForeignKey("users.id"))
    account_id = Column(Integer, ForeignKey("accounts.id"))
