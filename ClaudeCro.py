"""
Kalkulator jednostavnih kamata
Aplikacija za računanje kamata na temelju početnog iznosa, 
godišnje kamatne stope i trajanja štednje.
"""

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Dict, Tuple
from dataclasses import dataclass


@dataclass
class KamataParametri:
    """Klasa za čuvanje parametara kamata."""
    pocetni_iznos: float
    godisnja_kamata: float
    mjeseci: int


@dataclass
class KamataRezultat:
    """Klasa za čuvanje rezultata izračuna kamata."""
    ukupna_kamata: float
    konacni_iznos: float
    mjesecna_kamata: float
    godine: float


class KamataKalkulator:
    """Kalkulator jednostavnih kamata s poboljšanim GUI sučeljem."""
    
    def __init__(self, root: tk.Tk):
        """Inicijalizacija kalkulatora."""
        self.root = root
        self._podesi_prozor()
        self._podesi_stilove()
        self._stvori_varijable()
        self._stvori_gui()
        self._postavi_fokus_i_bindings()

    def _podesi_prozor(self) -> None:
        """Postavlja osnovne svojstva glavnog prozora."""
        self.root.title("💰 Kalkulator kamata")
        self.root.geometry("550x750")
        self.root.resizable(True, True)
        self.root.minsize(500, 700)
        self.root.configure(bg='#f0f8ff')
        
        # Centriranje prozora
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (550 // 2)
        y = (self.root.winfo_screenheight() // 2) - (750 // 2)
        self.root.geometry(f'550x750+{x}+{y}')

    def _podesi_stilove(self) -> None:
        """Postavlja ttk stilove."""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Stil za entry polja
        self.style.configure('Custom.TEntry',
                           fieldbackground='white',
                           borderwidth=2,
                           relief='solid',
                           padding=8)
        
        # Stil za gumbove
        self.style.configure('Action.TButton',
                           background='#4CAF50',
                           foreground='white',
                           padding=(20, 10),
                           font=('Arial', 12, 'bold'))
        
        self.style.configure('Clear.TButton',
                           background='#f44336',
                           foreground='white',
                           padding=(10, 5),
                           font=('Arial', 10))

    def _stvori_varijable(self) -> None:
        """Stvara tkinter varijable za unos podataka."""
        self.var_iznos = tk.StringVar()
        self.var_kamata = tk.StringVar()
        self.var_mjeseci = tk.StringVar()
        
        # Validacija unosa u realnom vremenu
        self.var_iznos.trace('w', self._validiraj_unos)
        self.var_kamata.trace('w', self._validiraj_unos)
        self.var_mjeseci.trace('w', self._validiraj_unos)

    def _stvori_gui(self) -> None:
        """Stvara kompletno korisničko sučelje."""
        # Glavna container s scroll
        canvas = tk.Canvas(self.root, bg='#f0f8ff', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#f0f8ff')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Glavna container
        main_container = tk.Frame(scrollable_frame, bg='#f0f8ff')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        self._stvori_naslov(main_container)
        self._stvori_okvir_unosa(main_container)
        self._stvori_gumbove(main_container)
        self._stvori_okvir_rezultata(main_container)

        # Mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def _stvori_naslov(self, parent: tk.Widget) -> None:
        """Stvara glavni naslov aplikacije."""
        naslov_frame = tk.Frame(parent, bg='#f0f8ff')
        naslov_frame.pack(pady=(0, 20))
        
        tk.Label(naslov_frame,
                text="💰 Kalkulator kamata",
                font=('Arial', 18, 'bold'),
                fg='#2c3e50',
                bg='#f0f8ff').pack()
        
        tk.Label(naslov_frame,
                text="Izračunajte jednostavne kamate brzo i jednostavno",
                font=('Arial', 10, 'italic'),
                fg='#7f8c8d',
                bg='#f0f8ff').pack(pady=(3, 0))

    def _stvori_okvir_unosa(self, parent: tk.Widget) -> None:
        """Stvara poboljšani okvir za unos podataka."""
        # Glavni okvir
        input_frame = tk.LabelFrame(parent,
                                   text="  📝 Unesite podatke  ",
                                   font=('Arial', 11, 'bold'),
                                   fg='#2c3e50',
                                   bg='#ffffff',
                                   relief='solid',
                                   bd=1,
                                   padx=15,
                                   pady=15)
        input_frame.pack(fill='x', pady=(0, 15))

        # Grid konfiguracija
        input_frame.columnconfigure(1, weight=1)

        # Početni iznos
        self._stvori_polje_unosa(input_frame, 0, 
                               "💵 Početni iznos:",
                               "€", 
                               self.var_iznos,
                               "Unesite početni iznos za štednju")

        # Kamatna stopa
        self._stvori_polje_unosa(input_frame, 1,
                               "📈 Godišnja kamatna stopa:",
                               "%",
                               self.var_kamata,
                               "Unesite godišnju kamatnu stopu")

        # Trajanje
        self._stvori_polje_unosa(input_frame, 2,
                               "📅 Trajanje štednje:",
                               "mj.",
                               self.var_mjeseci,
                               "Unesite broj mjeseci štednje")

    def _stvori_polje_unosa(self, parent: tk.Widget, red: int, 
                           label_text: str, suffix: str, 
                           varijabla: tk.StringVar, tooltip: str) -> None:
        """Stvara poboljšano polje za unos s labelom i suffix-om."""
        # Label
        label = tk.Label(parent, 
                        text=label_text,
                        font=('Arial', 10, 'bold'),
                        fg='#34495e',
                        bg='#ffffff',
                        anchor='w')
        label.grid(row=red, column=0, sticky='w', pady=(8, 4))

        # Frame za entry i suffix
        entry_frame = tk.Frame(parent, bg='#ffffff')
        entry_frame.grid(row=red, column=1, sticky='ew', padx=(15, 0), pady=(8, 4))

        # Entry polje
        entry = ttk.Entry(entry_frame,
                         textvariable=varijabla,
                         font=('Arial', 12),
                         style='Custom.TEntry',
                         width=15)
        entry.pack(side='left', fill='x', expand=True)

        # Suffix label
        suffix_label = tk.Label(entry_frame,
                               text=suffix,
                               font=('Arial', 11, 'bold'),
                               fg='#7f8c8d',
                               bg='#ffffff')
        suffix_label.pack(side='right', padx=(10, 0))

        # Tooltip (simulacija)
        self._dodaj_tooltip(entry, tooltip)

    def _dodaj_tooltip(self, widget: tk.Widget, text: str) -> None:
        """Dodaje jednostavan tooltip widget-u."""
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            label = tk.Label(tooltip, text=text, 
                           background='#ffffcc',
                           relief='solid',
                           borderwidth=1,
                           font=('Arial', 9))
            label.pack()
            widget.tooltip = tooltip

        def hide_tooltip(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip

        widget.bind('<Enter>', show_tooltip)
        widget.bind('<Leave>', hide_tooltip)

    def _stvori_gumbove(self, parent: tk.Widget) -> None:
        """Stvara gumbove za akcije."""
        button_frame = tk.Frame(parent, bg='#f0f8ff')
        button_frame.pack(pady=8)

        # Gumb za računanje
        self.calc_button = ttk.Button(button_frame,
                                     text="🧮 IZRAČUNAJ KAMATU",
                                     style='Action.TButton',
                                     command=self._izracunaj_kamatu)
        self.calc_button.pack(side='left', padx=(0, 8))

        # Gumb za brisanje
        clear_button = ttk.Button(button_frame,
                                 text="🗑️ OBRIŠI",
                                 style='Clear.TButton',
                                 command=self._obrisi_polja)
        clear_button.pack(side='left')

    def _stvori_okvir_rezultata(self, parent: tk.Widget) -> None:
        """Stvara poboljšani okvir za prikaz rezultata."""
        self.result_frame = tk.LabelFrame(parent,
                                        text="  📊 Rezultati  ",
                                        font=('Arial', 12, 'bold'),
                                        fg='#2c3e50',
                                        bg='#ffffff',
                                        relief='solid',
                                        bd=1,
                                        padx=20,
                                        pady=15)
        self.result_frame.pack(fill='both', expand=True, pady=(10, 0))

        # Početna poruka
        self.poruka_label = tk.Label(self.result_frame,
                                   text="👆 Unesite podatke i kliknite 'IZRAČUNAJ KAMATU'",
                                   font=('Arial', 11, 'italic'),
                                   fg='#95a5a6',
                                   bg='#ffffff')
        self.poruka_label.pack(expand=True)

        # Rezultati (skriveni na početku)
        self._stvori_rezultate()

    def _stvori_rezultate(self) -> None:
        """Stvara elemente za prikaz rezultata."""
        self.results_container = tk.Frame(self.result_frame, bg='#ffffff')
        
        # Glavni rezultati
        self._stvori_rezultat_karticu("💰", "Ukupna kamata:", "ukupna_kamata", "#27ae60")
        self._stvori_rezultat_karticu("💵", "Konačni iznos:", "konacni_iznos", "#2980b9")
        self._stvori_rezultat_karticu("📅", "Mjesečna kamata:", "mjesecna_kamata", "#e67e22")

        # Separator
        separator = tk.Frame(self.results_container, height=1, bg='#ecf0f1')
        separator.pack(fill='x', pady=10)

        # Detalji
        self.detalji_frame = tk.Frame(self.results_container, bg='#f8f9fa', relief='solid', bd=1)
        self.detalji_frame.pack(fill='x', pady=(0, 5))
        
        tk.Label(self.detalji_frame,
                text="📋 Detalji izračuna:",
                font=('Arial', 9, 'bold'),
                fg='#2c3e50',
                bg='#f8f9fa').pack(anchor='w', padx=10, pady=(8, 3))

        self.label_detalji = tk.Label(self.detalji_frame,
                                    text="",
                                    font=('Arial', 8),
                                    fg='#34495e',
                                    bg='#f8f9fa',
                                    justify='left',
                                    anchor='w')
        self.label_detalji.pack(anchor='w', padx=12, pady=(0, 8))

    def _stvori_rezultat_karticu(self, ikona: str, naslov: str, attr_name: str, boja: str) -> None:
        """Stvara karticu za pojedinačni rezultat."""
        card = tk.Frame(self.results_container, bg='#ffffff', relief='solid', bd=1)
        card.pack(fill='x', pady=3, ipady=5)

        # Ikona i naslov
        header_frame = tk.Frame(card, bg='#ffffff')
        header_frame.pack(fill='x', padx=15, pady=(8, 3))

        tk.Label(header_frame,
                text=f"{ikona} {naslov}",
                font=('Arial', 10, 'bold'),
                fg='#2c3e50',
                bg='#ffffff').pack(side='left')

        # Vrijednost
        value_label = tk.Label(card,
                             text="- €",
                             font=('Arial', 13, 'bold'),
                             fg=boja,
                             bg='#ffffff')
        value_label.pack(anchor='w', padx=15, pady=(0, 8))
        
        setattr(self, f"label_{attr_name}", value_label)

    def _postavi_fokus_i_bindings(self) -> None:
        """Postavlja fokus i tipkovničke prečace."""
        # Fokus na prvo polje
        self.root.after(100, lambda: self.var_iznos and self.root.focus_set())
        
        # Enter za računanje
        self.root.bind('<Return>', lambda e: self._izracunaj_kamatu())
        self.root.bind('<KP_Enter>', lambda e: self._izracunaj_kamatu())
        
        # Ctrl+N za novo
        self.root.bind('<Control-n>', lambda e: self._obrisi_polja())

    def _validiraj_unos(self, *args) -> None:
        """Validira unos u realnom vremenu i omogućava/onemogućava gumb."""
        try:
            iznos_ok = self.var_iznos.get() and float(self.var_iznos.get().replace(',', '.')) > 0
            kamata_ok = self.var_kamata.get() and float(self.var_kamata.get().replace(',', '.')) >= 0
            mjeseci_ok = self.var_mjeseci.get() and int(self.var_mjeseci.get()) > 0
            
            if iznos_ok and kamata_ok and mjeseci_ok:
                self.calc_button.config(state='normal')
            else:
                self.calc_button.config(state='disabled')
        except (ValueError, AttributeError):
            if hasattr(self, 'calc_button'):
                self.calc_button.config(state='disabled')

    def _obrisi_polja(self) -> None:
        """Briše sva polja i vraća na početno stanje."""
        self.var_iznos.set("")
        self.var_kamata.set("")
        self.var_mjeseci.set("")
        
        # Sakrij rezultate i prikaži poruku
        self.results_container.pack_forget()
        self.poruka_label.pack(expand=True)

    def _dohvati_parametre(self) -> KamataParametri:
        """Dohvaća i validira parametre iz GUI polja."""
        try:
            iznos = float(self.var_iznos.get().strip().replace(',', '.'))
            kamata = float(self.var_kamata.get().strip().replace(',', '.'))
            mjeseci = int(self.var_mjeseci.get().strip())
            
            self._validiraj_parametre(iznos, kamata, mjeseci)
            
            return KamataParametri(
                pocetni_iznos=iznos,
                godisnja_kamata=kamata,
                mjeseci=mjeseci
            )
            
        except ValueError as e:
            if "could not convert" in str(e):
                raise ValueError("Molimo unesite valjane brojeve!")
            raise e

    def _validiraj_parametre(self, iznos: float, kamata: float, mjeseci: int) -> None:
        """Validira unesene parametre."""
        if iznos <= 0:
            raise ValueError("Početni iznos mora biti veći od 0!")
        if kamata < 0:
            raise ValueError("Kamatna stopa ne može biti negativna!")
        if mjeseci <= 0:
            raise ValueError("Trajanje mora biti veće od 0 mjeseci!")

    @staticmethod
    def _izracunaj_jednostavnu_kamatu(parametri: KamataParametri) -> KamataRezultat:
        """Računa jednostavnu kamatu prema formuli K = P × r × t."""
        godine = parametri.mjeseci / 12
        godisnja_kamata_decimalno = parametri.godisnja_kamata / 100
        
        ukupna_kamata = (
            parametri.pocetni_iznos * 
            godisnja_kamata_decimalno * 
            godine
        )
        
        konacni_iznos = parametri.pocetni_iznos + ukupna_kamata
        mjesecna_kamata = ukupna_kamata / parametri.mjeseci
        
        return KamataRezultat(
            ukupna_kamata=ukupna_kamata,
            konacni_iznos=konacni_iznos,
            mjesecna_kamata=mjesecna_kamata,
            godine=godine
        )

    def _azuriraj_prikaz(self, parametri: KamataParametri, rezultat: KamataRezultat) -> None:
        """Ažurira GUI s rezultatima računanja."""
        # Sakrij poruku i prikaži rezultate
        self.poruka_label.pack_forget()
        self.results_container.pack(fill='both', expand=True)

        # Ažuriranje glavnih rezultata s animacijom
        self.label_ukupna_kamata.config(text=f"{rezultat.ukupna_kamata:.2f} €")
        self.label_konacni_iznos.config(text=f"{rezultat.konacni_iznos:.2f} €")
        self.label_mjesecna_kamata.config(text=f"{rezultat.mjesecna_kamata:.2f} €")

        # Ažuriranje detalja
        detalji = self._generiraj_detalje(parametri, rezultat)
        self.label_detalji.config(text=detalji)

    def _generiraj_detalje(self, parametri: KamataParametri, rezultat: KamataRezultat) -> str:
        """Generira tekst s detaljima računanja."""
        return (
            f"• Početni iznos: {parametri.pocetni_iznos:.2f} €\n"
            f"• Kamatna stopa: {parametri.godisnja_kamata:.2f}% godišnje\n"
            f"• Trajanje: {parametri.mjeseci} mjeseci ({rezultat.godine:.2f} godina)\n"
            f"• Formula: K = P × r × t\n"
            f"• Izračun: {parametri.pocetni_iznos:.2f} × "
            f"{parametri.godisnja_kamata/100:.4f} × {rezultat.godine:.2f} = "
            f"{rezultat.ukupna_kamata:.2f} €"
        )

    def _izracunaj_kamatu(self) -> None:
        """Glavna metoda za računanje kamata s error handling-om."""
        try:
            parametri = self._dohvati_parametre()
            rezultat = self._izracunaj_jednostavnu_kamatu(parametri)
            self._azuriraj_prikaz(parametri, rezultat)
            
        except ValueError as e:
            messagebox.showerror("⚠️ Greška", str(e))
        except Exception as e:
            messagebox.showerror("⚠️ Greška", f"Neočekivana greška: {str(e)}")


def main() -> None:
    """Glavna funkcija aplikacije."""
    root = tk.Tk()
    app = KamataKalkulator(root)
    root.mainloop()


if __name__ == "__main__":
    main()