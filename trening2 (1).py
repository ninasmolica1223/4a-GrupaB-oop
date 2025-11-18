
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
import os
from datetime import datetime

APP_NAME = "FITAPP"
VERSION = "1.0"
AUTHOR = "Nina Smolica"
COLOR_BG = "#f0f4f3"
COLOR_MAIN = "#a5d6a7"
COLOR_ACCENT = "#1b5e20"
COLOR_BUTTON = "#66bb6a"


LOGO = """
      🍽️💪
  FITAPP PLANNER
"""


class StavkaPlana(ABC):
    def __init__(self, naziv, datum, vrijeme):
        self.naziv = naziv
        self.datum = datum
        self.vrijeme = vrijeme

    def sort_key(self):
        return datetime.strptime(f"{self.datum} {self.vrijeme}", "%Y-%m-%d %H:%M")

    @abstractmethod
    def __str__(self):
        pass


class Obrok(StavkaPlana):
    def __init__(self, naziv, datum, vrijeme, kcal, proteini, ugljikohidrati, masti):
        super().__init__(naziv, datum, vrijeme)
        self.kcal = kcal
        self.proteini = proteini
        self.ugljikohidrati = ugljikohidrati
        self.masti = masti

    def __str__(self):
        return f"🍽️ {self.naziv} ({self.datum} {self.vrijeme}) - {self.kcal} kcal, P:{self.proteini}g U:{self.ugljikohidrati}g M:{self.masti}g"


class Trening(StavkaPlana):
    def __init__(self, naziv, datum, vrijeme, tip, trajanje, misicna_skupina):
        super().__init__(naziv, datum, vrijeme)
        self.tip = tip
        self.trajanje = trajanje
        self.misicna_skupina = misicna_skupina

    def __str__(self):
        return f"🏋️ {self.naziv} ({self.datum} {self.vrijeme}) - {self.tip}, {self.trajanje} min ({self.misicna_skupina})"


class FitnessApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"{APP_NAME} v{VERSION}")
        self.root.geometry("850x720")
        self.root.config(bg=COLOR_BG)

        self.stavke = []
        self.edit_index = None

        self.create_menu()
        self.create_main_interface()
        self.create_status_bar()


    def create_menu(self):
        menu_bar = tk.Menu(self.root)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Spremi XML", command=self.spremi_xml)
        file_menu.add_command(label="Učitaj XML", command=self.ucitaj_xml)
        file_menu.add_separator()
        file_menu.add_command(label="Izlaz", command=self.root.quit)
        menu_bar.add_cascade(label="📁 Datoteka", menu=file_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="Analiza makronutrijenata", command=self.show_macro_analysis)
        help_menu.add_command(label="O aplikaciji", command=self.show_about_window)
        menu_bar.add_cascade(label="❓ Pomoć", menu=help_menu)

        self.root.config(menu=menu_bar)


    def create_status_bar(self):
        self.status_var = tk.StringVar()
        self.status_var.set("Spremno")
        status_bar = tk.Label(self.root, textvariable=self.status_var, bg=COLOR_ACCENT, fg="white", anchor="w", padx=10)
        status_bar.pack(fill="x", side="bottom")

    def create_main_interface(self):
        frame = tk.Frame(self.root, bg=COLOR_MAIN, padx=10, pady=10)
        frame.pack(fill="both", expand=True)

        logo_label = tk.Label(frame, text=LOGO, bg=COLOR_MAIN, fg=COLOR_ACCENT, font=("Courier", 18, "bold"))
        logo_label.grid(row=0, column=0, columnspan=3, pady=10)

        tk.Label(frame, text="Naziv:", bg=COLOR_MAIN).grid(row=1, column=0, sticky="w")
        self.naziv_entry = tk.Entry(frame)
        self.naziv_entry.grid(row=1, column=1, sticky="ew")

        tk.Label(frame, text="Datum (YYYY-MM-DD):", bg=COLOR_MAIN).grid(row=2, column=0, sticky="w")
        self.datum_entry = tk.Entry(frame)
        self.datum_entry.grid(row=2, column=1, sticky="ew")

        tk.Label(frame, text="Vrijeme (HH:MM):", bg=COLOR_MAIN).grid(row=3, column=0, sticky="w")
        self.vrijeme_entry = tk.Entry(frame)
        self.vrijeme_entry.grid(row=3, column=1, sticky="ew")

        tk.Label(frame, text="Tip stavke:", bg=COLOR_MAIN).grid(row=4, column=0, sticky="w")
        self.tip_combobox = ttk.Combobox(frame, values=["Obrok", "Trening"], state="readonly")
        self.tip_combobox.grid(row=4, column=1, sticky="ew")
        self.tip_combobox.bind("<<ComboboxSelected>>", self.update_form)

        frame.columnconfigure(1, weight=1)

        self.dynamic_frame = tk.Frame(frame, bg=COLOR_MAIN)
        self.dynamic_frame.grid(row=5, column=0, columnspan=3, sticky="nsew")

        self.listbox = tk.Listbox(frame, height=15, bg="#e8f5e9")
        self.listbox.grid(row=6, column=0, columnspan=3, sticky="nsew", pady=10)

        button_frame = tk.Frame(frame, bg=COLOR_MAIN)
        button_frame.grid(row=7, column=0, columnspan=3, pady=5)

        self.btn_add = tk.Button(button_frame, text="Dodaj stavku", command=self.dodaj_stavku,
                                 bg=COLOR_BUTTON, fg="white", width=16)
        self.btn_add.grid(row=0, column=0, padx=5)

        self.btn_edit = tk.Button(button_frame, text="Uredi odabrano", command=self.uredi_stavku,
                                  bg=COLOR_BUTTON, fg="white", width=16)
        self.btn_edit.grid(row=0, column=1, padx=5)

        self.btn_save_edit = tk.Button(button_frame, text="Spremi izmjenu", command=self.spremi_izmjenu,
                                       state="disabled", bg="#bdbdbd", fg="white", width=16)
        self.btn_save_edit.grid(row=0, column=2, padx=5)

        tk.Button(button_frame, text="Svi unosi", command=self.prikazi_sve,
                  bg=COLOR_BUTTON, fg="white", width=16).grid(row=0, column=3, padx=5)
        tk.Button(button_frame, text="Obroci", command=self.prikazi_obroke,
                  bg=COLOR_BUTTON, fg="white", width=16).grid(row=0, column=4, padx=5)
        tk.Button(button_frame, text="Treninzi", command=self.prikazi_treninge,
                  bg=COLOR_BUTTON, fg="white", width=16).grid(row=0, column=5, padx=5)

    def update_form(self, event):
        for widget in self.dynamic_frame.winfo_children():
            widget.destroy()

        tip = self.tip_combobox.get()

        if tip == "Obrok":
            labels = ["Kcal:", "Proteini (g):", "Ugljikohidrati (g):", "Masti (g):"]
            self.entries = [tk.Entry(self.dynamic_frame) for _ in labels]
            for i, lbl in enumerate(labels):
                tk.Label(self.dynamic_frame, text=lbl, bg=COLOR_MAIN).grid(row=i, column=0)
                self.entries[i].grid(row=i, column=1)
        else:
            tk.Label(self.dynamic_frame, text="Tip treninga:", bg=COLOR_MAIN).grid(row=0, column=0)
            self.tip_treninga_combobox = ttk.Combobox(self.dynamic_frame, values=["Snaga", "Kardio"], state="readonly")
            self.tip_treninga_combobox.grid(row=0, column=1)

            tk.Label(self.dynamic_frame, text="Trajanje (min):", bg=COLOR_MAIN).grid(row=1, column=0)
            self.trajanje_entry = tk.Entry(self.dynamic_frame)
            self.trajanje_entry.grid(row=1, column=1)

            tk.Label(self.dynamic_frame, text="Mišićna skupina:", bg=COLOR_MAIN).grid(row=2, column=0)
            self.misicna_skupina_entry = tk.Entry(self.dynamic_frame)
            self.misicna_skupina_entry.grid(row=2, column=1)


    def dodaj_stavku(self):
        try:
            naziv = self.naziv_entry.get().strip()
            datum = self.datum_entry.get().strip()
            vrijeme = self.vrijeme_entry.get().strip()
            tip = self.tip_combobox.get()

            if not (naziv and datum and vrijeme and tip):
                raise ValueError("Sva osnovna polja moraju biti popunjena!")

            if tip == "Obrok":
                kcal, p, u, m = [int(e.get()) for e in self.entries]
                stavka = Obrok(naziv, datum, vrijeme, kcal, p, u, m)
            else:
                tip_t = self.tip_treninga_combobox.get()
                trajanje = int(self.trajanje_entry.get())
                misicna = self.misicna_skupina_entry.get()
                stavka = Trening(naziv, datum, vrijeme, tip_t, trajanje, misicna)

            self.stavke.append(stavka)
            self.osvjezi_listbox()
            self.status_var.set(f"Ukupno stavki: {len(self.stavke)}")

        except Exception as e:
            messagebox.showerror("Greška", str(e))


    def uredi_stavku(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("Upozorenje", "Odaberi stavku za uređivanje.")
            return

        self.edit_index = sel[0]
        stavka = self.stavke[self.edit_index]

        self.naziv_entry.delete(0, tk.END)
        self.naziv_entry.insert(0, stavka.naziv)

        self.datum_entry.delete(0, tk.END)
        self.datum_entry.insert(0, stavka.datum)

        self.vrijeme_entry.delete(0, tk.END)
        self.vrijeme_entry.insert(0, stavka.vrijeme)

        if isinstance(stavka, Obrok):
            self.tip_combobox.set("Obrok")
            self.update_form(None)

            values = [stavka.kcal, stavka.proteini, stavka.ugljikohidrati, stavka.masti]
            for e, v in zip(self.entries, values):
                e.delete(0, tk.END)
                e.insert(0, v)

        else:
            self.tip_combobox.set("Trening")
            self.update_form(None)

            self.tip_treninga_combobox.set(stavka.tip)
            self.trajanje_entry.delete(0, tk.END)
            self.trajanje_entry.insert(0, stavka.trajanje)

            self.misicna_skupina_entry.delete(0, tk.END)
            self.misicna_skupina_entry.insert(0, stavka.misicna_skupina)

        self.btn_save_edit.config(state="normal", bg=COLOR_BUTTON)


    def spremi_izmjenu(self):
        if self.edit_index is None:
            return

        try:
            naziv = self.naziv_entry.get().strip()
            datum = self.datum_entry.get().strip()
            vrijeme = self.vrijeme_entry.get().strip()
            tip = self.tip_combobox.get()

            if tip == "Obrok":
                kcal, p, u, m = [int(e.get()) for e in self.entries]
                nova = Obrok(naziv, datum, vrijeme, kcal, p, u, m)
            else:
                tip_t = self.tip_treninga_combobox.get()
                trajanje = int(self.trajanje_entry.get())
                misicna = self.misicna_skupina_entry.get()
                nova = Trening(naziv, datum, vrijeme, tip_t, trajanje, misicna)

            self.stavke[self.edit_index] = nova
            self.edit_index = None

            self.btn_save_edit.config(state="disabled", bg="#bdbdbd")

            self.osvjezi_listbox()
            self.status_var.set("Stavka uspješno izmijenjena!")

        except Exception as e:
            messagebox.showerror("Greška", str(e))


    def osvjezi_listbox(self, tip=None):
        self.listbox.delete(0, tk.END)
        self.stavke.sort(key=lambda x: x.sort_key())

        for s in self.stavke:
            if tip == "Obrok" and not isinstance(s, Obrok):
                continue
            if tip == "Trening" and not isinstance(s, Trening):
                continue
            self.listbox.insert(tk.END, str(s))

    def prikazi_sve(self): self.osvjezi_listbox()
    def prikazi_obroke(self): self.osvjezi_listbox("Obrok")
    def prikazi_treninge(self): self.osvjezi_listbox("Trening")

    def spremi_xml(self):
        try:
            path = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML datoteke", "*.xml")])
            if not path:
                return

            root = ET.Element("plan")
            for s in self.stavke:
                e = ET.SubElement(root, "obrok" if isinstance(s, Obrok) else "trening")
                for k, v in s.__dict__.items():
                    ET.SubElement(e, k).text = str(v)

            ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)
            messagebox.showinfo("Spremanje", "Podaci spremljeni!")
            self.status_var.set("Podaci spremljeni.")

        except Exception as e:
            messagebox.showerror("Greška", str(e))

    def ucitaj_xml(self):
        try:
            path = filedialog.askopenfilename(filetypes=[("XML datoteke", "*.xml")])
            if not path or not os.path.exists(path):
                return

            self.stavke.clear()
            root = ET.parse(path).getroot()

            for el in root:
                d = {c.tag: c.text for c in el}
                if el.tag == "obrok":
                    self.stavke.append(Obrok(d["naziv"], d["datum"], d["vrijeme"],
                                              int(d["kcal"]), int(d["proteini"]),
                                              int(d["ugljikohidrati"]), int(d["masti"])))
                else:
                    self.stavke.append(Trening(d["naziv"], d["datum"], d["vrijeme"],
                                               d["tip"], int(d["trajanje"]), d["misicna_skupina"]))

            self.osvjezi_listbox()
            self.status_var.set(f"Učitano {len(self.stavke)} stavki.")

        except Exception as e:
            messagebox.showerror("Greška", str(e))


    def show_macro_analysis(self):
        obroci = [s for s in self.stavke if isinstance(s, Obrok)]
        if not obroci:
            messagebox.showinfo("Analiza", "Nema unesenih obroka.")
            return

        P = sum(o.proteini for o in obroci)
        U = sum(o.ugljikohidrati for o in obroci)
        M = sum(o.masti for o in obroci)

        kcalP = P * 4
        kcalU = U * 4
        kcalM = M * 9
        total = kcalP + kcalU + kcalM

        p_pct = round(kcalP / total * 100)
        u_pct = round(kcalU / total * 100)
        m_pct = round(kcalM / total * 100)

        win = tk.Toplevel(self.root)
        win.title("Analiza makronutrijenata")
        win.geometry("350x250")
        win.config(bg=COLOR_MAIN)

        tk.Label(win, text="Analiza makronutrijenata", font=("Helvetica", 14, "bold"),
                 bg=COLOR_MAIN, fg=COLOR_ACCENT).pack(pady=10)

        tk.Label(win,
                 text=f"Proteini: {p_pct}%\n"
                      f"Ugljikohidrati: {u_pct}%\n"
                      f"Masti: {m_pct}%",
                 font=("Helvetica", 12),
                 bg=COLOR_MAIN).pack(pady=20)

        tk.Button(win, text="Zatvori", command=win.destroy,
                  bg=COLOR_BUTTON, fg="white").pack(pady=10)


    def show_about_window(self):
        about_win = tk.Toplevel(self.root)
        about_win.title(f"O {APP_NAME}")
        about_win.geometry("400x300")
        about_win.config(bg=COLOR_MAIN)
        about_win.resizable(False, False)

        tk.Label(about_win, text=LOGO, bg=COLOR_MAIN, fg=COLOR_ACCENT,
                 font=("Courier", 16, "bold")).pack(pady=10)

        tk.Label(about_win, text=APP_NAME, bg=COLOR_MAIN, fg=COLOR_ACCENT,
                 font=("Helvetica", 14, "bold")).pack(pady=5)
        tk.Label(about_win, text=f"Verzija: {VERSION}", bg=COLOR_MAIN,
                 fg=COLOR_ACCENT, font=("Helvetica", 12)).pack()
        tk.Label(about_win, text=f"Autor: {AUTHOR}", bg=COLOR_MAIN,
                 fg=COLOR_ACCENT, font=("Helvetica", 12)).pack()

        tk.Button(about_win, text="Zatvori", command=about_win.destroy,
                  bg=COLOR_BUTTON, fg="white").pack(pady=20)



if __name__ == "__main__":
    root = tk.Tk()
    app = FitnessApp(root)
    root.mainloop()
