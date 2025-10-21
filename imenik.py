import tkinter as tk
from tkinter import messagebox
import csv
import os

class Kontakt:
    def __init__(self, ime, email, telefon):
        self.ime = ime
        self.email = email
        self.telefon = telefon

    def __str__(self):
        return f"{self.ime} - {self.email} "

class ImenikApp:
    def __init__(self, root):
        self.kontakti = []
        self.root = root
        self.root.title("Digitalni imenik")

    
        for i in range(2):  
            root.columnconfigure(i, weight=1)
        for i in range(7):  
            root.rowconfigure(i, weight=1)


        tk.Label(root, text="Ime i prezime:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.ime_entry = tk.Entry(root)
        self.ime_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(root, text="Email:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.email_entry = tk.Entry(root)
        self.email_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)

        tk.Label(root, text="Telefon:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.telefon_entry = tk.Entry(root)
        self.telefon_entry.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

    
        tk.Button(root, text="Dodaj kontakt", command=self.dodaj_kontakt).grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        tk.Button(root, text="Obriši kontakt", command=self.obrisi_kontakt).grid(row=4, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        tk.Button(root, text="Spremi kontakte", command=self.spremi_kontakte).grid(row=6, column=0, sticky="ew", padx=5, pady=5)
        tk.Button(root, text="Učitaj kontakte", command=self.ucitaj_kontakte).grid(row=6, column=1, sticky="ew", padx=5, pady=5)


        self.listbox = tk.Listbox(root)
        self.listbox.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        self.ucitaj_kontakte()

    def dodaj_kontakt(self):
        ime = self.ime_entry.get().strip()
        email = self.email_entry.get().strip()
        telefon = self.telefon_entry.get().strip()

        if not ime or not email or not telefon:
            messagebox.showerror("Greška", "Popuni sva polja!")
            return
        if  len(ime) <3:
            messagebox.showerror("Greška", "Ime treba imati najmanje tri znaka!")
            return
        if  len(telefon) <10:
            messagebox.showerror("Greška", "Telefon treba imati 10 znakova!")
            return

        if "@" not in email or "." not in email:
            messagebox.showerror("Greška", "Neispravan email!")
            return

        if not telefon.isdigit():
            messagebox.showerror("Greška", "Telefon mora sadržavati samo brojeve!")
            return

        kontakt = Kontakt(ime, email, telefon)
        self.kontakti.append(kontakt)
        self.osvjezi_listu()

        self.ime_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.telefon_entry.delete(0, tk.END)

    def obrisi_kontakt(self):
        selekcija = self.listbox.curselection()
        if not selekcija:
            messagebox.showwarning("Upozorenje", "Odaberite kontakt koji želite obrisati!")
            return
        index = selekcija[0]
        del self.kontakti[index]
        self.osvjezi_listu()
        self.spremi_kontakte() 
    def osvjezi_listu(self):
        self.listbox.delete(0, tk.END)
        for kontakt in self.kontakti:
            self.listbox.insert(tk.END, str(kontakt))

    def spremi_kontakte(self):
        try:
            with open("kontakti.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                for k in self.kontakti:
                    writer.writerow([k.ime, k.email, k.telefon])
            messagebox.showinfo("Uspjeh", "Kontakti su spremljeni!")
        except Exception as e:
            messagebox.showerror("Greška", f"Greška pri spremanju: {e}")

    def ucitaj_kontakte(self):
        self.kontakti.clear()
        if os.path.exists("kontakti.csv"):
            try:
                with open("kontakti.csv", "r", newline="", encoding="utf-8") as f:
                    reader = csv.reader(f)
                    for red in reader:
                        if len(red) == 3:
                            self.kontakti.append(Kontakt(*red))
            except Exception as e:
                messagebox.showerror("Greška", f"Greška pri učitavanju: {e}")
        self.osvjezi_listu()

if __name__ == "__main__":
    root = tk.Tk()
    app = ImenikApp(root)
    root.mainloop()
