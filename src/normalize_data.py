import re
from datetime import datetime

class NormalizeData:
    def __init__(self, raw_text: list):
        self.raw_text = raw_text
        self.regular_expressions = {"bank": r'^\d{2}-\d{2}-\d{2}\s+\d+\s+\d{2}-\d{2}-\d{2}\s+.+\s+\d{1,3}(?:\.\d{3})*,\d{2}\s+\d{1,3}(?:\.\d{3})*,\d{2}$', 
                               "card": r'^\d{2}/\d{2}/\d{4}\s+\d{4}\s+.+\s+\d{1,3}(?:\.\d{3})*,\d{2}$'}
        self.raw_transactions = []
        self.transactions = []

    def extract_transactions(self) -> list:
        self.raw_transactions = []
        for file_text in self.raw_text:
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
                    self.raw_transactions.append({"transaction": transaction, "category": category})

        return self.raw_transactions
    
    def transform_transactions(self):
        for raw_transaction in self.raw_transactions:
            if raw_transaction["category"] == "bank":
                match = re.match(r"^(?P<date>\d{2}-\d{2}-\d{2})\s+\d+\s+\d{2}-\d{2}-\d{2}\s+(?P<description>.+)\s+(?P<amount>\d{1,3}(?:\.\d{3})*,\d{2})\s+(?P<balance>\d{1,3}(?:\.\d{3})*,\d{2})$", raw_transaction["transaction"])
                transaction = {"date": datetime.strptime(match.group("date"), "%d-%m-%y"),
                               "description": match.group("description"),
                               "amount": float(match.group("amount").replace(",", ".")),
                               "balance": float(match.group("balance").replace(".", "").replace(",", ".")),
                               "type": "bank"}
                self.transactions.append(transaction)
            elif raw_transaction["category"] == "card":
                match = re.match(r'(?P<date>\d{2}/\d{2}/\d{4})\s+\d{4}\s+(?P<description>.+?)\s+(?P<amount>\d{1,3}(?:\.\d{3})*,\d{2})', raw_transaction["transaction"])
                transaction = {"date": datetime.strptime(match.group("date"), "%d/%m/%Y"),
                               "description": match.group("description"),
                               "amount": -float(match.group("amount").replace(",", ".")),
                               "type": "card"}
                self.transactions.append(transaction)
        return self.transactions
    
    def apply_signs(self):
        bank_transactions = [t for t in self.transactions if t["type"] == "bank"]
        for i in range(1, len(bank_transactions)):
            prev_balance = bank_transactions[i-1]["balance"]
            current_balance = bank_transactions[i]["balance"]
            amount = bank_transactions[i]["amount"]

            if current_balance < prev_balance:
                bank_transactions[i]["amount"] = -amount
            else:
                bank_transactions[i]["amount"] = amount
        pointer = 0
        for i in range(len(self.transactions)): 
            if self.transactions[i]["type"] == "bank":
                self.transactions[i] = bank_transactions[pointer]
                pointer += 1

        
