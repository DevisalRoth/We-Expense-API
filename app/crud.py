from sqlalchemy.orm import Session
from . import models, schemas
from .auth import get_password_hash
import uuid

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    # Default username from email if not provided (though our schema currently doesn't ask for it)
    username = user.email.split("@")[0].capitalize()
    db_user = models.User(
        email=user.email, 
        hashed_password=hashed_password,
        username=username,
        subtitle="New User"
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: str, user_update: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None
    
    if user_update.username is not None:
        db_user.username = user_update.username
    if user_update.subtitle is not None:
        db_user.subtitle = user_update.subtitle
    if user_update.profile_image_data is not None:
        db_user.profile_image_data = user_update.profile_image_data
        
    db.commit()
    db.refresh(db_user)
    return db_user

def get_expense(db: Session, expense_id: str, user_id: str):
    return db.query(models.Expense).filter(models.Expense.id == expense_id, models.Expense.user_id == user_id).first()

def get_expenses(db: Session, user_id: str, skip: int = 0, limit: int = 100):
    return db.query(models.Expense).filter(models.Expense.user_id == user_id).offset(skip).limit(limit).all()

def create_expense(db: Session, expense: schemas.ExpenseCreate, user_id: str):
    try:
        db_expense = models.Expense(
            user_id=user_id,
            title=expense.title,
            amount=expense.amount,
            date=expense.date,
            category=expense.category.value, # Store the string value
            receipt_data=expense.receipt_data,
            recipient_email=expense.recipient_email
        )
        db.add(db_expense)
        db.commit()
        db.refresh(db_expense)
        
        # Create splits if any
        for split in expense.splits:
            db_split = models.Split(
                expense_id=db_expense.id,
                name=split.name,
                initials=split.initials,
                amount=split.amount
            )
            db.add(db_split)
        
        # Create items if any
        for item in expense.items:
            db_item = models.ExpenseItem(
                expense_id=db_expense.id,
                name=item.name,
                price=item.price,
                quantity=item.quantity,
                image_data=item.image_data
            )
            db.add(db_item)
        
        db.commit()
        db.refresh(db_expense)
        return db_expense
    except Exception as e:
        db.rollback()
        print(f"❌ Error creating expense: {str(e)}")
        # Raise it again so FastAPI can handle it (or return None)
        raise e

def delete_expense(db: Session, expense_id: str, user_id: str):
    db_expense = db.query(models.Expense).filter(models.Expense.id == expense_id, models.Expense.user_id == user_id).first()
    if db_expense:
        db.delete(db_expense)
        db.commit()
    return db_expense

def update_expense(db: Session, expense_id: str, expense: schemas.ExpenseUpdate, user_id: str):
    db_expense = db.query(models.Expense).filter(models.Expense.id == expense_id, models.Expense.user_id == user_id).first()
    if not db_expense:
        return None
    
    # Update fields
    if expense.title is not None:
        db_expense.title = expense.title
    if expense.amount is not None:
        db_expense.amount = expense.amount
    if expense.date is not None:
        db_expense.date = expense.date
    if expense.category is not None:
        db_expense.category = expense.category.value
    if expense.receipt_data is not None:
        db_expense.receipt_data = expense.receipt_data
    if expense.recipient_email is not None:
        db_expense.recipient_email = expense.recipient_email
        
    # Update Splits (Replace strategy)
    if expense.splits is not None:
        # Delete existing splits
        db.query(models.Split).filter(models.Split.expense_id == expense_id).delete()
        # Add new splits
        for split in expense.splits:
            db_split = models.Split(
                expense_id=db_expense.id,
                name=split.name,
                initials=split.initials,
                amount=split.amount
            )
            db.add(db_split)
            
    # Update Items (Replace strategy)
    if expense.items is not None:
        # Delete existing items
        db.query(models.ExpenseItem).filter(models.ExpenseItem.expense_id == expense_id).delete()
        # Add new items
        for item in expense.items:
            db_item = models.ExpenseItem(
                expense_id=db_expense.id,
                name=item.name,
                price=item.price,
                quantity=item.quantity,
                image_data=item.image_data
            )
            db.add(db_item)
            
    db.commit()
    db.refresh(db_expense)
    return db_expense

def get_friends(db: Session, user_id: str, skip: int = 0, limit: int = 100):
    return db.query(models.Friend).filter(models.Friend.user_id == user_id).offset(skip).limit(limit).all()

def create_friend(db: Session, friend: schemas.FriendCreate, user_id: str):
    db_friend = models.Friend(
        user_id=user_id,
        name=friend.name,
        initials=friend.initials,
        gradient_start=friend.gradient_start,
        gradient_end=friend.gradient_end
    )
    db.add(db_friend)
    db.commit()
    db.refresh(db_friend)
    return db_friend

def get_saved_items(db: Session, user_id: str, skip: int = 0, limit: int = 100):
    return db.query(models.SavedItem).filter(models.SavedItem.user_id == user_id).offset(skip).limit(limit).all()

def create_saved_item(db: Session, item: schemas.SavedItemCreate, user_id: str):
    db_item = models.SavedItem(user_id=user_id, name=item.name, default_price=item.default_price)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_saved_item(db: Session, item_id: str, item: schemas.SavedItemCreate, user_id: str):
    db_item = db.query(models.SavedItem).filter(models.SavedItem.id == item_id, models.SavedItem.user_id == user_id).first()
    if db_item:
        db_item.name = item.name
        db_item.default_price = item.default_price
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_saved_item(db: Session, item_id: str, user_id: str):
    db_item = db.query(models.SavedItem).filter(models.SavedItem.id == item_id, models.SavedItem.user_id == user_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item
