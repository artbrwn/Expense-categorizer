from app import app
from flask import render_template, request, redirect
from app.models.transaction_processor import TransactionProcessor
import json

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/review", methods=["GET", "POST"])
def review():
    processor = TransactionProcessor()
    all_transactions = processor.process_transactions("statements")

    if request.method == "GET":
        all_categories = processor.categories
        return render_template("review.html", 
                            transactions=all_transactions, 
                            categories=all_categories)
    elif request.method == "POST":
        transactions = processor.reconstruct_transactions(request.form)
        with open("data/processed_data.json", "w") as file:
            json.dump(transactions, file)
        
        return redirect("/stats.html")
    