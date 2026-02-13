from sqlalchemy import Column, String, Float, DateTime, ForeignKey, LargeBinary, Integer
from sqlalchemy.orm import relationship
from .database import Base
import uuid
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Integer, default=1)  # 1 for True, 0 for False (SQLite boolean)
    username = Column(String, default="User")
    subtitle = Column(String, default="New User")
    profile_image_data = Column(LargeBinary, nullable=True)

    expenses = relationship("Expense", back_populates="owner")
    friends = relationship("Friend", back_populates="owner")
    saved_items = relationship("SavedItem", back_populates="owner")

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    title = Column(String, index=True)
    amount = Column(Float)
    date = Column(DateTime, default=datetime.utcnow)
    category = Column(String)  # Storing Enum as String
    receipt_data = Column(LargeBinary, nullable=True)
    recipient_email = Column(String, nullable=True)

    owner = relationship("User", back_populates="expenses")
    splits = relationship("Split", back_populates="expense", cascade="all, delete-orphan")
    items = relationship("ExpenseItem", back_populates="expense", cascade="all, delete-orphan")

class ExpenseItem(Base):
    __tablename__ = "expense_items"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    expense_id = Column(String, ForeignKey("expenses.id"))
    name = Column(String)
    price = Column(Float)
    quantity = Column(Integer, default=1)
    image_data = Column(LargeBinary, nullable=True)

    expense = relationship("Expense", back_populates="items")

class Split(Base):
    __tablename__ = "splits"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    expense_id = Column(String, ForeignKey("expenses.id"))
    name = Column(String)
    initials = Column(String)
    amount = Column(Float, nullable=True) # Optional, if we want to track specific split amounts

    expense = relationship("Expense", back_populates="splits")

class Friend(Base):
    __tablename__ = "friends"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    name = Column(String)
    initials = Column(String)
    gradient_start = Column(String) # RGBA or Hex
    gradient_end = Column(String)

    owner = relationship("User", back_populates="friends")

class SavedItem(Base):
    __tablename__ = "saved_items"
    
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    name = Column(String, index=True) # Removed unique=True to allow same name for different users
    default_price = Column(Float, default=0.0)

    owner = relationship("User", back_populates="saved_items")
