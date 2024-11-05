import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import re  # For input validation

# Database connection details
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Parthsam@5',
    'database': 'Preet'
}

class FinancialTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Financial Transaction Tracker")
        self.root.geometry("800x500")
        self.root.configure(bg="#EAEAEA")  # Light grey background
        
        # Configure styles for better aesthetics
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background="#B0C4DE")  # Light steel blue for the tabs
        style.configure("TNotebook.Tab", font=("Arial", 12, "bold"), padding=[10, 5], background="#87CEFA", foreground="black")  # Sky blue for tabs
        style.map("TNotebook.Tab", background=[("active", "#87CEFA")])  # Change tab color on active
        style.configure("TButton", background="#4682B4", foreground="white", font=("Arial", 10, "bold"))  # Steel blue for buttons
        style.configure("TLabel", background="#EAEAEA", font=("Arial", 10), padding=5)  # Grey for labels
        style.configure("TEntry", font=("Arial", 10), padding=5)  # Entry field font

        # Connect to the database
        self.connect_to_database()

        # Tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=10)

        # Create tabs
        self.create_add_transaction_tab()
        self.create_monthly_report_tab()
        self.create_category_breakdown_tab()

    def connect_to_database(self):
        """ Connect to the MySQL database. """
        try:
            self.conn = mysql.connector.connect(**db_config)
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error connecting to the database: {err}")
            self.root.destroy()

    def create_add_transaction_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Add Transaction")

        title_label = tk.Label(tab, text="Add a New Transaction", font=("Arial", 14, "bold"), bg="#B0C4DE")
        title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

        tk.Label(tab, text="Date (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.date_entry = ttk.Entry(tab, width=30)
        self.date_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(tab, text="Amount:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.amount_entry = ttk.Entry(tab, width=30)
        self.amount_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(tab, text="Category ID:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.category_id_entry = ttk.Entry(tab, width=30)
        self.category_id_entry.grid(row=3, column=1, padx=10, pady=10)

        tk.Label(tab, text="Description:").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        self.description_entry = ttk.Entry(tab, width=30)
        self.description_entry.grid(row=4, column=1, padx=10, pady=10)

        add_button = ttk.Button(tab, text="Add Transaction", command=self.add_transaction)
        add_button.grid(row=5, column=0, columnspan=2, pady=20)

    def add_transaction(self):
        date = self.date_entry.get()
        amount = self.amount_entry.get()
        category_id = self.category_id_entry.get()
        description = self.description_entry.get()

        # Validate input
        if not self.validate_input(date, amount, category_id):
            return

        try:
            query = """
                INSERT INTO Transactions (transaction_date, amount, category_id, description)
                VALUES (%s, %s, %s, %s)
            """
            self.cursor.execute(query, (date, float(amount), int(category_id), description))
            self.conn.commit()
            messagebox.showinfo("Success", "Transaction added successfully!")
            self.clear_input_fields()  # Clear fields after successful addition
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to add transaction: {err}")

    def validate_input(self, date, amount, category_id):
        """ Validate user input for date, amount, and category ID. """
        if not re.match(r'\d{4}-\d{2}-\d{2}', date):
            messagebox.showerror("Input Error", "Date must be in YYYY-MM-DD format.")
            return False
        if not re.match(r'^\d+(\.\d{1,2})?$', amount):  # Matches decimal numbers
            messagebox.showerror("Input Error", "Amount must be a valid number.")
            return False
        if not category_id.isdigit():
            messagebox.showerror("Input Error", "Category ID must be a number.")
            return False
        return True

    def clear_input_fields(self):
        """ Clear input fields after adding a transaction. """
        self.date_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.category_id_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)

    def create_monthly_report_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Monthly Spending Report")

        title_label = tk.Label(tab, text="Monthly Spending Report", font=("Arial", 14, "bold"), bg="#B0C4DE")
        title_label.pack(pady=(10, 20))

        report_button = ttk.Button(tab, text="Generate Monthly Report", command=self.monthly_spending_report)
        report_button.pack(pady=10)

        self.report_text = tk.Text(tab, height=15, width=60, font=("Arial", 10), bg="#EAEAEA")
        self.report_text.pack(padx=10, pady=10)

    def monthly_spending_report(self):
        try:
            query = """
                SELECT DATE_FORMAT(transaction_date, '%Y-%m') AS month, SUM(amount) AS total_spent
                FROM Transactions
                GROUP BY month
                ORDER BY month DESC
            """
            self.cursor.execute(query)
            result = self.cursor.fetchall()

            # Format the report manually instead of using pandas
            report = "Monthly Spending Report:\n\n"
            report += "{:<15} {:<15}\n".format("Month", "Total Spent")
            report += "-" * 30 + "\n"
            for row in result:
                report += "{:<15} ${:<15.2f}\n".format(row[0], row[1])

            self.report_text.delete(1.0, tk.END)  # Clear previous report
            self.report_text.insert(tk.END, report)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to retrieve monthly report: {err}")

    def create_category_breakdown_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Category Breakdown Report")

        title_label = tk.Label(tab, text="Category Breakdown Report", font=("Arial", 14, "bold"), bg="#B0C4DE")
        title_label.pack(pady=(10, 20))

        tk.Label(tab, text="Month (YYYY-MM):").pack(pady=5)
        self.month_entry = ttk.Entry(tab, width=30)
        self.month_entry.pack(pady=5)

        breakdown_button = ttk.Button(tab, text="Generate Category Breakdown", command=self.category_breakdown_report)
        breakdown_button.pack(pady=10)

        self.breakdown_text = tk.Text(tab, height=15, width=60, font=("Arial", 10), bg="#EAEAEA")
        self.breakdown_text.pack(padx=10, pady=10)

    def category_breakdown_report(self):
        month = self.month_entry.get()
        try:
            query = """
                SELECT c.category_name, SUM(t.amount) AS total_spent
                FROM Transactions t
                JOIN Categories c ON t.category_id = c.category_id
                WHERE DATE_FORMAT(t.transaction_date, '%Y-%m') = %s
                GROUP BY c.category_name
                ORDER BY total_spent DESC  # Sort by total spent
            """
            self.cursor.execute(query, (month,))
            result = self.cursor.fetchall()

            # Format the breakdown manually
            breakdown = f"Spending Breakdown for {month}:\n\n"
            breakdown += "{:<20} {:<15}\n".format("Category", "Total Spent")
            breakdown += "-" * 35 + "\n"
            for row in result:
                breakdown += "{:<20} ${:<15.2f}\n".format(row[0], row[1])

            self.breakdown_text.delete(1.0, tk.END)  # Clear previous report
            self.breakdown_text.insert(tk.END, breakdown)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to retrieve category breakdown: {err}")

    def close(self):
        """ Ensure resources are released. """
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        self.root.destroy()

def run_app():
    root = tk.Tk()
    app = FinancialTrackerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close)  # Close the app properly when the window is closed
    root.mainloop()

# Use run_app() to launch the application.
run_app()
