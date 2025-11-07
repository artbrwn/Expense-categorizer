import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import base64
from io import BytesIO

class AnalyzeTransactions:
    def load_data(self, file_path):
        self.all_data = pd.read_json(file_path, convert_dates=True)
    
    def create_month_column(self):
        self.all_data["year_month"] = self.all_data["date"].dt.to_period("M")
    
    def monthly_net_by_category(self):
        return self.all_data.groupby(["year_month", "category"])["amount"].sum()

    def monthly_total_expense(self):
        return self.all_data.groupby("year_month")["amount"].sum()
    
    @property
    def salary(self):
        salary_df = self.all_data[self.all_data["category"] == "salary"]
        return salary_df.groupby("year_month")["amount"].sum().mean()

    def monthly_savings(self):
        # Excluye salary y uncategorized
        df_expenses = self.all_data[~self.all_data["category"].isin(["uncategorized", "salary"])]
        
        # Total mensual de gastos tal cual (positivos y negativos)
        total_expense = df_expenses.groupby("year_month")["amount"].sum()
        
        # Ahorro = salario normalizado - gastos reales
        savings = self.salary - total_expense
        return savings
        
    
    def prepare_for_chart(self):
        # --- Gasto por categoría excluyendo salary y uncategorized ---
        df_filtered = self.all_data[
            ~self.all_data["category"].isin(["salary", "uncategorized", "transactions"])
        ].copy()
        df_filtered["amount"] = df_filtered["amount"].abs()
        
        df_category = df_filtered.groupby(["year_month", "category"])["amount"].sum().unstack(fill_value=0)
        
        plt.figure(figsize=(10,6))
        df_category.plot(kind="bar")  # barras separadas por categoría por mes
        plt.title("Gasto por categoría por mes")
        plt.ylabel("Cantidad (€)")
        plt.xlabel("Mes")
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        buffer1 = BytesIO()
        plt.savefig(buffer1, format="png")
        plt.close()
        buffer1.seek(0)
        category_chart = base64.b64encode(buffer1.getvalue()).decode()
        
        # --- Gasto vs ahorro ---
        df_expenses = self.all_data[
            ~self.all_data["category"].isin(["uncategorized", "salary", "transactions"])
        ]
        total_expense = (
            df_expenses["amount"].abs()
            .groupby(df_expenses["year_month"])
            .sum()
        )
        total_expense = df_expenses.groupby("year_month")["amount"].sum().abs()
        
        df_compare = pd.DataFrame({
            "Gasto": total_expense,
            "Ahorro": self.salary - total_expense
        })
        
        plt.figure(figsize=(10,6))
        ax = df_compare.plot(kind="bar", stacked=True, color=["red", "green"])
        plt.title("Gasto vs ahorro mensual")
        plt.ylabel("Cantidad (€)")
        plt.xlabel("Mes")
        plt.tight_layout()

        for i, month in enumerate(df_compare.index):
            gasto = df_compare.loc[month, "Gasto"]
            ahorro = df_compare.loc[month, "Ahorro"]
            
            # Etiqueta del gasto
            ax.text(i, gasto/2, f"{gasto:.0f}€", ha='center', va='center', color='white', fontweight='bold')
            # Etiqueta del ahorro
            ax.text(i, gasto + ahorro/2, f"{ahorro:.0f}€", ha='center', va='center', color='white', fontweight='bold')
        
        buffer2 = BytesIO()
        plt.savefig(buffer2, format="png")
        plt.close()
        buffer2.seek(0)
        compare_chart = base64.b64encode(buffer2.getvalue()).decode()
        
        # Devuelve un diccionario con ambos gráficos
        return {
            "category_chart": category_chart,
            "compare_chart": compare_chart
        }