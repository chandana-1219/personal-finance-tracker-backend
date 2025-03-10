import requests

# Add an expense
post_url = "http://127.0.0.1:5000/add_expense"
post_data = {
    "title": "Groceries",
    "amount": 50.5,
    "category": "Food"
}
post_response = requests.post(post_url, json=post_data)

print("\nPOST Response:")
print("Status Code:", post_response.status_code)
print("JSON:", post_response.json())

# Fetch all expenses
get_url = "http://127.0.0.1:5000/get_expenses"
get_response = requests.get(get_url)

print("\nGET Response:")
print("Status Code:", get_response.status_code)
print("JSON:", get_response.json())
