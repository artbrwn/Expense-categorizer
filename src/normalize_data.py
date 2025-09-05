import re

class NormalizeData:
    def __init__(self):
        self.regular_expressions = {"bank": r'^\d{2}-\d{2}-\d{2}\s+\d+\s+\d{2}-\d{2}-\d{2}\s+.+\s+\d{1,3}(?:\.\d{3})*,\d{2}\s+\d{1,3}(?:\.\d{3})*,\d{2}$', 
                               "card": r'^\d{2}/\d{2}/\d{4}\s+\d{4}\s+.+\s+\d{1,3}(?:\.\d{3})*,\d{2}$'}

    def extract_transactions(self, raw_text: list) -> list:
        transactions = []
        for file_text in raw_text:
            # Decide category
            if "Movimientos y saldo de su cuenta" in file_text:
                category = "bank"
            elif "Extracto Tarjeta" in file_text:
                category = "card"
            else:
                category = "uncategorized"
            if category != "uncategorized":
                transactions_in_file = re.findall(self.regular_expressions[category], file_text, flags=re.MULTILINE)
                for transaction in transactions_in_file:
                    transactions.append({"transaction": transaction, "category": category})

        return transactions