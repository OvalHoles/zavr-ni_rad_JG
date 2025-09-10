import tkinter as tk
from tkinter import ttk, messagebox
from typing import Tuple, Optional
from dataclasses import dataclass
import math


@dataclass
class InterestResult:
    """Data class to hold interest calculation results."""
    total_interest: float
    monthly_interest: float
    final_amount: float


@dataclass
class SavingsResult:
    """Data class to hold savings calculation results."""
    monthly_savings_required: float


class InterestCalculations:
    """Handles all interest and savings calculations."""
    
    @staticmethod
    def calculate_simple_interest(principal: float, annual_rate: float, months: int) -> InterestResult:
        """
        Calculate simple interest for given parameters.
        
        Args:
            principal: Initial amount invested
            annual_rate: Annual interest rate as percentage (e.g., 6 for 6%)
            months: Duration in months
            
        Returns:
            InterestResult containing calculation results
            
        Raises:
            ValueError: If any parameter is invalid
        """
        if principal <= 0:
            raise ValueError("Principal amount must be positive")
        if annual_rate < 0:
            raise ValueError("Interest rate cannot be negative")
        if months <= 0:
            raise ValueError("Duration must be positive")
            
        # Convert percentage to decimal and months to years
        rate_decimal = annual_rate / 100
        years = months / 12
        
        # Simple Interest: SI = P * R * T
        total_interest = principal * rate_decimal * years
        monthly_interest = total_interest / months
        final_amount = principal + total_interest
        
        return InterestResult(total_interest, monthly_interest, final_amount)
    
    @staticmethod
    def calculate_monthly_savings(target_amount: float, annual_rate: float, months: int) -> SavingsResult:
        """
        Calculate required monthly savings to reach target amount with compound interest.
        
        Args:
            target_amount: Desired final amount
            annual_rate: Annual interest rate as percentage
            months: Duration in months
            
        Returns:
            SavingsResult containing monthly savings required
            
        Raises:
            ValueError: If any parameter is invalid
        """
        if target_amount <= 0:
            raise ValueError("Target amount must be positive")
        if annual_rate < 0:
            raise ValueError("Interest rate cannot be negative")
        if months <= 0:
            raise ValueError("Duration must be positive")
            
        # Convert annual rate to monthly rate
        monthly_rate = (annual_rate / 100) / 12
        
        if monthly_rate == 0:
            # No interest case - simple division
            monthly_savings = target_amount / months
        else:
            # Future value of annuity formula: FV = PMT * [((1 + r)^n - 1) / r]
            # Solving for PMT: PMT = FV / [((1 + r)^n - 1) / r]
            factor = ((1 + monthly_rate) ** months - 1) / monthly_rate
            monthly_savings = target_amount / factor
            
        return SavingsResult(monthly_savings)


class UIConstants:
    """Constants for UI configuration."""
    WINDOW_WIDTH = 520
    WINDOW_HEIGHT = 650
    PADDING = 25
    SECTION_PADDING = 15
    ENTRY_WIDTH = 18
    
    # Colors
    PRIMARY_COLOR = "#2E86AB"
    SUCCESS_COLOR = "#28A745"
    WARNING_COLOR = "#FFC107"
    BACKGROUND_COLOR = "#F8F9FA"
    CARD_COLOR = "#FFFFFF"
    TEXT_COLOR = "#343A40"
    ACCENT_COLOR = "#6C757D"
    
    # Fonts
    TITLE_FONT = ("Segoe UI", 18, "bold")
    SUBTITLE_FONT = ("Segoe UI", 12, "bold")
    LABEL_FONT = ("Segoe UI", 10)
    RESULT_FONT = ("Segoe UI", 11, "bold")
    SMALL_FONT = ("Segoe UI", 9)
    
    # Text labels
    TITLE = "💰 Interest Calculator"
    SUBTITLE_SAVINGS = "🎯 Monthly Savings Calculator"
    
    # Tooltips
    TOOLTIPS = {
        'principal': "Enter the initial amount you want to invest or save",
        'rate': "Enter the annual interest rate as a percentage (e.g., 5.5 for 5.5%)",
        'duration': "Enter the number of months for your investment or savings period",
        'target': "Enter the amount you want to accumulate by the end of the period"
    }


class ToolTip:
    """Creates a tooltip for a given widget."""
    
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0
        
        self.widget.bind('<Enter>', self.on_enter)
        self.widget.bind('<Leave>', self.on_leave)
    
    def on_enter(self, event=None):
        self.show_tip()
    
    def on_leave(self, event=None):
        self.hide_tip()
    
    def show_tip(self):
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + cy + self.widget.winfo_rooty() + 25
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                        background="#FFFFE0", relief=tk.SOLID, borderwidth=1,
                        font=UIConstants.SMALL_FONT, wraplength=200)
        label.pack(ipadx=5, ipady=3)
    
    def hide_tip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


class InputValidator:
    """Handles input validation for the calculator."""
    
    @staticmethod
    def validate_and_convert(value: str, field_name: str, allow_zero: bool = False) -> float:
        """
        Validate and convert string input to float.
        
        Args:
            value: String value to validate
            field_name: Name of the field for error messages
            allow_zero: Whether zero values are allowed
            
        Returns:
            Validated float value
            
        Raises:
            ValueError: If validation fails
        """
        if not value.strip():
            raise ValueError(f"{field_name} is required")
            
        try:
            num_value = float(value.strip())
        except ValueError:
            raise ValueError(f"{field_name} must be a valid number")
            
        if not allow_zero and num_value <= 0:
            raise ValueError(f"{field_name} must be positive")
        elif allow_zero and num_value < 0:
            raise ValueError(f"{field_name} cannot be negative")
            
        return num_value


class InterestCalculatorGUI:
    """Main GUI class for the Interest Calculator application."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.calculator = InterestCalculations()
        self.validator = InputValidator()
        
        self._setup_window()
        self._configure_styles()
        self._create_variables()
        self._create_widgets()
        self._setup_tooltips()
        
    def _setup_window(self) -> None:
        """Configure the main window."""
        self.root.title("Interest Calculator")
        self.root.geometry(f"{UIConstants.WINDOW_WIDTH}x{UIConstants.WINDOW_HEIGHT}")
        self.root.resizable(True, True)
        self.root.configure(bg=UIConstants.BACKGROUND_COLOR)
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (UIConstants.WINDOW_WIDTH // 2)
        y = (self.root.winfo_screenheight() // 2) - (UIConstants.WINDOW_HEIGHT // 2)
        self.root.geometry(f"{UIConstants.WINDOW_WIDTH}x{UIConstants.WINDOW_HEIGHT}+{x}+{y}")
        
        # Configure grid weights for responsiveness
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
    def _configure_styles(self) -> None:
        """Configure custom styles for ttk widgets."""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure custom styles
        self.style.configure('Title.TLabel', font=UIConstants.TITLE_FONT, 
                           foreground=UIConstants.PRIMARY_COLOR)
        self.style.configure('Subtitle.TLabel', font=UIConstants.SUBTITLE_FONT, 
                           foreground=UIConstants.TEXT_COLOR)
        self.style.configure('Result.TLabel', font=UIConstants.RESULT_FONT, 
                           foreground=UIConstants.SUCCESS_COLOR)
        self.style.configure('Card.TFrame', background=UIConstants.CARD_COLOR, 
                           relief='raised', borderwidth=1)
        self.style.configure('Primary.TButton', font=UIConstants.LABEL_FONT)
        self.style.configure('Clear.TButton', font=UIConstants.LABEL_FONT)
        
        # Configure entry styles
        self.style.configure('Custom.TEntry', font=UIConstants.LABEL_FONT, 
                           fieldbackground='white')
        
    def _create_variables(self) -> None:
        """Create tkinter variables for form inputs."""
        self.principal_var = tk.StringVar()
        self.rate_var = tk.StringVar()
        self.duration_var = tk.StringVar()
        self.target_var = tk.StringVar()
        
        # Add validation to entries
        vcmd = (self.root.register(self._validate_number), '%P')
        self.validation_command = vcmd
        
    def _validate_number(self, value: str) -> bool:
        """Validate numeric input in real-time."""
        if value == "":
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False
            
    def _create_widgets(self) -> None:
        """Create and layout all GUI widgets."""
        # Create scrollable main frame
        self.canvas = tk.Canvas(self.root, bg=UIConstants.BACKGROUND_COLOR, highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.main_frame = ttk.Frame(self.canvas)
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")
        
        # Pack canvas and scrollbar
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Bind events for scrolling
        self.main_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.canvas.bind("<MouseWheel>", self._on_mousewheel)
        
        self._create_content()
        
    def _on_frame_configure(self, event=None):
        """Update scroll region when frame size changes."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def _on_canvas_configure(self, event=None):
        """Update frame width when canvas size changes."""
        canvas_width = self.canvas.winfo_width()
        self.canvas.itemconfig(self.canvas.find_all()[0], width=canvas_width)
        
    def _on_mousewheel(self, event):
        """Handle mouse wheel scrolling."""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
    def _create_content(self) -> None:
        """Create the main content."""
        # Add padding to main frame
        self.main_frame.configure(padding=UIConstants.PADDING)
        
        self._create_title()
        self._create_input_section()
        self._create_results_section()
        self._create_separator()
        self._create_savings_section()
        self._create_action_buttons()
        
    def _create_title(self) -> None:
        """Create the main title."""
        title_frame = ttk.Frame(self.main_frame)
        title_frame.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="ew")
        
        title_label = ttk.Label(
            title_frame, 
            text=UIConstants.TITLE, 
            style='Title.TLabel'
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            title_frame,
            text="Calculate your investment returns with ease",
            font=UIConstants.SMALL_FONT,
            foreground=UIConstants.ACCENT_COLOR
        )
        subtitle_label.pack(pady=(5, 0))
        
    def _create_input_section(self) -> None:
        """Create the input form section."""
        input_frame = ttk.LabelFrame(
            self.main_frame, 
            text=" 📊 Investment Details ", 
            style='Card.TFrame',
            padding=UIConstants.SECTION_PADDING
        )
        input_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        
        # Configure grid weights
        input_frame.columnconfigure(1, weight=1)
        
        row = 0
        
        # Principal amount
        self._create_input_row(
            input_frame, row, "💵 Principal Amount ($):", 
            self.principal_var, "Enter initial investment amount"
        )
        
        # Interest rate
        row += 1
        self._create_input_row(
            input_frame, row, "📈 Annual Interest Rate (%):", 
            self.rate_var, "Enter annual interest rate"
        )
        
        # Duration
        row += 1
        self._create_input_row(
            input_frame, row, "📅 Duration (months):", 
            self.duration_var, "Enter investment period in months"
        )
        
        # Calculate button
        row += 1
        self.calc_button = ttk.Button(
            input_frame, 
            text="🔢 Calculate Interest", 
            command=self._calculate_interest,
            style='Primary.TButton'
        )
        self.calc_button.grid(row=row, column=0, columnspan=2, pady=(15, 0), sticky="ew")
        
    def _create_input_row(self, parent: ttk.Frame, row: int, label_text: str, 
                         variable: tk.StringVar, placeholder: str) -> None:
        """Create a single input row with label and entry."""
        # Label
        label = ttk.Label(parent, text=label_text, font=UIConstants.LABEL_FONT)
        label.grid(row=row, column=0, sticky="w", pady=(5, 5), padx=(0, 10))
        
        # Entry with placeholder effect
        entry = ttk.Entry(
            parent, 
            textvariable=variable, 
            width=UIConstants.ENTRY_WIDTH,
            style='Custom.TEntry',
            validate='key',
            validatecommand=self.validation_command
        )
        entry.grid(row=row, column=1, sticky="ew", pady=(5, 5))
        
        # Store entry reference for placeholder functionality
        setattr(self, f"entry_{row}", entry)
        
    def _create_results_section(self) -> None:
        """Create the results display section."""
        self.results_frame = ttk.LabelFrame(
            self.main_frame, 
            text=" 📋 Calculation Results ", 
            style='Card.TFrame',
            padding=UIConstants.SECTION_PADDING
        )
        self.results_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        self.results_frame.columnconfigure(1, weight=1)
        
        # Initially hide results
        self.results_frame.grid_remove()
        
        # Create result rows
        self._create_result_row(self.results_frame, 0, "💰 Total Interest Earned:", "interest_result")
        self._create_result_row(self.results_frame, 1, "📅 Monthly Interest:", "monthly_interest_result")
        self._create_result_row(self.results_frame, 2, "🎯 Final Amount:", "total_result")
        
        # Add summary section
        self._create_summary_section()
        
    def _create_result_row(self, parent: ttk.Frame, row: int, label_text: str, attr_name: str) -> None:
        """Create a single result row with label and value."""
        label = ttk.Label(parent, text=label_text, font=UIConstants.LABEL_FONT)
        label.grid(row=row, column=0, sticky="w", pady=(5, 5), padx=(0, 10))
        
        result_label = ttk.Label(parent, text="$0.00", style='Result.TLabel')
        result_label.grid(row=row, column=1, sticky="e", pady=(5, 5))
        setattr(self, attr_name, result_label)
        
    def _create_summary_section(self) -> None:
        """Create a summary section with key insights."""
        summary_frame = ttk.Frame(self.results_frame)
        summary_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(10, 0))
        summary_frame.columnconfigure(0, weight=1)
        
        self.summary_label = ttk.Label(
            summary_frame,
            text="",
            font=UIConstants.SMALL_FONT,
            foreground=UIConstants.ACCENT_COLOR,
            wraplength=400,
            justify="center"
        )
        self.summary_label.grid(row=0, column=0, pady=(5, 0))
        
    def _create_separator(self) -> None:
        """Create a visual separator."""
        separator = ttk.Separator(self.main_frame, orient='horizontal')
        separator.grid(row=3, column=0, columnspan=2, sticky="ew", pady=20)
        
    def _create_savings_section(self) -> None:
        """Create the monthly savings calculator section."""
        savings_frame = ttk.LabelFrame(
            self.main_frame, 
            text=" 🎯 Monthly Savings Calculator ", 
            style='Card.TFrame',
            padding=UIConstants.SECTION_PADDING
        )
        savings_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, 15))
        savings_frame.columnconfigure(1, weight=1)
        
        # Description
        desc_label = ttk.Label(
            savings_frame,
            text="Calculate how much to save monthly to reach your target amount",
            font=UIConstants.SMALL_FONT,
            foreground=UIConstants.ACCENT_COLOR
        )
        desc_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Target amount input
        self._create_input_row(
            savings_frame, 1, "🎯 Target Amount ($):", 
            self.target_var, "Enter your savings goal"
        )
        
        # Calculate button
        self.savings_calc_button = ttk.Button(
            savings_frame, 
            text="💡 Calculate Monthly Savings", 
            command=self._calculate_monthly_savings,
            style='Primary.TButton'
        )
        self.savings_calc_button.grid(row=2, column=0, columnspan=2, pady=(15, 10), sticky="ew")
        
        # Result
        self._create_result_row(savings_frame, 3, "💳 Required Monthly Savings:", "monthly_savings_result")
        
    def _create_action_buttons(self) -> None:
        """Create action buttons."""
        button_frame = ttk.Frame(self.main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(15, 0), sticky="ew")
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        
        # Clear button
        clear_button = ttk.Button(
            button_frame, 
            text="🗑️ Clear All", 
            command=self._clear_all,
            style='Clear.TButton'
        )
        clear_button.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        
        # Example button
        example_button = ttk.Button(
            button_frame, 
            text="💡 Load Example", 
            command=self._load_example
        )
        example_button.grid(row=0, column=1, padx=(5, 0), sticky="ew")
        
    def _setup_tooltips(self) -> None:
        """Setup tooltips for better user guidance."""
        # Will be set up after widgets are created
        pass
        
    def _calculate_interest(self) -> None:
        """Handle interest calculation with enhanced feedback."""
        try:
            # Validate inputs
            principal = self.validator.validate_and_convert(
                self.principal_var.get(), "Principal amount"
            )
            rate = self.validator.validate_and_convert(
                self.rate_var.get(), "Interest rate", allow_zero=True
            )
            duration = int(self.validator.validate_and_convert(
                self.duration_var.get(), "Duration"
            ))
            
            # Calculate results
            result = self.calculator.calculate_simple_interest(principal, rate, duration)
            
            # Update UI with animation effect
            self._update_interest_results(result, principal, rate, duration)
            
            # Show results frame
            self.results_frame.grid()
            
            # Scroll to results
            self.root.after(100, lambda: self.canvas.yview_moveto(0.5))
            
        except ValueError as e:
            self._show_error("Input Error", str(e))
        except Exception as e:
            self._show_error("Calculation Error", f"An unexpected error occurred: {str(e)}")
            
    def _calculate_monthly_savings(self) -> None:
        """Handle monthly savings calculation with enhanced feedback."""
        try:
            # Validate inputs
            target = self.validator.validate_and_convert(
                self.target_var.get(), "Target amount"
            )
            rate = self.validator.validate_and_convert(
                self.rate_var.get(), "Interest rate", allow_zero=True
            )
            duration = int(self.validator.validate_and_convert(
                self.duration_var.get(), "Duration"
            ))
            
            # Calculate results
            result = self.calculator.calculate_monthly_savings(target, rate, duration)
            
            # Update UI
            self.monthly_savings_result.config(text=f"${result.monthly_savings_required:.2f}")
            
        except ValueError as e:
            self._show_error("Input Error", str(e))
        except Exception as e:
            self._show_error("Calculation Error", f"An unexpected error occurred: {str(e)}")
            
    def _update_interest_results(self, result: InterestResult, principal: float, rate: float, duration: int) -> None:
        """Update the interest calculation results with enhanced information."""
        self.interest_result.config(text=f"${result.total_interest:.2f}")
        self.monthly_interest_result.config(text=f"${result.monthly_interest:.2f}")
        self.total_result.config(text=f"${result.final_amount:.2f}")
        
        # Update summary
        roi = (result.total_interest / principal) * 100
        years = duration / 12
        summary_text = f"Your investment will grow by {roi:.1f}% over {years:.1f} year(s), earning ${result.total_interest:.2f} in interest."
        self.summary_label.config(text=summary_text)
        
    def _show_error(self, title: str, message: str) -> None:
        """Show error message with custom styling."""
        messagebox.showerror(title, message, parent=self.root)
        
    def _load_example(self) -> None:
        """Load example values for demonstration."""
        self.principal_var.set("10000")
        self.rate_var.set("5.5")
        self.duration_var.set("24")
        self.target_var.set("15000")
        
        # Auto-calculate
        self.root.after(100, self._calculate_interest)
        
    def _clear_all(self) -> None:
        """Clear all input fields and results with confirmation."""
        # Clear inputs
        self.principal_var.set("")
        self.rate_var.set("")
        self.duration_var.set("")
        self.target_var.set("")
        
        # Clear results
        self.interest_result.config(text="$0.00")
        self.monthly_interest_result.config(text="$0.00")
        self.total_result.config(text="$0.00")
        self.monthly_savings_result.config(text="$0.00")
        self.summary_label.config(text="")
        
        # Hide results frame
        self.results_frame.grid_remove()


def main() -> None:
    """Main entry point for the application."""
    root = tk.Tk()
    app = InterestCalculatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()