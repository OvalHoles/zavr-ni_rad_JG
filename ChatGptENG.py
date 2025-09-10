import tkinter as tk
from tkinter import ttk, messagebox


class InterestCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💰 Interest Calculator")
        self.root.geometry("400x300")
        self.root.configure(bg="#f4f6f9")
        self.root.resizable(False, False)

        # Variables
        self.amount_var = tk.StringVar()
        self.rate_var = tk.StringVar()
        self.months_var = tk.StringVar()

        self._build_ui()

    def _build_ui(self):
        """Builds the user interface with better styling."""
        # Card container
        card = ttk.Frame(self.root, padding=20, relief="ridge")
        card.place(relx=0.5, rely=0.5, anchor="center")

        # Title
        ttk.Label(card, text="Interest Calculator", font=("Arial", 16, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 15)
        )

        # Input fields
        ttk.Label(card, text="Amount ($):", font=("Arial", 11)).grid(
            row=1, column=0, sticky="e", padx=8, pady=6
        )
        ttk.Entry(card, textvariable=self.amount_var, width=22, font=("Arial", 11)).grid(
            row=1, column=1, pady=6
        )

        ttk.Label(card, text="Annual Interest Rate (%):", font=("Arial", 11)).grid(
            row=2, column=0, sticky="e", padx=8, pady=6
        )
        ttk.Entry(card, textvariable=self.rate_var, width=22, font=("Arial", 11)).grid(
            row=2, column=1, pady=6
        )

        ttk.Label(card, text="Duration (months):", font=("Arial", 11)).grid(
            row=3, column=0, sticky="e", padx=8, pady=6
        )
        ttk.Entry(card, textvariable=self.months_var, width=22, font=("Arial", 11)).grid(
            row=3, column=1, pady=6
        )

        # Buttons
        btns = ttk.Frame(card)
        btns.grid(row=4, column=0, columnspan=2, pady=12)
        ttk.Button(btns, text="Calculate", command=self.calculate_interest).grid(row=0, column=0, padx=6)
        ttk.Button(btns, text="Clear", command=self.clear_fields).grid(row=0, column=1, padx=6)

        # Result label
        self.result_label = ttk.Label(card, text="", font=("Arial", 12), justify="left", foreground="#1a73e8")
        self.result_label.grid(row=5, column=0, columnspan=2, pady=10)

    def calculate_interest(self):
        """Calculate simple interest and show results."""
        try:
            principal = float(self.amount_var.get())
            annual_rate = float(self.rate_var.get())
            months = int(self.months_var.get())

            if principal < 0 or annual_rate < 0 or months <= 0:
                messagebox.showerror("Invalid Input", "Amount and rate must be ≥ 0, months must be > 0.")
                return

            monthly_rate = annual_rate / 100 / 12
            monthly_interest = principal * monthly_rate
            total_interest = monthly_interest * months
            total_amount = principal + total_interest

            self.result_label.config(
                text=(
                    f"Monthly interest: {monthly_interest:,.2f}\n"
                    f"Total interest ({months} months): {total_interest:,.2f}\n"
                    f"Final amount: {total_amount:,.2f}"
                )
            )

        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter numeric values only.")

    def clear_fields(self):
        """Clear inputs and result."""
        self.amount_var.set("")
        self.rate_var.set("")
        self.months_var.set("")
        self.result_label.config(text="")


if __name__ == "__main__":
    root = tk.Tk()
    app = InterestCalculatorApp(root)
    root.mainloop()
