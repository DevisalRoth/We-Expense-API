import requests
import datetime

BASE_URL = "http://127.0.0.1:8002"

def test_create_friend():
    friend_data = {
        "name": "Test Friend",
        "initials": "TF",
        "gradient_start": "#FF0000",
        "gradient_end": "#00FF00"
    }
    response = requests.post(f"{BASE_URL}/friends/", json=friend_data)
    print("Create Friend Status:", response.status_code)
    print("Create Friend Response:", response.json())
    return response.json()

def test_create_expense(friend_id=None):
    expense_data = {
        "title": "Test Expense",
        "amount": 100.50,
        "date": datetime.datetime.now().isoformat(),
        "category": "Food",
        "splits": []
    }
    if friend_id:
        expense_data["splits"].append({
            "name": "Test Friend",
            "initials": "TF",
            "amount": 50.25
        })
    
    response = requests.post(f"{BASE_URL}/expenses/", json=expense_data)
    print("Create Expense Status:", response.status_code)
    print("Create Expense Response:", response.json())

if __name__ == "__main__":
    try:
        friend = test_create_friend()
        test_create_expense(friend["id"])
    except Exception as e:
        print("Error:", e)
