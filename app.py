from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime


# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow frontend to call API

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Expense Model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
# Create the database
with app.app_context():
    db.create_all()

# Route to add an expense
@app.route("/add_expense", methods=["POST"])
def add_expense():
    data = request.json

    # ✅ Check if all required fields are present
    if "title" not in data or "amount" not in data or "category" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    # ✅ Ensure amount is a valid positive number
    if not isinstance(data["amount"], (int, float)) or data["amount"] <= 0:
        return jsonify({"error": "Amount must be a positive number"}), 400

    # ✅ Save the expense to the database
    new_expense = Expense(title=data["title"], amount=data["amount"], category=data["category"])
    db.session.add(new_expense)
    db.session.commit()
    
    return jsonify({"message": "Expense added successfully"}), 201


# Route to get all expenses
@app.route("/get_expenses", methods=["GET"])
def get_expenses():
    expenses = Expense.query.all()
    return jsonify([
        {
            "id": e.id, 
            "title": e.title, 
            "amount": e.amount, 
            "category": e.category,
            "date_added": e.date_added.strftime("%Y-%m-%d %H:%M:%S")  # ✅ Convert datetime to string
        } 
        for e in expenses
    ])

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
