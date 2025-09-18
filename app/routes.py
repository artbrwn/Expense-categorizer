from app import app
from flask import render_template

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/review")
def review():
    from app.models.normalize_data import NormalizeData
    from app.models.load_data import LoadData
    from app.models.categorize_transactions import CategorizeTransactions

    # Create instance of LoadData for statements folder
    load_data = LoadData("statements")

    # Extract text from all pdf's in folder
    raw_text = load_data.extract_all_texts()

    # Create instance of NormalizeData for the extracted text
    normalize_data = NormalizeData(raw_text)

    # Get only transactions from text
    transactions_list = normalize_data.extract_transactions()

    # Format extracted transactions
    transformed_list = normalize_data.transform_transactions()

    # Apply correct signs to transactions
    normalize_data.apply_signs()

    # Create instance of CategorizeTransactions
    categorize_transactions = CategorizeTransactions()

    # Load config from json file
    categorize_transactions.load_config()

    # First categorization of data
    categorize_transactions.categorize(normalize_data.transactions)
    all_transactions = categorize_transactions.categorized_transactions
    all_categories = categorize_transactions.categories
    return render_template("review.html", transactions=all_transactions, categories=all_categories)