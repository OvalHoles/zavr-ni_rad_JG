import tkinter as tk
from tkinter import messagebox

class KalkulatorKamate:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("💰 Kalkulator Kamate")
        self.root.geometry("360x400")
        self.root.resizable(False, False)
        self.kreiraj_sucelje()

    def kreiraj_sucelje(self) -> None:
        # Glavni okvir
        okvir = tk.Frame(self.root, padx=20, pady=20)
        okvir.pack(fill="both", expand=True)

        # Naslov
        tk.Label(okvir, text="Izračun jednostavne kamate", font=("Arial", 14, "bold")).pack(pady=10)

        # Polja za unos
        self.entry_iznos = self.kreiraj_polje(okvir, "Iznos (€):")
        self.entry_kamata = self.kreiraj_polje(okvir, "Godišnja kamata (%):")
        self.entry_mjeseci = self.kreiraj_polje(okvir, "Trajanje (mjeseci):")

        # Gumbi
        gumb_okvir = tk.Frame(okvir)
        gumb_okvir.pack(pady=10)

        tk.Button(gumb_okvir, text="Izračunaj", width=12, command=self.izracunaj).pack(side="left", padx=5)
        tk.Button(gumb_okvir, text="Resetiraj", width=12, command=self.resetiraj).pack(side="left", padx=5)

        # Rezultat
        self.label_rezultat = tk.Label(okvir, text="", font=("Arial", 12), fg="blue", justify="left")
        self.label_rezultat.pack(pady=15)

        # Fokus na prvo polje
        self.entry_iznos.focus()

    def kreiraj_polje(self, parent: tk.Frame, label_text: str) -> tk.Entry:
        tk.Label(parent, text=label_text, font=("Arial", 10)).pack(anchor="w", pady=(10, 0))
        entry = tk.Entry(parent, font=("Arial", 10), width=30)
        entry.pack()
        return entry

    def izracunaj(self) -> None:
        try:
            iznos = float(self.entry_iznos.get())
            kamata = float(self.entry_kamata.get())
            mjeseci = int(self.entry_mjeseci.get())

            if iznos <= 0 or kamata <= 0 or mjeseci <= 0:
                messagebox.showerror("Neispravan unos", "Sve vrijednosti moraju biti pozitivni brojevi.")
                return

            ukupna_kamata, mjesecna_kamata, ukupan_iznos = self.izracunaj_kamatu(iznos, kamata, mjeseci)

            self.label_rezultat.config(
                text=(
                    f"📊 Rezultati:\n"
                    f"• Ukupna kamata: {ukupna_kamata:.2f} €\n"
                    f"• Mjesečna kamata: {mjesecna_kamata:.2f} €\n"
                    f"• Ukupan iznos na kraju: {ukupan_iznos:.2f} €"
                )
            )
        except ValueError:
            messagebox.showerror("Greška", "Unesite ispravne brojčane vrijednosti.")

    def resetiraj(self) -> None:
        self.entry_iznos.delete(0, tk.END)
        self.entry_kamata.delete(0, tk.END)
        self.entry_mjeseci.delete(0, tk.END)
        self.label_rezultat.config(text="")
        self.entry_iznos.focus()

    @staticmethod
    def izracunaj_kamatu(iznos: float, kamata: float, mjeseci: int) -> tuple[float, float, float]:
        ukupna_kamata = (iznos * kamata * mjeseci) / (100 * 12)
        mjesecna_kamata = ukupna_kamata / mjeseci
        ukupan_iznos = iznos + ukupna_kamata
        return ukupna_kamata, mjesecna_kamata, ukupan_iznos

# Pokretanje aplikacije
if __name__ == "__main__":
    root = tk.Tk()
    app = KalkulatorKamate(root)
    root.mainloop()
