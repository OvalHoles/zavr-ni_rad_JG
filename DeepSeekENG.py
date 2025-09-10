import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Tuple
import tkinter.font as tkfont


class Theme:
    """Centralized theme configuration"""
    COLORS = {
        'primary': '#2563eb',
        'primary_hover': '#1d4ed8',
        'secondary': '#64748b',
        'success': '#16a34a',
        'warning': '#ea580c',
        'error': '#dc2626',
        'background': '#f8fafc',
        'card_bg': '#ffffff',
        'text_primary': '#1e293b',
        'text_secondary': '#64748b',
        'border': '#e2e8f0',
        'button_text': '#ffffff'
    }
    
    FONTS = {
        'title': ('Segoe UI', 16, 'bold'),
        'heading': ('Segoe UI', 12, 'bold'),
        'body': ('Segoe UI', 10),
        'button': ('Segoe UI', 10, 'bold'),
        'result': ('Segoe UI', 11, 'bold')
    }


class InterestCalculator:
    """Handles the interest calculation logic"""
    
    @staticmethod
    def calculate_simple_interest(principal: float, annual_rate: float, 
                                 months: int, monthly_deposit: float = 0) -> Tuple[float, float, float]:
        """
        Calculate simple interest and related amounts
        
        Args:
            principal: Initial amount
            annual_rate: Annual interest rate in percentage
            months: Duration in months
            monthly_deposit: Optional monthly deposit amount
            
        Returns:
            Tuple of (total_interest, total_amount, monthly_interest)
        """
        if any(val <= 0 for val in [principal, annual_rate, months]) or monthly_deposit < 0:
            raise ValueError("All values must be positive")
        
        years = months / 12
        principal_interest = principal * (annual_rate / 100) * years
        total_interest = principal_interest
        
        # Calculate interest from monthly deposits
        if monthly_deposit > 0:
            for month in range(months):
                remaining_months = months - month
                remaining_years = remaining_months / 12
                deposit_interest = monthly_deposit * (annual_rate / 100) * remaining_years
                total_interest += deposit_interest
        
        total_deposits = principal + (monthly_deposit * months)
        total_amount = total_deposits + total_interest
        average_monthly_interest = total_interest / months
        
        return round(total_interest, 2), round(total_amount, 2), round(average_monthly_interest, 2)


class InputValidator:
    """Handles input validation"""
    
    @staticmethod
    def validate_inputs(amount: str, rate: str, duration: str, monthly: str) -> Tuple[float, float, int, float]:
        """
        Validate and convert input strings to appropriate types
        
        Args:
            amount: Principal amount string
            rate: Annual rate string
            duration: Duration string
            monthly: Monthly deposit string
            
        Returns:
            Tuple of validated (principal, annual_rate, months, monthly_deposit)
        """
        try:
            principal = float(amount)
            annual_rate = float(rate)
            months = int(duration)
            monthly_deposit = float(monthly) if monthly else 0.0
            
            if principal <= 0 or annual_rate <= 0 or months <= 0 or monthly_deposit < 0:
                raise ValueError("All values must be positive numbers")
                
            return principal, annual_rate, months, monthly_deposit
            
        except ValueError as e:
            raise ValueError("Please enter valid positive numbers") from e


class ResultsDisplay:
    """Handles results display updates with visual enhancements"""
    
    def __init__(self, interest_label: ttk.Label, total_label: ttk.Label, 
                 monthly_interest_label: ttk.Label, results_frame: ttk.Frame):
        self.interest_label = interest_label
        self.total_label = total_label
        self.monthly_interest_label = monthly_interest_label
        self.results_frame = results_frame
    
    def update_results(self, total_interest: float, total_amount: float, 
                      monthly_interest: float) -> None:
        """Update the result labels with formatted values and visual feedback"""
        # Format currency values
        self.interest_label.config(text=f"${total_interest:,.2f}")
        self.total_label.config(text=f"${total_amount:,.2f}")
        self.monthly_interest_label.config(text=f"${monthly_interest:,.2f}")
    
    def clear_results(self) -> None:
        """Reset all result labels to zero"""
        self.interest_label.config(text="$0.00")
        self.total_label.config(text="$0.00")
        self.monthly_interest_label.config(text="$0.00")


class InputFields:
    """Manages input field operations with enhanced styling"""
    
    def __init__(self, amount_entry: ttk.Entry, rate_entry: ttk.Entry,
                 duration_entry: ttk.Entry, monthly_entry: ttk.Entry):
        self.entries = {
            'amount': amount_entry,
            'rate': rate_entry,
            'duration': duration_entry,
            'monthly': monthly_entry
        }
    
    def get_values(self) -> Tuple[str, str, str, str]:
        """Get all input values as strings"""
        return (
            self.entries['amount'].get().strip(),
            self.entries['rate'].get().strip(),
            self.entries['duration'].get().strip(),
            self.entries['monthly'].get().strip()
        )
    
    def clear_all(self) -> None:
        """Clear all input fields"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.entries['monthly'].insert(0, "0")
    
    def set_default_example(self) -> None:
        """Set default example values"""
        self.entries['amount'].insert(0, "1000")
        self.entries['rate'].insert(0, "5")
        self.entries['duration'].insert(0, "12")
        self.entries['monthly'].delete(0, tk.END)
        self.entries['monthly'].insert(0, "0")


class SavingsCalculatorApp:
    """Main application class with enhanced UI"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.setup_window()
        self.create_widgets()
        self.setup_components()
    
    def setup_window(self) -> None:
        """Configure the main window settings"""
        self.root.title("💰 Simple Interest Calculator")
        self.root.geometry("600x600")
        self.root.resizable(False, False)
        self.root.configure(bg=Theme.COLORS['background'])
    
    def create_widgets(self) -> None:
        """Create and arrange all GUI widgets"""
        # Main container with padding
        self.main_container = ttk.Frame(self.root, padding="20")
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header section
        self.create_header()
        
        # Input card
        self.create_input_card()
        
        # Results card
        self.create_results_card()
        
        # Footer section
        self.create_footer()
    
    def create_header(self) -> None:
        """Create application header"""
        header_frame = ttk.Frame(self.main_container)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        # App title with icon
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(anchor='center')
        
        # Emoji icon (using text as emoji)
        icon_label = ttk.Label(title_frame, text="💰", font=('Segoe UI', 24))
        icon_label.pack(side=tk.LEFT, padx=(0, 10))
        
        title_label = ttk.Label(title_frame, text="Simple Interest Calculator", 
                               font=Theme.FONTS['title'], foreground=Theme.COLORS['primary'])
        title_label.pack(side=tk.LEFT)
        
        # Subtitle
        subtitle_label = ttk.Label(header_frame, text="Calculate your savings growth with simple interest",
                                  font=Theme.FONTS['body'], foreground=Theme.COLORS['text_secondary'])
        subtitle_label.pack(anchor='center', pady=(5, 0))
    
    def create_input_card(self) -> None:
        """Create input section as a card"""
        input_card = ttk.LabelFrame(self.main_container, text="📊 Input Details", 
                                   padding="15")
        input_card.pack(fill=tk.X, pady=(0, 15))
        
        # Input grid
        self.create_input_grid(input_card)
        
        # Buttons - using regular tkinter buttons for reliable styling
        self.create_action_buttons(input_card)
    
    def create_input_grid(self, parent: ttk.Frame) -> None:
        """Create input fields grid"""
        # Principal amount
        ttk.Label(parent, text="Principal Amount ($):", font=Theme.FONTS['body']).grid(
            row=0, column=0, sticky=tk.W, pady=6, padx=(0, 10))
        self.amount_entry = ttk.Entry(parent, font=Theme.FONTS['body'], width=20)
        self.amount_entry.grid(row=0, column=1, pady=6, sticky=(tk.W, tk.E))
        
        # Annual interest rate
        ttk.Label(parent, text="Annual Interest Rate (%):", font=Theme.FONTS['body']).grid(
            row=1, column=0, sticky=tk.W, pady=6, padx=(0, 10))
        self.rate_entry = ttk.Entry(parent, font=Theme.FONTS['body'], width=20)
        self.rate_entry.grid(row=1, column=1, pady=6, sticky=(tk.W, tk.E))
        
        # Duration
        ttk.Label(parent, text="Duration (months):", font=Theme.FONTS['body']).grid(
            row=2, column=0, sticky=tk.W, pady=6, padx=(0, 10))
        self.duration_entry = ttk.Entry(parent, font=Theme.FONTS['body'], width=20)
        self.duration_entry.grid(row=2, column=1, pady=6, sticky=(tk.W, tk.E))
        
        # Monthly deposit
        ttk.Label(parent, text="Monthly Deposit ($):", font=Theme.FONTS['body']).grid(
            row=3, column=0, sticky=tk.W, pady=6, padx=(0, 10))
        self.monthly_entry = ttk.Entry(parent, font=Theme.FONTS['body'], width=20)
        self.monthly_entry.grid(row=3, column=1, pady=6, sticky=(tk.W, tk.E))
        self.monthly_entry.insert(0, "0")
        
        # Configure grid weights
        parent.columnconfigure(1, weight=1)
    
    def create_action_buttons(self, parent: ttk.Frame) -> None:
        """Create action buttons with proper styling"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=4, column=0, columnspan=2, pady=15)
        
        # Create regular tkinter buttons with proper styling
        self.calculate_btn = tk.Button(
            button_frame, 
            text="🚀 Calculate", 
            font=Theme.FONTS['button'],
            bg=Theme.COLORS['primary'],
            fg=Theme.COLORS['button_text'],
            activebackground=Theme.COLORS['primary_hover'],
            activeforeground=Theme.COLORS['button_text'],
            relief='flat',
            padx=15,
            pady=8,
            cursor='hand2',
            command=self.calculate_interest
        )
        self.calculate_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        self.clear_btn = tk.Button(
            button_frame, 
            text="🗑️ Clear", 
            font=Theme.FONTS['button'],
            bg=Theme.COLORS['primary'],
            fg=Theme.COLORS['button_text'],
            activebackground=Theme.COLORS['primary_hover'],
            activeforeground=Theme.COLORS['button_text'],
            relief='flat',
            padx=15,
            pady=8,
            cursor='hand2',
            command=self.clear_fields
        )
        self.clear_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        self.example_btn = tk.Button(
            button_frame, 
            text="💡 Example", 
            font=Theme.FONTS['button'],
            bg=Theme.COLORS['primary'],
            fg=Theme.COLORS['button_text'],
            activebackground=Theme.COLORS['primary_hover'],
            activeforeground=Theme.COLORS['button_text'],
            relief='flat',
            padx=15,
            pady=8,
            cursor='hand2',
            command=self.load_example
        )
        self.example_btn.pack(side=tk.LEFT)
    
    def create_results_card(self) -> None:
        """Create results display section as a card"""
        self.results_frame = ttk.LabelFrame(self.main_container, text="📈 Results", 
                                          padding="15")
        self.results_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Results grid with more spacing
        ttk.Label(self.results_frame, text="Total Interest Earned:", 
                 font=Theme.FONTS['body']).grid(row=0, column=0, sticky=tk.W, pady=8, padx=(0, 10))
        self.interest_label = ttk.Label(self.results_frame, text="$0.00", 
                                      font=Theme.FONTS['result'], foreground=Theme.COLORS['success'])
        self.interest_label.grid(row=0, column=1, sticky=tk.W, pady=8)
        
        ttk.Label(self.results_frame, text="Total Amount:", 
                 font=Theme.FONTS['body']).grid(row=1, column=0, sticky=tk.W, pady=8, padx=(0, 10))
        self.total_label = ttk.Label(self.results_frame, text="$0.00", 
                                   font=Theme.FONTS['result'], foreground=Theme.COLORS['primary'])
        self.total_label.grid(row=1, column=1, sticky=tk.W, pady=8)
        
        ttk.Label(self.results_frame, text="Average Monthly Interest:", 
                 font=Theme.FONTS['body']).grid(row=2, column=0, sticky=tk.W, pady=8, padx=(0, 10))
        self.monthly_interest_label = ttk.Label(self.results_frame, text="$0.00", 
                                              font=Theme.FONTS['result'], foreground=Theme.COLORS['secondary'])
        self.monthly_interest_label.grid(row=2, column=1, sticky=tk.W, pady=8)
        
        # Configure grid weights
        self.results_frame.columnconfigure(1, weight=1)
    
    def create_footer(self) -> None:
        """Create footer section"""
        footer_frame = ttk.Frame(self.main_container)
        footer_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Info text
        info_text = "💡 Tip: Simple interest is calculated on the original principal only, without compounding."
        info_label = ttk.Label(footer_frame, text=info_text, font=('Segoe UI', 9),
                              foreground=Theme.COLORS['text_secondary'], wraplength=500)
        info_label.pack(anchor='center')
        
        # Copyright
        copyright_label = ttk.Label(footer_frame, text="© 2024 Interest Calculator", 
                                   font=('Segoe UI', 8), foreground=Theme.COLORS['text_secondary'])
        copyright_label.pack(anchor='center', pady=(8, 0))
    
    def setup_components(self) -> None:
        """Initialize component instances"""
        self.input_fields = InputFields(
            self.amount_entry, self.rate_entry, self.duration_entry, self.monthly_entry
        )
        self.results_display = ResultsDisplay(
            self.interest_label, self.total_label, self.monthly_interest_label, self.results_frame
        )
        
        # Set focus to first field
        self.amount_entry.focus_set()
        
        # Bind Enter key to calculate
        self.root.bind('<Return>', lambda event: self.calculate_interest())
    
    def calculate_interest(self) -> None:
        """Calculate and display interest based on user inputs"""
        try:
            # Get and validate inputs
            input_values = self.input_fields.get_values()
            principal, annual_rate, months, monthly_deposit = InputValidator.validate_inputs(*input_values)
            
            # Calculate results
            total_interest, total_amount, monthly_interest = InterestCalculator.calculate_simple_interest(
                principal, annual_rate, months, monthly_deposit
            )
            
            # Update display with visual feedback
            self.results_display.update_results(total_interest, total_amount, monthly_interest)
            
        except ValueError as e:
            messagebox.showerror("Input Error", str(e), icon='warning')
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}", icon='error')
    
    def clear_fields(self) -> None:
        """Clear all input fields and reset results"""
        self.input_fields.clear_all()
        self.results_display.clear_results()
        self.amount_entry.focus_set()
    
    def load_example(self) -> None:
        """Load example values"""
        self.clear_fields()
        self.input_fields.set_default_example()
        self.calculate_interest()


def center_window(window: tk.Tk) -> None:
    """Center the window on the screen"""
    window.update_idletasks()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_width = window.winfo_width()
    window_height = window.winfo_height()
    
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    
    window.geometry(f'+{x}+{y}')


def main():
    """Main application entry point"""
    root = tk.Tk()
    app = SavingsCalculatorApp(root)
    center_window(root)
    root.mainloop()


if __name__ == "__main__":
    main()