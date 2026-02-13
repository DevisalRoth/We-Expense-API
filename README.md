# Expense App FastAPI Backend

This is the backend for the Expense App, replacing CoreData storage.

## Setup

1.  **Create Virtual Environment**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

2.  **Install Dependencies**:
    ```bash
    pip install fastapi uvicorn sqlalchemy requests
    ```

## Running the Server

Run the server using `uvicorn`:

```bash
./.venv/bin/uvicorn app.main:app --reload --port 8002
```

The API will be available at `http://127.0.0.1:8002`.
Interactive documentation is available at `http://127.0.0.1:8002/docs`.

## API Endpoints

### Authentication
-   `POST /register`: Register a new user.
-   `POST /token`: Login and get access/refresh tokens.
-   `POST /refresh`: Refresh an expired access token.

### User
-   `GET /users/me`: Get current user profile.
-   `PUT /users/me`: Update user profile (username, subtitle, profile image).

### Expenses
-   `GET /`: Check if API is running.
-   `POST /expenses/`: Create a new expense.
-   `GET /expenses/`: List all expenses.
-   `GET /expenses/{id}`: Get a specific expense.
-   `PUT /expenses/{id}`: Update an expense.
-   `DELETE /expenses/{id}`: Delete an expense.

### Friends & Saved Items
-   `POST /friends/`: Create a new friend (for splits).
-   `GET /friends/`: List all friends.
-   `GET /saved-items/`: List saved items.
-   `POST /saved-items/`: Create a saved item.
-   `DELETE /saved-items/{id}`: Delete a saved item.

## Data Models

The data models are designed to mirror the Swift CoreData entities:

-   **User**: `id`, `email`, `hashed_password`, `username`, `subtitle`, `profile_image_data`
-   **Expense**: `id`, `title`, `amount`, `date`, `category`, `receipt_data`
-   **Split**: `id`, `expense_id`, `name`, `initials`, `amount`
-   **Friend**: `id`, `name`, `initials`, `gradient_start`, `gradient_end`
-   **SavedItem**: `id`, `name`, `default_price`
