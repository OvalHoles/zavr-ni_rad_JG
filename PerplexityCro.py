import tkinter as tk
from tkinter import messagebox

class KalkulatorKamate:
    def __init__(self, root):
        self.root = root
        self.root.title("Kalkulator kamate")
        self._kreiraj_sucelje()
        self.entry_iznos.focus_set()

        # Dodaj Enter kao prečac za izračun
        self.root.bind('<Return>', lambda event: self.izracunaj())

    def _kreiraj_sucelje(self):
        # Glavni okvir za unos podataka
        frame_unos = tk.Frame(self.root, padx=15, pady=15)
        frame_unos.pack(fill="x", padx=10, pady=10)

        tk.Label(frame_unos, text="Unesite osnovne podatke za izračun kamate", font=("Arial", 12, "bold")).pack(pady=(0,10))

        # Iznos
        row1 = tk.Frame(frame_unos)
        row1.pack(fill="x", pady=5)
        tk.Label(row1, text="Osnovni iznos (kn):", width=20, anchor='w').pack(side="left")
        self.entry_iznos = tk.Entry(row1)
        self.entry_iznos.pack(side="right", fill="x", expand=True)

        # Kamatna stopa
        row2 = tk.Frame(frame_unos)
        row2.pack(fill="x", pady=5)
        tk.Label(row2, text="Godišnja kamatna stopa (%):", width=20, anchor='w').pack(side="left")
        self.entry_kamata = tk.Entry(row2)
        self.entry_kamata.pack(side="right", fill="x", expand=True)

        # Mjeseci
        row3 = tk.Frame(frame_unos)
        row3.pack(fill="x", pady=5)
        tk.Label(row3, text="Trajanje štednje (mjeseci):", width=20, anchor='w').pack(side="left")
        self.entry_mjeseci = tk.Entry(row3)
        self.entry_mjeseci.pack(side="right", fill="x", expand=True)

        # Gumb za izračun
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill="x", padx=10, pady=(0,10))
        btn_izracunaj = tk.Button(btn_frame, text="Izračunaj", command=self.izracunaj)
        btn_izracunaj.pack(fill="x")

        # Okvir za rezultate
        frame_izlaz = tk.LabelFrame(self.root, text="Rezultati", padx=15, pady=15)
        frame_izlaz.pack(fill="both", expand=True, padx=10, pady=10)

        self.label_mjesecna_kamata = tk.Label(frame_izlaz, text="Mjesečna kamata: -")
        self.label_mjesecna_kamata.pack(anchor="w", pady=5)

        self.label_ukupna_kamata = tk.Label(frame_izlaz, text="Ukupna kamata: -")
        self.label_ukupna_kamata.pack(anchor="w", pady=5)

        self.label_ukupan_iznos = tk.Label(frame_izlaz, text="Ukupan iznos: -")
        self.label_ukupan_iznos.pack(anchor="w", pady=5)

    def izracunaj(self):
        try:
            iznos = float(self.entry_iznos.get())
            god_kamata = float(self.entry_kamata.get())
            mjeseci = int(self.entry_mjeseci.get())

            if not self._validiraj_unos(iznos, god_kamata, mjeseci):
                return

            mjesecna_kamata, ukupna_kamata, ukupan_iznos = self._izracunaj_kamate(iznos, god_kamata, mjeseci)
            self._prikazi_rezultate(mjesecna_kamata, ukupna_kamata, ukupan_iznos)

        except ValueError:
            messagebox.showerror("Greška", "Molimo unesite valjane brojeve!")

    def _validiraj_unos(self, iznos, god_kamata, mjeseci):
        if iznos <= 0 or god_kamata < 0 or mjeseci <= 0:
            messagebox.showerror("Greška", "Molimo unesite pozitivne vrijednosti!")
            return False
        return True

    def _izracunaj_kamate(self, iznos, god_kamata, mjeseci):
        mjesecna_kamata_stopa = god_kamata / 100 / 12
        mjesecna_kamata = iznos * mjesecna_kamata_stopa
        ukupna_kamata = mjesecna_kamata * mjeseci
        ukupan_iznos = iznos + ukupna_kamata
        return mjesecna_kamata, ukupna_kamata, ukupan_iznos

    def _prikazi_rezultate(self, mjesecna_kamata, ukupna_kamata, ukupan_iznos):
        self.label_mjesecna_kamata.config(text=f"Mjesečna kamata: {mjesecna_kamata:.2f} kn")
        self.label_ukupna_kamata.config(text=f"Ukupna kamata: {ukupna_kamata:.2f} kn")
        self.label_ukupan_iznos.config(text=f"Ukupan iznos: {ukupan_iznos:.2f} kn")


if __name__ == "__main__":
    root = tk.Tk()
    app = KalkulatorKamate(root)
    root.mainloop()
