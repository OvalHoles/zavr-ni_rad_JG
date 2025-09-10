import tkinter as tk
from tkinter import messagebox

class KamataKalkulatorApp:
    def __init__(self, master):
        self.master = master
        master.title("Jednostavan kalkulator štednje")
        master.geometry("400x450")  # Povećana visina prozora
        master.resizable(False, False)

        self._kreiraj_widgets()

    def _kreiraj_widgets(self):
        """Metoda za kreiranje i postavljanje svih GUI elemenata s poboljšanim izgledom."""
        main_frame = tk.Frame(self.master, padx=20, pady=20)
        main_frame.pack(expand=True, fill='both')

        input_frame = tk.LabelFrame(main_frame, text=" Unesite podatke ", padx=15, pady=15)
        input_frame.pack(pady=10, fill='x')

        # Početni iznos
        tk.Label(input_frame, text="Početni iznos (HRK):", font=("Arial", 10)).grid(row=0, column=0, pady=5, sticky="w")
        self.unos_iznos = tk.Entry(input_frame, width=30)
        self.unos_iznos.grid(row=0, column=1, pady=5)

        # Godišnja kamatna stopa
        tk.Label(input_frame, text="Godišnja kamatna stopa (%):", font=("Arial", 10)).grid(row=1, column=0, pady=5, sticky="w")
        self.unos_stopa = tk.Entry(input_frame, width=30)
        self.unos_stopa.grid(row=1, column=1, pady=5)

        # Trajanje štednje u mjesecima
        tk.Label(input_frame, text="Trajanje (mjeseci):", font=("Arial", 10)).grid(row=2, column=0, pady=5, sticky="w")
        self.unos_mjeseci = tk.Entry(input_frame, width=30)
        self.unos_mjeseci.grid(row=2, column=1, pady=5)

        # Gumb za izračun
        tk.Button(main_frame, text="Izračunaj", command=self.izracunaj_kamatu, font=("Arial", 12, "bold"), relief="raised").pack(pady=15)

        # Okvir za prikaz rezultata
        result_frame = tk.LabelFrame(main_frame, text=" Rezultati ", padx=15, pady=15)
        result_frame.pack(pady=10, fill='x')

        # Labele za prikaz rezultata
        self.rezultat_mj_kamata_label = tk.Label(result_frame, text="", font=("Arial", 11, "bold"))
        self.rezultat_mj_kamata_label.pack(pady=5, anchor='w')

        self.rezultat_ukupna_kamata_label = tk.Label(result_frame, text="", font=("Arial", 11, "bold"))
        self.rezultat_ukupna_kamata_label.pack(pady=5, anchor='w')

        self.rezultat_ukupno_label = tk.Label(result_frame, text="", font=("Arial", 11, "bold"))
        self.rezultat_ukupno_label.pack(pady=5, anchor='w')

    def izracunaj_kamatu(self):
        """Metoda koja dohvaća unose, validira ih, računa i prikazuje rezultate."""
        try:
            iznos = float(self.unos_iznos.get())
            stopa = float(self.unos_stopa.get())
            mjeseci = int(self.unos_mjeseci.get())

            if iznos <= 0 or stopa <= 0 or mjeseci <= 0:
                messagebox.showerror("Pogreška u unosu", "Sve vrijednosti moraju biti pozitivni brojevi.")
                return

            godisnja_stopa_decimal = stopa / 100
            mjesecna_stopa_decimal = godisnja_stopa_decimal / 12

            mjesecna_kamata = iznos * mjesecna_stopa_decimal
            ukupna_kamata = mjesecna_kamata * mjeseci
            ukupni_iznos = iznos + ukupna_kamata

            # Ažuriranje labele s rezultatima
            self.rezultat_mj_kamata_label.config(text=f"Mjesečna kamata: {mjesecna_kamata:.2f} HRK")
            self.rezultat_ukupna_kamata_label.config(text=f"Ukupna kamata: {ukupna_kamata:.2f} HRK")
            self.rezultat_ukupno_label.config(text=f"Ukupan iznos na kraju: {ukupni_iznos:.2f} HRK")
        
        except ValueError:
            messagebox.showerror("Pogreška u unosu", "Molimo unesite valjane numeričke vrijednosti.")

if __name__ == "__main__":
    root = tk.Tk()
    app = KamataKalkulatorApp(root)
    root.mainloop()