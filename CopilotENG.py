import tkinter as tk
from tkinter import ttk, messagebox


class InterestCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💰 Monthly Interest Calculator")
        self.root.geometry("400x320")
        self.root.resizable(False, False)

        self._setup_style()
        self._create_widgets()

    def _setup_style(self):
        style = ttk.Style()
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 12, "bold"))
        style.configure("Result.TLabel", font=("Segoe UI", 10, "bold"), foreground="#007700")
        style.configure("TButton", font=("Segoe UI", 10))

    def _create_widgets(self):
        # Title
        ttk.Label(self.root, text="Monthly Interest Calculator", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=10)

        # Input Fields
        self._add_label("Amount (€):", 1)
        self.amount_entry = self._add_entry(1)

        self._add_label("Annual Interest Rate (%):", 2)
        self.rate_entry = self._add_entry(2)

        self._add_label("Duration (months):", 3)
        self.duration_entry = self._add_entry(3)

        # Calculate Button
        ttk.Button(self.root, text="Calculate", command=self.calculate_interest).grid(row=4, column=0, columnspan=2, pady=15)

        # Results
        self.monthly_result = self._add_result_label("Monthly Interest:", 5)
        self.total_interest_result = self._add_result_label("Total Interest:", 6)
        self.final_amount_result = self._add_result_label("Final Amount:", 7)

        # Autofocus
        self.amount_entry.focus()

    def _add_label(self, text, row):
        ttk.Label(self.root, text=text).grid(row=row, column=0, sticky="e", padx=10, pady=5)

    def _add_entry(self, row):
        entry = ttk.Entry(self.root, width=20)
        entry.grid(row=row, column=1, padx=10, pady=5)
        return entry

    def _add_result_label(self, text, row):
        label = ttk.Label(self.root, text=text, style="Result.TLabel")
        label.grid(row=row, column=0, columnspan=2, pady=3)
        return label

    def calculate_interest(self):
        try:
            principal = float(self.amount_entry.get())
            annual_rate = float(self.rate_entry.get())
            months = int(self.duration_entry.get())

            # Validation: Check for negative or zero values
            if principal <= 0 or annual_rate <= 0 or months <= 0:
                messagebox.showerror("Input Error", "All values must be positive numbers.")
                return

            # Convert annual rate to decimal
            annual_rate /= 100
            monthly_rate = annual_rate / 12
            monthly_interest = principal * monthly_rate
            total_interest = monthly_interest * months
            total_amount = principal + total_interest

            self.monthly_result.config(text=f"Monthly Interest: €{monthly_interest:.2f}")
            self.total_interest_result.config(text=f"Total Interest: €{total_interest:.2f}")
            self.final_amount_result.config(text=f"Final Amount After {months} Months: €{total_amount:.2f}")

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values.")


if __name__ == "__main__":
    root = tk.Tk()
    app = InterestCalculatorApp(root)
    root.mainloop()
