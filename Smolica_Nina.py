# Kratka provjera – Evidencija učenika (CSV fokus, XML bonus)
# Vrijeme: 20 min

#1. RAM (radna memorija) je privremena i sadržaj se gubi čim se aplikacija zatvori ili se računalo ugasi. Trajna pohrana omogućuje da podaci ostanu dostupni i nakon zatvaranja aplikacije.
#2. CSV je jednostavan (lako čitljiv), ali ne podržava opis strukture podataka. Ima tekstualni format s redovima i stupcima (tablično).
#   XML koristi hijerarhijsku strukturu s oznakama (tragovima). Fleksibilniji je, može opisivati tipove podataka i odnose, ali je opsežniji i teže čitljiv.
#3. with open(...) as f automatski zatvara datoteku i štiti od grešaka. Sigurnije je od manualnog zatvaranja.
#4. Stari podaci ostajuvidljivi zajedno s novima zbog čega Listbox treba očistiti prije učitavanja kako bi se izbjeglo dupliranje podataka.
#5. csv.DictWriter/DictReader olakšavaju rad s imenovanim stupcima i izbjegavaju ručnu analizu. Automatski povezuju vrijednosti s imenima stupca. Rješavaju probleme s redoslijedom, praznim poljima, zarezima u tekstu.Pojednostavljuju kod i nema potrebe za ručnom analizom. split(',') ovisi o točnom redoslijedu i broju polja. Ne radi dobro ako polja sadrže zareze i lakše dolazi do grešaka.

import tkinter as tk
from tkinter import messagebox
import csv
import xml.etree.ElementTree as ET


class Ucenik:
    def __init__(self, ime, prezime, razred):
        self.ime = ime
        self.prezime = prezime
        self.razred = razred

    def __str__(self):
        return f"{self.ime} {self.prezime} ({self.razred})"



class EvidencijaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Evidencija učenika – provjera")
        self.root.geometry("600x400")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        self.ucenici = []
        self.odabrani_index = None

        self.kreiraj_gui()

    def kreiraj_gui(self):

        unos = tk.Frame(self.root, padx=10, pady=10, bg="red")
        unos.grid(row=0, column=0, sticky="EW")
        unos.columnconfigure(1, weight=1)

        tk.Label(unos, text="Ime:", bg="green").grid(row=0, column=0, sticky="W")
        self.e_ime = tk.Entry(unos); self.e_ime.grid(row=0, column=1, sticky="EW")

        tk.Label(unos, text="Prezime:", bg="green").grid(row=1, column=0, sticky="W")
        self.e_prezime = tk.Entry(unos); self.e_prezime.grid(row=1, column=1, sticky="EW")

        tk.Label(unos, text="Razred:", bg="green").grid(row=2, column=0, sticky="W")
        self.e_razred = tk.Entry(unos); self.e_razred.grid(row=2, column=1, sticky="EW")

        gumbi = tk.Frame(unos); gumbi.grid(row=3, column=0, columnspan=2, pady=8)
        tk.Button(gumbi, text="Dodaj učenika", bg="purple", command=self.dodaj_ucenika).pack(side="left", padx=4)


        tk.Button(gumbi, text="Spremi CSV", bg="pink", command=self.spremi_u_csv).pack(side="left", padx=4)
        tk.Button(gumbi, text="Učitaj CSV", bg="yellow", command=self.ucitaj_iz_csv).pack(side="left", padx=4 )


        tk.Button(gumbi, text="Spremi XML", bg="blue" ,command=self.spremi_u_xml).pack(side="left", padx=4)
        tk.Button(gumbi, text="Učitaj XML", bg="orange", command=self.ucitaj_iz_xml).pack(side="left", padx=4)


        prikaz = tk.Frame(self.root, padx=10, pady=10)
        prikaz.grid(row=1, column=0, sticky="NSEW")
        prikaz.columnconfigure(0, weight=1)
        prikaz.rowconfigure(0, weight=1)

        self.lb = tk.Listbox(prikaz)
        self.lb.grid(row=0, column=0, sticky="NSEW")

        sc = tk.Scrollbar(prikaz, orient="vertical", command=self.lb.yview)
        sc.grid(row=0, column=1, sticky="NS")
        self.lb.configure(yscrollcommand=sc.set)

        self.lb.bind("<<ListboxSelect>>", self.odaberi)


    def osvjezi(self):
        self.lb.delete(0, tk.END)
        for u in self.ucenici:
            self.lb.insert(tk.END, str(u))

    def ocisti_unos(self):
        self.e_ime.delete(0, tk.END)
        self.e_prezime.delete(0, tk.END)
        self.e_razred.delete(0, tk.END)


    def dodaj_ucenika(self):
        ime = self.e_ime.get().strip()
        prezime = self.e_prezime.get().strip()
        razred = self.e_razred.get().strip()
        if not (ime and prezime and razred):
            messagebox.showwarning("Upozorenje", "Sva polja moraju biti popunjena.")
            return
        self.ucenici.append(Ucenik(ime, prezime, razred))
        self.osvjezi()
        self.ocisti_unos()

    def odaberi(self, _e):
        sel = self.lb.curselection()
        if not sel: 
            self.odabrani_index = None
            return
        self.odabrani_index = sel[0]


    def spremi_u_csv(self):
        """TODO (B-1): Zapiši sve učenike u 'ucenici.csv' pomoću csv.DictWriter.
        Zaglavlja: ime, prezime, razred.
        """

        try:
            with open("ucenici.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["ime", "prezime", "razred"])
                writer.writeheader()
                for u in self.ucenici:
                    writer.writerow({"ime": u.ime, "prezime": u.prezime, "razred": u.razred})
            messagebox.showinfo("Info", "Podaci su spremljeni u ucenici.csv")
        except Exception as e:
            messagebox.showerror("Greška", f"Nije moguće spremiti CSV: {e}")

    def ucitaj_iz_csv(self):
        """TODO (B-2): Učitaj iz 'ucenici.csv' pomoću csv.DictReader.
        1) Očisti self.ucenici i Listbox.
        2) Za svaki red u CSV-u, kreiraj objekt Ucenik i dodaj u listu.
        3) Osvježi prikaz. Obradi FileNotFoundError.
        """
        try:
            self.ucenici.clear()
            self.lb.delete(0, tk.END)
            with open("ucenici.csv", "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.ucenici.append(Ucenik(row["ime"], row["prezime"], row["razred"]))
            self.osvjezi()
            messagebox.showinfo("Info", "Podaci su učitani iz ucenici.csv")
        except FileNotFoundError:
            messagebox.showwarning("Upozorenje", "Datoteka ucenici.csv ne postoji.")
        except Exception as e:
            messagebox.showerror("Greška", f"Nije moguće učitati CSV: {e}")


    def spremi_u_xml(self):
        """BONUS: Spremi u 'ucenici.xml' koristeći ElementTree."""
        try:
            root = ET.Element("evidencija")
            for u in self.ucenici:
                e = ET.SubElement(root, "ucenik")
                ET.SubElement(e, "ime").text = u.ime
                ET.SubElement(e, "prezime").text = u.prezime
                ET.SubElement(e, "razred").text = u.razred
            tree = ET.ElementTree(root)
            tree.write("ucenici.xml", encoding="utf-8", xml_declaration=True)
            messagebox.showinfo("Info", "XML spremljen u ucenici.xml")
        except Exception as e:
            messagebox.showerror("Greška", f"Nije moguće spremiti XML: {e}")

    def ucitaj_iz_xml(self):
        """BONUS: Učitaj iz 'ucenici.xml' koristeći ElementTree."""
        try:
            self.ucenici.clear()
            self.lb.delete(0, tk.END)
            tree = ET.parse("ucenici.xml")
            root = tree.getroot()
            for e in root.findall("ucenik"):
                ime = e.findtext("ime", default="")
                prezime = e.findtext("prezime", default="")
                razred = e.findtext("razred", default="")
                if ime and prezime and razred:
                    self.ucenici.append(Ucenik(ime, prezime, razred))
            self.osvjezi()
            messagebox.showinfo("Info", "XML učitan iz ucenici.xml")
        except FileNotFoundError:
            messagebox.showwarning("Upozorenje", "Datoteka ucenici.xml ne postoji.")
        except Exception as e:
            messagebox.showerror("Greška", f"Nije moguće učitati XML: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = EvidencijaApp(root)
    root.mainloop()
