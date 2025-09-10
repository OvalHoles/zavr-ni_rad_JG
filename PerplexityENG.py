import tkinter as tk
from tkinter import messagebox, font

def calculate_simple_interest(principal, annual_rate, months):
    total_interest = principal * (annual_rate / 100) * (months / 12)
    total_amount = principal + total_interest
    monthly_interest = total_interest / months if months else 0
    return total_interest, total_amount, monthly_interest

def validate_inputs(principal, annual_rate, months):
    if principal < 0:
        raise ValueError("Amount must be non-negative.")
    if annual_rate < 0:
        raise ValueError("Annual Interest Rate must be non-negative.")
    if months <= 0:
        raise ValueError("Duration (months) must be greater than zero.")

def on_calculate():
    try:
        principal = float(entry_amount.get())
        annual_rate = float(entry_rate.get())
        months = int(entry_months.get())
        validate_inputs(principal, annual_rate, months)

        total_interest, total_amount, monthly_interest = calculate_simple_interest(
            principal, annual_rate, months)

        label_total_interest.config(text=f"Total Interest: {total_interest:.2f}")
        label_total_amount.config(text=f"Total Amount after {months} months: {total_amount:.2f}")
        label_monthly_interest.config(text=f"Monthly Interest Amount: {monthly_interest:.2f}")
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

def clear_placeholder(event, entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, tk.END)
        entry.config(fg='black')

def add_placeholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.config(fg='grey')
    entry.bind("<FocusIn>", lambda event: clear_placeholder(event, entry, placeholder))
    entry.bind("<FocusOut>", lambda event: add_placeholder_on_focus_out(event, entry, placeholder))

def add_placeholder_on_focus_out(event, entry, placeholder):
    if entry.get() == '':
        entry.insert(0, placeholder)
        entry.config(fg='grey')

def create_ui():
    root = tk.Tk()
    root.title("Interest Calculator")
    root.geometry("350x350")
    root.resizable(False, False)

    # Fonts
    heading_font = font.Font(root=root, family="Helvetica", size=14, weight="bold")
    result_font = font.Font(root=root, family="Helvetica", size=12)

    # Heading
    tk.Label(root, text="Simple Interest Calculator", font=heading_font).pack(pady=10)

    # Input frame for cleaner group
    input_frame = tk.Frame(root)
    input_frame.pack(pady=10, padx=20, fill='x')

    tk.Label(input_frame, text="Amount:").grid(row=0, column=0, sticky='w', pady=5)
    global entry_amount
    entry_amount = tk.Entry(input_frame)
    entry_amount.grid(row=0, column=1, pady=5)
    add_placeholder(entry_amount, "e.g. 1000")

    tk.Label(input_frame, text="Annual Interest Rate (%):").grid(row=1, column=0, sticky='w', pady=5)
    global entry_rate
    entry_rate = tk.Entry(input_frame)
    entry_rate.grid(row=1, column=1, pady=5)
    add_placeholder(entry_rate, "e.g. 5")

    tk.Label(input_frame, text="Duration (months):").grid(row=2, column=0, sticky='w', pady=5)
    global entry_months
    entry_months = tk.Entry(input_frame)
    entry_months.grid(row=2, column=1, pady=5)
    add_placeholder(entry_months, "e.g. 12")

    tk.Button(root, text="Calculate", command=on_calculate, bg='blue', fg='white').pack(pady=15, ipadx=10, ipady=5)

    # Results frame
    result_frame = tk.Frame(root)
    result_frame.pack(pady=5, padx=20, fill='x')

    global label_total_interest, label_total_amount, label_monthly_interest
    label_total_interest = tk.Label(result_frame, text="Total Interest: ", font=result_font)
    label_total_interest.pack(anchor='w', pady=3)

    label_total_amount = tk.Label(result_frame, text="Total Amount after period: ", font=result_font)
    label_total_amount.pack(anchor='w', pady=3)

    label_monthly_interest = tk.Label(result_frame, text="Monthly Interest Amount: ", font=result_font)
    label_monthly_interest.pack(anchor='w', pady=3)

    return root

if __name__ == "__main__":
    app = create_ui()
    app.mainloop()
