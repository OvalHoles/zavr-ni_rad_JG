import tkinter as tk
from tkinter import messagebox
from typing import Tuple, Optional

class KalkulatorKamata:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Kalkulator kamata na štednju")
        self.root.geometry("600x1200")
        self.root.resizable(True, True)
        self.root.configure(bg="#f5f5f5")
        
        # Varijable za praćenje unosa
        self.iznos_var = tk.StringVar()
        self.kamatna_stopa_var = tk.StringVar()
        self.mjeseci_var = tk.StringVar()
        
        self._setup_styles()
        self._create_widgets()
        self._setup_layout()
        self._setup_bindings()
        
    def _setup_styles(self):
        """Definira moderne stilove za aplikaciju"""
        self.styles = {
            'bg_color': "#f5f5f5",
            'card_bg': "#ffffff",
            'primary_color': "#2563eb",
            'success_color': "#10b981",
            'danger_color': "#ef4444",
            'text_color': "#374151",
            'muted_color': "#6b7280",
            
            'font_title': ("Arial", 18, "bold"),
            'font_subtitle': ("Arial", 14, "bold"),
            'font_label': ("Arial", 11),
            'font_entry': ("Arial", 11),
            'font_button': ("Arial", 12, "bold"),
            'font_result': ("Arial", 13, "bold"),
            'font_info': ("Arial", 10),
        }
        
    def _create_widgets(self):
        """Kreira sve UI komponente"""
        self._create_header()
        self._create_input_card()
        self._create_buttons()
        self._create_results_card()
        self._create_footer()
    
    def _create_header(self):
        """Kreira zaglavlje aplikacije"""
        self.header_frame = tk.Frame(self.root, bg="#f5f5f5")
        
        self.label_naslov = tk.Label(
            self.header_frame,
            text="💰 KALKULATOR KAMATA NA ŠTEDNJU",
            font=self.styles['font_title'],
            fg=self.styles['primary_color'],
            bg="#f5f5f5",
            pady=20
        )
        
        self.label_podnaslov = tk.Label(
            self.header_frame,
            text="Izračunajte koliko možete zaraditi štedeći novac",
            font=self.styles['font_label'],
            fg=self.styles['muted_color'],
            bg="#f5f5f5"
        )
    
    def _create_input_card(self):
        """Kreira karticu za unos podataka"""
        self.input_card = tk.Frame(self.root, bg="#ffffff", relief="solid", bd=2)
        
        # Frame za input polja
        self.input_fields_frame = tk.Frame(self.input_card, bg="#ffffff")
        
        # Lista input polja
        self.input_fields = [
            {
                "label": "Početni iznos (€)",
                "var": self.iznos_var,
                "placeholder": "Unesite iznos...",
                "icon": "💶"
            },
            {
                "label": "Godišnja kamatna stopa (%)",
                "var": self.kamatna_stopa_var,
                "placeholder": "Npr. 3.5",
                "icon": "📈"
            },
            {
                "label": "Trajanje štednje (mjeseci)",
                "var": self.mjeseci_var,
                "placeholder": "Npr. 12",
                "icon": "📅"
            }
        ]
        
        self.entries = {}
        for i, field in enumerate(self.input_fields):
            # Red za label i input
            row_frame = tk.Frame(self.input_fields_frame, bg="#ffffff")
            row_frame.pack(fill="x", pady=15)
            
            # Label s ikonom
            label = tk.Label(
                row_frame,
                text=f"{field['icon']} {field['label']}:",
                font=self.styles['font_label'],
                fg=self.styles['text_color'],
                bg="#ffffff",
                anchor="w"
            )
            label.pack(fill="x", pady=(0, 8))
            
            # Input polje
            entry = tk.Entry(
                row_frame,
                textvariable=field['var'],
                font=self.styles['font_entry'],
                width=30,
                bg="#f8f9fa",
                relief="solid",
                bd=1
            )
            entry.pack(fill="x", pady=2)
            
            # Postavi placeholder
            entry.insert(0, field['placeholder'])
            entry.config(fg="gray")
            entry.bind("<FocusIn>", lambda e, entry=entry, ph=field['placeholder']: 
                      self._clear_placeholder(e, entry, ph))
            entry.bind("<FocusOut>", lambda e, entry=entry, ph=field['placeholder']: 
                      self._set_placeholder(e, entry, ph))
            
            self.entries[field['label']] = entry
    
    def _create_buttons(self):
        """Kreira gumbe za akcije"""
        self.button_frame = tk.Frame(self.root, bg="#f5f5f5")
        
        self.btn_izracunaj = tk.Button(
            self.button_frame,
            text="🧮 IZRAČUNAJ",
            command=self._izracunaj_kamatu,
            font=self.styles['font_button'],
            bg=self.styles['primary_color'],
            fg="white",
            padx=30,
            pady=12,
            borderwidth=0,
            cursor="hand2",
            relief="flat"
        )
        
        self.btn_resetiraj = tk.Button(
            self.button_frame,
            text="🔄 RESETIRAJ",
            command=self._resetiraj,
            font=self.styles['font_button'],
            bg=self.styles['muted_color'],
            fg="white",
            padx=30,
            pady=12,
            borderwidth=0,
            cursor="hand2",
            relief="flat"
        )
    
    def _create_results_card(self):
        """Kreira VELIKU karticu za prikaz rezultata"""
        self.results_card = tk.Frame(
            self.root, 
            bg="#e8f5e8",
            relief="solid", 
            bd=3,
            height=250
        )
        
        self.results_header = tk.Label(
            self.results_card,
            text="📊 REZULTATI IZRAČUNA",
            font=self.styles['font_subtitle'],
            fg=self.styles['primary_color'],
            bg="#e8f5e8",
            pady=20
        )
        
        # Glavni frame za rezultate
        self.results_content_frame = tk.Frame(self.results_card, bg="#e8f5e8")
        
        # Definiranje rezultata - SADA PRAZNI TEKSTOVI
        self.result_configs = [
            {"key": "ukupna_kamata", "text": "Ukupna kamata:", "color": "#059669", "icon": "💰"},
            {"key": "ukupan_iznos", "text": "Ukupan iznos:", "color": "#2563eb", "icon": "💵"},
            {"key": "mjesečna_kamata", "text": "Mjesečna kamata:", "color": "#dc2626", "icon": "📈"}
        ]
        
        self.result_labels = {}
        for config in self.result_configs:
            # Frame za svaki rezultat
            result_frame = tk.Frame(self.results_content_frame, bg="#e8f5e8")
            result_frame.pack(fill="x", pady=12)
            
            # Label za rezultat - POČETNI TEKST JE PRAZAN
            label = tk.Label(
                result_frame,
                text="",  # PRAZNO NA POČETKU
                font=self.styles['font_result'],
                fg=config['color'],
                bg="#e8f5e8",
                anchor="w",
                pady=5
            )
            label.pack(fill="x")
            
            self.result_labels[config['key']] = label
    
    def _create_footer(self):
        """Kreira footer s informacijama"""
        self.footer = tk.Frame(self.root, bg="#f5f5f5")
        
        self.info_label = tk.Label(
            self.footer,
            text="💡 Mjesečna kamata = Ukupna kamata / Broj mjeseci • Jednostavna kamata",
            font=self.styles['font_info'],
            fg=self.styles['muted_color'],
            bg="#f5f5f5",
            pady=15
        )
    
    def _setup_layout(self):
        """Postavlja layout komponenti"""
        # Header
        self.header_frame.pack(fill="x", pady=(20, 15))
        self.label_naslov.pack()
        self.label_podnaslov.pack()
        
        # Input card
        self.input_card.pack(fill="x", padx=30, pady=20, ipady=25)
        self.input_fields_frame.pack(padx=30, pady=20, fill="x")
        
        # Buttons
        self.button_frame.pack(pady=25)
        self.btn_izracunaj.grid(row=0, column=0, padx=20)
        self.btn_resetiraj.grid(row=0, column=1, padx=20)
        
        # Results card
        self.results_card.pack(fill="x", padx=30, pady=25, ipady=20)
        self.results_card.pack_propagate(False)
        
        self.results_header.pack(pady=(15, 20))
        self.results_content_frame.pack(expand=True, fill="both", padx=40, pady=15)
        
        # Footer
        self.footer.pack(side="bottom", fill="x", pady=20)
        self.info_label.pack()
        
        # Fokus na prvo polje
        self.entries["Početni iznos (€)"].focus()
        self.entries["Početni iznos (€)"].icursor(0)
    
    def _setup_bindings(self):
        """Postavlja event bindings"""
        # Enter tipka za izračun
        self.root.bind('<Return>', lambda event: self._izracunaj_kamatu())
        
        # Esc tipka za reset
        self.root.bind('<Escape>', lambda event: self._resetiraj())
    
    def _clear_placeholder(self, event, entry, placeholder):
        """Briše placeholder na fokusu"""
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.configure(foreground='black')
    
    def _set_placeholder(self, event, entry, placeholder):
        """Postavlja placeholder ako je polje prazno"""
        if not entry.get():
            entry.insert(0, placeholder)
            entry.configure(foreground='gray')
    
    def _get_user_input(self) -> Optional[Tuple[float, float, int]]:
        """Dohvaća i validira korisnički unos"""
        try:
            # Provjeri jesu li sva polja popunjena
            for field in self.input_fields:
                value = field['var'].get().strip()
                if value == field['placeholder'] or not value:
                    messagebox.showwarning("Upozorenje", f"Molimo unesite {field['label'].lower()}")
                    self.entries[field['label']].focus()
                    return None
            
            iznos = float(self.iznos_var.get())
            kamatna_stopa = float(self.kamatna_stopa_var.get())
            mjeseci = int(self.mjeseci_var.get())
            
            if iznos <= 0 or kamatna_stopa <= 0 or mjeseci <= 0:
                raise ValueError("Vrijednosti moraju biti veće od 0")
                
            return iznos, kamatna_stopa, mjeseci
            
        except ValueError as e:
            messagebox.showerror("Greška", "Molimo unesite ispravne numeričke vrijednosti veće od 0!")
            return None
    
    def _calculate_interest(self, iznos: float, kamatna_stopa: float, mjeseci: int) -> dict:
        """Izračunava kamate prema formulama"""
        mjesecna_kamatna_stopa = kamatna_stopa / 100 / 12
        ukupna_kamata = iznos * mjesecna_kamatna_stopa * mjeseci
        
        return {
            'ukupna_kamata': ukupna_kamata,
            'ukupan_iznos': iznos + ukupna_kamata,
            'mjesečna_kamata': ukupna_kamata / mjeseci
        }
    
    def _display_results(self, results: dict):
        """Prikazuje rezultate korisniku UNUTAR aplikacije"""
        for config in self.result_configs:
            key = config['key']
            value = results[key]
            # PRIKAZUJEMO REZULTATE U LABEL-IMA UNUTAR APLIKACIJE
            result_text = f"{config['icon']} {config['text']} {value:,.2f} €".replace(',', ' ')
            self.result_labels[key].config(text=result_text)
    
    def _izracunaj_kamatu(self):
        """Glavna funkcija za izračun kamata - SADA PRIKAZUJE REZULTATE U APLIKACIJI"""
        user_input = self._get_user_input()
        if user_input is None:
            return
            
        iznos, kamatna_stopa, mjeseci = user_input
        
        results = self._calculate_interest(iznos, kamatna_stopa, mjeseci)
        self._display_results(results)  # PRIKAZ U APLIKACIJI, NE U KONZOLI
    
    def _resetiraj(self):
        """Resetira sva polja i rezultate"""
        for field in self.input_fields:
            field['var'].set("")
            entry = self.entries[field['label']]
            entry.delete(0, tk.END)
            entry.insert(0, field['placeholder'])
            entry.configure(foreground='gray')
        
        # Resetiraj rezultate na prazan tekst
        for config in self.result_configs:
            self.result_labels[config['key']].config(text="")
        
        self.entries["Početni iznos (€)"].focus()

def main():
    """Glavna funkcija za pokretanje aplikacije"""
    root = tk.Tk()
    app = KalkulatorKamata(root)
    root.mainloop()

if __name__ == "__main__":
    main()