import tkinter as tk

class KalkulatorKamata:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Kalkulator kamata")

        # Kreiranje ulaznih polja
        tk.Label(self.window, text="Iznos:").grid(row=0, column=0)
        tk.Label(self.window, text="Godišnja kamatna stopa (%):").grid(row=1, column=0)
        tk.Label(self.window, text="Trajanje štednje (mjeseci):").grid(row=2, column=0)

        self.iznos_entry = tk.Entry(self.window)
        self.kamatna_stopa_entry = tk.Entry(self.window)
        self.trajanje_stednje_entry = tk.Entry(self.window)

        self.iznos_entry.grid(row=0, column=1)
        self.kamatna_stopa_entry.grid(row=1, column=1)
        self.trajanje_stednje_entry.grid(row=2, column=1)

        # Kreiranje gumba za izračun
        tk.Button(self.window, text="Izračunaj", command=self.izracunaj).grid(row=3, column=0, columnspan=2)

        # Kreiranje polja za prikaz rezultata
        tk.Label(self.window, text="Ukupna kamata:").grid(row=4, column=0)
        tk.Label(self.window, text="Mjesečni iznos:").grid(row=5, column=0)

        self.ukupna_kamata_label = tk.Label(self.window, text="")
        self.mjesečni_iznos_label = tk.Label(self.window, text="")

        self.ukupna_kamata_label.grid(row=4, column=1)
        self.mjesečni_iznos_label.grid(row=5, column=1)

    def izracunaj(self):
        try:
            iznos = float(self.iznos_entry.get())
            kamatna_stopa = float(self.kamatna_stopa_entry.get()) / 100 / 12
            trajanje_stednje = int(self.trajanje_stednje_entry.get())

            ukupna_kamata = iznos * kamatna_stopa * trajanje_stednje
            mjesečni_iznos = (iznos + ukupna_kamata) / trajanje_stednje

            self.ukupna_kamata_label.config(text=f"{ukupna_kamata:.2f}")
            self.mjesečni_iznos_label.config(text=f"{mjesečni_iznos:.2f}")
        except ValueError:
            self.ukupna_kamata_label.config(text="Greška")
            self.mjesečni_iznos_label.config(text="Greška")

    def pokreni(self):
        self.window.mainloop()

if __name__ == "__main__":
    kalkulator = KalkulatorKamata()
    kalkulator.pokreni()