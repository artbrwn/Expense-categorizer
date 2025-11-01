from app import app
from flask import render_template, request, redirect
from app.models.transaction_processor import TransactionProcessor
import json
from app.models.analyze_transactions import AnalyzeTransactions
from datetime import datetime
from pathlib import Path

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/process")
def process():
    message = None
    try:
        processor = TransactionProcessor()
        all_transactions = processor.process_transactions()
        
        timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M")
        filename = f"transactions_{timestamp}.json"
        save_dir = Path("data/auto_processed")
        save_dir.mkdir(parents=True, exist_ok=True)

        with open("data/auto_processed/" + filename, "w") as file:
            json.dump(all_transactions, file, default=str)
    except Exception as e:
        message = f"An error has occurred: {e}"
    
    return render_template("process.html", message=message)
    

@app.route("/review", methods=["GET", "POST"])
def review():
    processor = TransactionProcessor()
    all_transactions = processor.process_transactions()
    if request.method == "GET":
        all_categories = processor.categories
        return render_template("review.html", 
                            transactions=all_transactions, 
                            categories=all_categories)
    elif request.method == "POST":
        transactions = processor.reconstruct_transactions(request.form)
        with open("data/processed_data.json", "w") as file:
            json.dump(transactions, file)
        
        return redirect("/stats")
    
@app.route("/stats")
def stats():
    df = AnalyzeTransactions()
    df.load_data()
    df.create_month_column()
    charts = df.prepare_for_chart()
    return render_template("stats.html", charts=charts)