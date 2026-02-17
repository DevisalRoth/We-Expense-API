from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from jose import JWTError, jwt

from . import models, schemas, crud, auth
from .database import SessionLocal, engine
from .email import send_receipt_email
from .telegram_bot import send_telegram_notification

# Create tables
try:
    models.Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"⚠️ Error creating tables on startup: {e}")
    # Don't crash here, let the app start. The endpoint requests might fail later if tables don't exist,
    # but at least we'll get logs instead of a hard crash.

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency
def get_db():
    if SessionLocal is None:
        raise HTTPException(status_code=500, detail="Database not initialized")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

@app.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.email})
    refresh_token = auth.create_refresh_token(data={"sub": user.email})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@app.post("/refresh", response_model=schemas.Token)
async def refresh_token(token: str, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
        
    access_token = auth.create_access_token(data={"sub": user.email})
    # Optionally rotate refresh token
    return {"access_token": access_token, "refresh_token": token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_user)):
    return current_user

@app.put("/users/me", response_model=schemas.User)
async def update_user_me(user_update: schemas.UserUpdate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    updated_user = crud.update_user(db, user_id=current_user.id, user_update=user_update)
    return updated_user

@app.get("/db-test")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        # Try a simple query
        result = db.execute(text("SELECT 1")).scalar()
        return {"status": "ok", "result": result, "db_url": str(engine.url).replace(":", "***")}
    except Exception as e:
        return {"status": "error", "detail": str(e)}

@app.get("/")
def read_root():
    return {"message": "Expense API is running"}

@app.post("/expenses/", response_model=schemas.Expense)
async def create_expense(
    expense: schemas.ExpenseCreate, 
    background_tasks: BackgroundTasks,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        db_expense = crud.create_expense(db=db, expense=expense, user_id=current_user.id)
        
        # Send email if recipient is provided
        if expense.recipient_email:
            expense_data = {
                "title": db_expense.title,
                "amount": f"{db_expense.amount:.2f}",
                "date": db_expense.date.strftime("%Y-%m-%d %H:%M"),
                "category": db_expense.category,
                "id": db_expense.id
            }
            # Note: We need to update send_receipt_email to handle background tasks properly if it's async
            # For now, let's assume it works or fix it later.
            # background_tasks.add_task(send_receipt_email, expense.recipient_email, expense_data, expense.receipt_data)
            
        # Send Telegram notification (if configured)
        if expense.telegram_chat_id:
            expense_data = {
                "title": db_expense.title,
                "amount": f"{db_expense.amount:.2f}",
                "date": db_expense.date.strftime("%Y-%m-%d %H:%M"),
                "category": db_expense.category,
                "id": db_expense.id
            }
            # background_tasks.add_task(send_telegram_notification, expense.telegram_chat_id, expense_data, expense.receipt_data)
            
        return db_expense
    except Exception as e:
        print(f"Server Error creating expense: {e}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.get("/expenses/", response_model=List[schemas.Expense])
def read_expenses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    expenses = crud.get_expenses(db, user_id=current_user.id, skip=skip, limit=limit)
    return expenses

@app.get("/expenses/{expense_id}", response_model=schemas.Expense)
def read_expense(expense_id: str, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_expense = crud.get_expense(db, expense_id=expense_id, user_id=current_user.id)
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return db_expense

@app.delete("/expenses/{expense_id}", response_model=schemas.Expense)
def delete_expense(expense_id: str, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_expense = crud.delete_expense(db, expense_id=expense_id, user_id=current_user.id)
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return db_expense

@app.put("/expenses/{expense_id}", response_model=schemas.Expense)
def update_expense(expense_id: str, expense: schemas.ExpenseUpdate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_expense = crud.update_expense(db, expense_id=expense_id, expense=expense, user_id=current_user.id)
    if db_expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return db_expense

@app.post("/friends/", response_model=schemas.Friend)
def create_friend(friend: schemas.FriendCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return crud.create_friend(db=db, friend=friend, user_id=current_user.id)

@app.get("/friends/", response_model=List[schemas.Friend])
def read_friends(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    friends = crud.get_friends(db, user_id=current_user.id, skip=skip, limit=limit)
    return friends

@app.get("/saved-items/", response_model=List[schemas.SavedItem])
def read_saved_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return crud.get_saved_items(db, user_id=current_user.id, skip=skip, limit=limit)

@app.post("/saved-items/", response_model=schemas.SavedItem)
def create_saved_item(item: schemas.SavedItemCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return crud.create_saved_item(db=db, item=item, user_id=current_user.id)

@app.put("/saved-items/{item_id}", response_model=schemas.SavedItem)
def update_saved_item(item_id: str, item: schemas.SavedItemCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_item = crud.update_saved_item(db, item_id=item_id, item=item, user_id=current_user.id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.delete("/saved-items/{item_id}", response_model=schemas.SavedItem)
def delete_saved_item(item_id: str, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    db_item = crud.delete_saved_item(db, item_id=item_id, user_id=current_user.id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
