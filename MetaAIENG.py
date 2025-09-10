import tkinter as tk
from tkinter import messagebox

class InterestCalculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Interest Calculator")
        self.create_widgets()

    def create_widgets(self):
        # Header
        header_label = tk.Label(self.window, text="Interest Calculator", font=("Arial", 18))
        header_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        # Input fields
        input_frame = tk.Frame(self.window)
        input_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        tk.Label(input_frame, text="Principal Amount:").grid(row=0, column=0, padx=5, pady=5)
        self.amount_entry = tk.Entry(input_frame, width=20)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Annual Interest Rate (%):").grid(row=1, column=0, padx=5, pady=5)
        self.interest_rate_entry = tk.Entry(input_frame, width=20)
        self.interest_rate_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Savings Duration (months):").grid(row=2, column=0, padx=5, pady=5)
        self.duration_entry = tk.Entry(input_frame, width=20)
        self.duration_entry.grid(row=2, column=1, padx=5, pady=5)

        # Buttons
        button_frame = tk.Frame(self.window)
        button_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        calculate_button = tk.Button(button_frame, text="Calculate", command=self.calculate_interest)
        calculate_button.grid(row=0, column=0, padx=5, pady=5)

        clear_button = tk.Button(button_frame, text="Clear", command=self.clear_fields)
        clear_button.grid(row=0, column=1, padx=5, pady=5)

        # Output fields
        output_frame = tk.Frame(self.window)
        output_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        tk.Label(output_frame, text="Total Amount after period:").grid(row=0, column=0, padx=5, pady=5)
        self.total_amount_result = tk.Label(output_frame, text="")
        self.total_amount_result.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(output_frame, text="Total Interest:").grid(row=1, column=0, padx=5, pady=5)
        self.total_interest_result = tk.Label(output_frame, text="")
        self.total_interest_result.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(output_frame, text="Monthly Interest:").grid(row=2, column=0, padx=5, pady=5)
        self.monthly_interest_result = tk.Label(output_frame, text="")
        self.monthly_interest_result.grid(row=2, column=1, padx=5, pady=5)

    def calculate_interest(self):
        try:
            amount = float(self.amount_entry.get())
            interest_rate = float(self.interest_rate_entry.get()) / 100
            duration = int(self.duration_entry.get())

            if amount <= 0:
                messagebox.showerror("Error", "Principal Amount must be greater than zero.")
                return
            if interest_rate < 0:
                messagebox.showerror("Error", "Annual Interest Rate cannot be negative.")
                return
            if duration <= 0:
                messagebox.showerror("Error", "Savings Duration must be greater than zero.")
                return

            total_interest = amount * interest_rate * (duration / 12)
            total_amount = amount + total_interest
            monthly_interest = total_interest / duration

            self.total_amount_result.config(text=f"{total_amount:.2f}")
            self.total_interest_result.config(text=f"{total_interest:.2f}")
            self.monthly_interest_result.config(text=f"{monthly_interest:.2f}")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid numbers.")

    def clear_fields(self):
        self.amount_entry.delete(0, tk.END)
        self.interest_rate_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)
        self.total_amount_result.config(text="")
        self.total_interest_result.config(text="")
        self.monthly_interest_result.config(text="")

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = InterestCalculator()
    app.run()