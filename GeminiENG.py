import tkinter as tk
from tkinter import ttk, messagebox

class InterestCalculatorApp:
    """
    A GUI application for calculating simple interest using tkinter with an improved UI.
    This version is organized into a class for better readability and maintainability.
    """
    # --- Styling Constants ---
    BG_COLOR = "#f7f9fa"
    FRAME_BG_COLOR = "#ffffff"
    BUTTON_BG_COLOR = "#007bff"
    BUTTON_ACTIVE_BG = "#0056b3"
    BUTTON_FG_COLOR = "white"
    CLEAR_BUTTON_BG = "#6c757d"
    CLEAR_BUTTON_ACTIVE_BG = "#5a6268"
    RESULT_TEXT_COLOR = "#0056b3"
    FONT_TITLE = ("Helvetica", 16, "bold")
    FONT_LABEL = ("Helvetica", 11)
    FONT_ENTRY = ("Helvetica", 11)
    FONT_RESULT_LABEL = ("Helvetica", 11)
    FONT_RESULT_VALUE = ("Helvetica", 12, "bold")

    def __init__(self, root_window):
        """
        Initializes the application.
        :param root_window: The root tkinter window.
        """
        self.root = root_window
        self._configure_window()
        self._initialize_vars()
        self._create_styles()
        self._create_widgets()
        self._center_window()

    def _configure_window(self):
        """Sets up the main window properties."""
        self.root.title("Interest Calculator")
        self.root.configure(bg=self.BG_COLOR)
        # Set a minimum size for the window
        self.root.minsize(400, 450)

    def _initialize_vars(self):
        """Initializes tkinter StringVars for displaying results."""
        self.result_total_amount_var = tk.StringVar(value="$0.00")
        self.result_total_interest_var = tk.StringVar(value="$0.00")
        self.result_monthly_interest_var = tk.StringVar(value="$0.00")

    def _create_styles(self):
        """Creates custom styles for ttk widgets."""
        style = ttk.Style()
        style.configure('TLabel', background=self.BG_COLOR, font=self.FONT_LABEL)
        style.configure('TFrame', background=self.BG_COLOR)
        style.configure('Card.TFrame', background=self.FRAME_BG_COLOR)
        style.configure('TEntry', font=self.FONT_ENTRY)

    def _create_widgets(self):
        """Creates and places all the UI widgets in the window."""
        main_frame = ttk.Frame(self.root, padding="20 20 20 20")
        main_frame.pack(expand=True, fill="both")

        # --- Title ---
        title_label = ttk.Label(main_frame, text="Simple Interest Calculator", font=self.FONT_TITLE, anchor="center")
        title_label.pack(pady=(0, 20), fill="x")

        # --- Input Frame ---
        input_frame = ttk.Frame(main_frame, style='Card.TFrame', padding=15)
        input_frame.pack(fill="x", expand=True)
        input_frame.columnconfigure(1, weight=1)

        # --- Input Fields ---
        self.principal_entry = self._create_input_field(input_frame, "Principal Amount ($):", 0)
        self.rate_entry = self._create_input_field(input_frame, "Annual Interest Rate (%):", 1)
        self.months_entry = self._create_input_field(input_frame, "Duration (in months):", 2)

        # --- Button Frame ---
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=20, fill="x")
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        # --- Calculate Button ---
        calculate_button = tk.Button(
            button_frame, text="Calculate", command=self._calculate_interest,
            font=("Helvetica", 12, "bold"), bg=self.BUTTON_BG_COLOR, fg=self.BUTTON_FG_COLOR,
            activebackground=self.BUTTON_ACTIVE_BG, activeforeground=self.BUTTON_FG_COLOR,
            relief="flat", borderwidth=0, padx=15, pady=8
        )
        calculate_button.grid(row=0, column=0, sticky="ew", padx=(0, 5))

        # --- Clear Button ---
        clear_button = tk.Button(
            button_frame, text="Clear", command=self._clear_fields,
            font=("Helvetica", 12, "bold"), bg=self.CLEAR_BUTTON_BG, fg=self.BUTTON_FG_COLOR,
            activebackground=self.CLEAR_BUTTON_ACTIVE_BG, activeforeground=self.BUTTON_FG_COLOR,
            relief="flat", borderwidth=0, padx=15, pady=8
        )
        clear_button.grid(row=0, column=1, sticky="ew", padx=(5, 0))

        # --- Results Display ---
        self._create_results_display(main_frame)

    def _create_input_field(self, parent, label_text, row):
        """Helper method to create a label and an entry widget in a grid."""
        label = ttk.Label(parent, text=label_text, style='TLabel')
        label.grid(row=row, column=0, sticky="w", pady=5, padx=5)
        entry = ttk.Entry(parent, style='TEntry', width=25)
        entry.grid(row=row, column=1, sticky="ew", pady=5, padx=5)
        return entry

    def _create_results_display(self, parent):
        """Helper method to create the results frame and labels."""
        results_frame = ttk.Frame(parent, style='Card.TFrame', padding=15)
        results_frame.pack(fill="x", expand=True)
        results_frame.columnconfigure(1, weight=1)

        self._create_result_row(results_frame, "Total Amount:", self.result_total_amount_var, 0)
        self._create_result_row(results_frame, "Total Interest:", self.result_total_interest_var, 1)
        self._create_result_row(results_frame, "Average Monthly Interest:", self.result_monthly_interest_var, 2)

    def _create_result_row(self, parent, label_text, text_variable, row):
        """Helper method to create a single row in the results display."""
        label = ttk.Label(parent, text=label_text, font=self.FONT_RESULT_LABEL, style='TLabel')
        label.grid(row=row, column=0, sticky="w", pady=4, padx=5)
        
        value_display = ttk.Label(parent, textvariable=text_variable, font=self.FONT_RESULT_VALUE, foreground=self.RESULT_TEXT_COLOR, anchor="e")
        value_display.grid(row=row, column=1, sticky="e", pady=4, padx=5)

    def _calculate_interest(self):
        """
        Validates input, calculates simple interest, and updates the display.
        """
        try:
            principal = float(self.principal_entry.get())
            annual_rate = float(self.rate_entry.get())
            months = int(self.months_entry.get())

            if principal < 0 or annual_rate < 0 or months <= 0:
                messagebox.showerror("Input Error", "Please enter positive values. Duration must be greater than 0.")
                return

            total_interest = principal * (annual_rate / 100) * (months / 12)
            total_amount = principal + total_interest
            monthly_interest_amount = total_interest / months

            self.result_total_amount_var.set(f"${total_amount:,.2f}")
            self.result_total_interest_var.set(f"${total_interest:,.2f}")
            self.result_monthly_interest_var.set(f"${monthly_interest_amount:,.2f}")

        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers in all fields.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def _clear_fields(self):
        """Clears all input and result fields."""
        self.principal_entry.delete(0, tk.END)
        self.rate_entry.delete(0, tk.END)
        self.months_entry.delete(0, tk.END)
        self.result_total_amount_var.set("$0.00")
        self.result_total_interest_var.set("$0.00")
        self.result_monthly_interest_var.set("$0.00")
        # Set focus back to the first entry field
        self.principal_entry.focus_set()
        
    def _center_window(self):
        """Centers the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

if __name__ == "__main__":
    # --- Set up and run the application ---
    root = tk.Tk()
    app = InterestCalculatorApp(root)
    root.mainloop()
