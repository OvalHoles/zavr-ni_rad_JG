import tkinter as tk
from tkinter import messagebox

class KalkulatorKamate:
    def __init__(self, root):
        self.root = root
        self.root.title("Kalkulator jednostavne kamate")
        self.root.geometry("400x300")
        self.root.resizable(False, False)

        self._kreiraj_sucelje()

    def _kreiraj_sucelje(self):
        # Frame za unos podataka
        frame_input = tk.Frame(self.root, padx=10, pady=10)
        frame_input.pack(fill='x')

        # Iznos
        tk.Label(frame_input, text="Iznos (€):", anchor='w').grid(row=0, column=0, sticky='w', pady=5)
        self.entry_iznos = tk.Entry(frame_input)
        self.entry_iznos.grid(row=0, column=1, pady=5, sticky='ew')

        # Godišnja stopa
        tk.Label(frame_input, text="Godišnja kamatna stopa (%):", anchor='w').grid(row=1, column=0, sticky='w', pady=5)
        self.entry_stopa = tk.Entry(frame_input)
        self.entry_stopa.grid(row=1, column=1, pady=5, sticky='ew')

        # Trajanje
        tk.Label(frame_input, text="Trajanje (mjeseci):", anchor='w').grid(row=2, column=0, sticky='w', pady=5)
        self.entry_trajanje = tk.Entry(frame_input)
        self.entry_trajanje.grid(row=2, column=1, pady=5, sticky='ew')

        # Konfiguracija grid kolona za ravnomjernu širinu
        frame_input.columnconfigure(1, weight=1)

        # Gumb za izračun
        tk.Button(self.root, text="Izračunaj", command=self.izracunaj, bg='#4CAF50', fg='white', font=('Arial', 12, 'bold')).pack(pady=15, ipadx=10, ipady=5)

        # Label za rezultate
        self.label_rezultat = tk.Label(self.root, text="", justify='left', font=('Arial', 11))
        self.label_rezultat.pack(padx=10, pady=10, anchor='w')

    def izracunaj(self):
        try:
            iznos = float(self.entry_iznos.get())
            stopa = float(self.entry_stopa.get()) / 100  # pretvaramo u decimalni oblik
            trajanje = int(self.entry_trajanje.get())

            # Validacija
            if iznos <= 0:
                raise ValueError("Iznos mora biti veći od 0.")
            if stopa < 0:
                raise ValueError("Kamatna stopa ne može biti negativna.")
            if trajanje <= 0:
                raise ValueError("Trajanje mora biti veće od 0.")

            mjesecna_kamata, ukupna_kamata, ukupan_iznos = self._izracunaj_kamate(iznos, stopa, trajanje)

            self.label_rezultat.config(
                text=(
                    f"Mjesečni iznos kamate: {mjesecna_kamata:.2f} €\n"
                    f"Ukupna kamata: {ukupna_kamata:.2f} €\n"
                    f"Ukupan iznos nakon isteka: {ukupan_iznos:.2f} €"
                )
            )
        except ValueError as e:
            messagebox.showerror("Greška", str(e))
        except Exception:
            messagebox.showerror("Greška", "Molimo unesite ispravne brojeve.")

    @staticmethod
    def _izracunaj_kamate(iznos: float, stopa: float, trajanje: int):
        mjesecna_kamata = iznos * stopa / 12
        ukupna_kamata = mjesecna_kamata * trajanje
        ukupan_iznos = iznos + ukupna_kamata
        return mjesecna_kamata, ukupna_kamata, ukupan_iznos


if __name__ == "__main__":
    root = tk.Tk()
    app = KalkulatorKamate(root)
    root.mainloop()
