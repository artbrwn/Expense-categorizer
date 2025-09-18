from app import app
from flask import render_template
from app.models.transaction_processor import TransactionProcessor

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/review")
def review():
    processor = TransactionProcessor("statements")
    all_transactions = processor.process_transactions()
    all_categories = processor.categories
    return render_template("review.html", 
                           transactions=all_transactions, 
                           categories=all_categories)