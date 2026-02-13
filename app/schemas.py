from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str = Field(..., max_length=128)

class User(UserBase):
    id: str
    is_active: bool
    username: Optional[str] = "User"
    subtitle: Optional[str] = "New User"
    profile_image_data: Optional[bytes] = None

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    username: Optional[str] = None
    subtitle: Optional[str] = None
    profile_image_data: Optional[bytes] = None

class ExpenseCategory(str, Enum):
    lodging = "Lodging"
    food = "Food"
    activities = "Fun"
    transport = "Transport"

class SplitBase(BaseModel):
    name: str
    initials: str
    amount: Optional[float] = None

class SplitCreate(SplitBase):
    pass

class Split(SplitBase):
    id: str
    expense_id: str

    class Config:
        from_attributes = True

class ExpenseItemBase(BaseModel):
    name: str
    price: float
    quantity: int = 1
    image_data: Optional[bytes] = None

class ExpenseItemCreate(ExpenseItemBase):
    pass

class ExpenseItem(ExpenseItemBase):
    id: str
    expense_id: str

    class Config:
        from_attributes = True

class ExpenseBase(BaseModel):
    title: str
    amount: float
    date: datetime
    category: ExpenseCategory

class ExpenseCreate(ExpenseBase):
    receipt_data: Optional[bytes] = None
    recipient_email: Optional[str] = None
    telegram_chat_id: Optional[str] = None
    splits: List[SplitCreate] = []
    items: List[ExpenseItemCreate] = []

class ExpenseUpdate(BaseModel):
    title: Optional[str] = None
    amount: Optional[float] = None
    date: Optional[datetime] = None
    category: Optional[ExpenseCategory] = None
    receipt_data: Optional[bytes] = None
    recipient_email: Optional[str] = None
    splits: Optional[List[SplitCreate]] = None
    items: Optional[List[ExpenseItemCreate]] = None

class ExpenseListItem(ExpenseBase):
    id: str
    recipient_email: Optional[str] = None
    splits: List[Split] = []
    items: List[ExpenseItem] = []

    class Config:
        from_attributes = True

class Expense(ExpenseListItem):
    receipt_data: Optional[bytes] = None

class FriendBase(BaseModel):
    name: str
    initials: str
    gradient_start: str
    gradient_end: str

class FriendCreate(FriendBase):
    pass

class Friend(FriendBase):
    id: str

    class Config:
        from_attributes = True

class SavedItemBase(BaseModel):
    name: str
    default_price: float = 0.0

class SavedItemCreate(SavedItemBase):
    pass

class SavedItem(SavedItemBase):
    id: str

    class Config:
        from_attributes = True
