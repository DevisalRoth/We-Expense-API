from fastapi.testclient import TestClient
from datetime import datetime

def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Expense API is running"}

def test_create_expense(client):
    response = client.post(
        "/expenses/",
        json={
            "title": "Test Expense",
            "amount": 50.0,
            "date": datetime.now().isoformat(),
            "category": "Food",
            "splits": [
                {"name": "Friend1", "initials": "F1", "amount": 25.0}
            ]
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Expense"
    assert data["amount"] == 50.0
    assert data["category"] == "Food"
    assert "id" in data

def test_read_expenses(client):
    # Create an expense first
    client.post(
        "/expenses/",
        json={
            "title": "Expense 1",
            "amount": 10.0,
            "date": datetime.now().isoformat(),
            "category": "Transport"
        },
    )
    
    response = client.get("/expenses/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_read_expense(client):
    # Create an expense
    create_response = client.post(
        "/expenses/",
        json={
            "title": "Single Expense",
            "amount": 20.0,
            "date": datetime.now().isoformat(),
            "category": "Lodging"
        },
    )
    expense_id = create_response.json()["id"]
    
    # Read it back
    response = client.get(f"/expenses/{expense_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == expense_id
    assert data["title"] == "Single Expense"

def test_delete_expense(client):
    # Create an expense
    create_response = client.post(
        "/expenses/",
        json={
            "title": "To Delete",
            "amount": 5.0,
            "date": datetime.now().isoformat(),
            "category": "Fun"
        },
    )
    expense_id = create_response.json()["id"]
    
    # Delete it
    response = client.delete(f"/expenses/{expense_id}")
    assert response.status_code == 200
    
    # Verify it's gone
    get_response = client.get(f"/expenses/{expense_id}")
    assert get_response.status_code == 404
