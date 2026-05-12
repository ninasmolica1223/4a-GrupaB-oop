import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import csv

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB = True
except:
    MATPLOTLIB = False


# =========================
# LANGUAGE SYSTEM
# =========================
LANG = {}

TRANSLATIONS = {

    # CROATIAN
    "hr": {
        "table": "Tablica",
        "add": "Dodaj unos",
        "dashboard": "Pregled",
        "graph": "Graf",
        "export": "Izvoz CSV",
        "save": "Spremi",
        "delete": "Obriši",
        "records": "Zapisi",
        "ready": "Spremno"
    },

    # ENGLISH
    "en": {
        "table": "Table",
        "add": "Add Entry",
        "dashboard": "Dashboard",
        "graph": "Graph",
        "export": "Export CSV",
        "save": "Save",
        "delete": "Delete",
        "records": "Records",
        "ready": "Ready"
    },

    # SWEDISH
    "se": {
        "table": "Tabell",
        "add": "Lägg till",
        "dashboard": "Översikt",
        "graph": "Graf",
        "export": "Exportera CSV",
        "save": "Spara",
        "delete": "Ta bort",
        "records": "Poster",
        "ready": "Redo"
    },

    # ITALIAN
    "it": {
        "table": "Tabella",
        "add": "Aggiungi",
        "dashboard": "Cruscotto",
        "graph": "Grafico",
        "export": "Esporta CSV",
        "save": "Salva",
        "delete": "Elimina",
        "records": "Record",
        "ready": "Pronto"
    },

    # FRENCH
    "fr": {
        "table": "Tableau",
        "add": "Ajouter",
        "dashboard": "Tableau de bord",
        "graph": "Graphique",
        "export": "Exporter CSV",
        "save": "Enregistrer",
        "delete": "Supprimer",
        "records": "Entrées",
        "ready": "Prêt"
    },

    # GERMAN
    "de": {
        "table": "Tabelle",
        "add": "Eintrag hinzufügen",
        "dashboard": "Übersicht",
        "graph": "Diagramm",
        "export": "CSV exportieren",
        "save": "Speichern",
        "delete": "Löschen",
        "records": "Einträge",
        "ready": "Bereit"
    },

    # SPANISH
    "es": {
        "table": "Tabla",
        "add": "Agregar",
        "dashboard": "Panel",
        "graph": "Gráfico",
        "export": "Exportar CSV",
        "save": "Guardar",
        "delete": "Eliminar",
        "records": "Registros",
        "ready": "Listo"
    },

    # PORTUGUESE
    "pt": {
        "table": "Tabela",
        "add": "Adicionar",
        "dashboard": "Painel",
        "graph": "Gráfico",
        "export": "Exportar CSV",
        "save": "Salvar",
        "delete": "Excluir",
        "records": "Registros",
        "ready": "Pronto"
    },

    # SERBIAN
    "rs": {
        "table": "Tabela",
        "add": "Dodaj",
        "dashboard": "Pregled",
        "graph": "Grafik",
        "export": "Izvezi CSV",
        "save": "Sačuvaj",
        "delete": "Obriši",
        "records": "Zapisi",
        "ready": "Spremno"
    },

    # SLOVENIAN
    "si": {
        "table": "Tabela",
        "add": "Dodaj",
        "dashboard": "Nadzorna plošča",
        "graph": "Graf",
        "export": "Izvozi CSV",
        "save": "Shrani",
        "delete": "Izbriši",
        "records": "Zapisi",
        "ready": "Pripravljeno"
    },

    # CZECH
    "cz": {
        "table": "Tabulka",
        "add": "Přidat",
        "dashboard": "Přehled",
        "graph": "Graf",
        "export": "Export CSV",
        "save": "Uložit",
        "delete": "Smazat",
        "records": "Záznamy",
        "ready": "Připraveno"
    },

    # POLISH
    "pl": {
        "table": "Tabela",
        "add": "Dodaj",
        "dashboard": "Panel",
        "graph": "Wykres",
        "export": "Eksport CSV",
        "save": "Zapisz",
        "delete": "Usuń",
        "records": "Rekordy",
        "ready": "Gotowe"
    }
}


def set_lang(code):
    global LANG
    LANG = TRANSLATIONS[code]


# =========================
# COLORS
# =========================
class Colors:
    BG = "#f1f5f9"
    CARD = "#ffffff"

    DARK = "#0f172a"
    SIDEBAR = "#111827"

    BLUE = "#3b82f6"
    GREEN = "#22c55e"
    ORANGE = "#f97316"
    RED = "#ef4444"
    PURPLE = "#8b5cf6"


# =========================
# DATABASE
# =========================
class Database:
    def __init__(self):
        self.conn = sqlite3.connect("plants.db")

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS plants(
            id INTEGER PRIMARY KEY,
            date TEXT,
            temperature REAL,
            humidity REAL,
            height REAL
        )
        """)

        self.conn.commit()

    def insert(self, d, t, h, he):
        self.conn.execute(
            "INSERT INTO plants(date,temperature,humidity,height) VALUES(?,?,?,?)",
            (d, t, h, he)
        )
        self.conn.commit()

    def fetch(self):
        return self.conn.execute(
            "SELECT * FROM plants ORDER BY date ASC"
        ).fetchall()

    def delete(self, i):
        self.conn.execute("DELETE FROM plants WHERE id=?", (i,))
        self.conn.commit()

    def stats(self):
        return self.conn.execute(
            "SELECT AVG(height), MAX(height), MIN(height) FROM plants"
        ).fetchone()


# =========================
# MODERN LANGUAGE SCREEN
# =========================
class LanguageScreen:

    def __init__(self, root, callback):

        self.root = root
        self.callback = callback

        self.frame = tk.Frame(root, bg="#0f172a")
        self.frame.pack(fill="both", expand=True)

        top = tk.Frame(self.frame, bg="#1e293b", height=170)
        top.pack(fill="x")

        card = tk.Frame(
            self.frame,
            bg="#111827",
            padx=40,
            pady=35
        )

        card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            card,
            text="🌱 Plant Tracker PRO",
            font=("Segoe UI", 24, "bold"),
            fg="white",
            bg="#111827"
        ).pack(pady=(0, 8))

        tk.Label(
            card,
            text="Choose your language",
            font=("Segoe UI", 11),
            fg="#94a3b8",
            bg="#111827"
        ).pack(pady=(0, 25))

        lang_frame = tk.Frame(card, bg="#111827")
        lang_frame.pack()

        languages = [

            ("🇭🇷 Hrvatski", "hr", "#3b82f6"),
            ("🇬🇧 English", "en", "#2563eb"),
            ("🇸🇪 Svenska", "se", "#06b6d4"),

            ("🇮🇹 Italiano", "it", "#60a5fa"),
            ("🇫🇷 Français", "fr", "#38bdf8"),
            ("🇩🇪 Deutsch", "de", "#8b5cf6"),

            ("🇪🇸 Español", "es", "#f97316"),
            ("🇵🇹 Português", "pt", "#22c55e"),
            ("🇷🇸 Srpski", "rs", "#ef4444"),

            ("🇸🇮 Slovenščina", "si", "#14b8a6"),
            ("🇨🇿 Čeština", "cz", "#e11d48"),
            ("🇵🇱 Polski", "pl", "#ec4899"),
        ]

        row = 0
        col = 0

        for text, code, color in languages:

            btn = tk.Frame(
                lang_frame,
                bg=color,
                width=180,
                height=70,
                cursor="hand2"
            )

            btn.grid(row=row, column=col, padx=10, pady=10)
            btn.pack_propagate(False)

            label = tk.Label(
                btn,
                text=text,
                bg=color,
                fg="white",
                font=("Segoe UI", 11, "bold")
            )

            label.pack(expand=True)

            btn.bind("<Button-1>", lambda e, c=code: self.select(c))
            label.bind("<Button-1>", lambda e, c=code: self.select(c))

            def enter(e, b=btn):
                b.config(bg="white")
                for w in b.winfo_children():
                    w.config(bg="white", fg="#111827")

            def leave(e, b=btn, c=color):
                b.config(bg=c)
                for w in b.winfo_children():
                    w.config(bg=c, fg="white")

            btn.bind("<Enter>", enter)
            btn.bind("<Leave>", leave)

            label.bind("<Enter>", enter)
            label.bind("<Leave>", leave)

            col += 1

            if col > 2:
                col = 0
                row += 1

        tk.Label(
            card,
            text="Modern multilingual desktop application",
            font=("Segoe UI", 9),
            fg="#64748b",
            bg="#111827"
        ).pack(pady=(20, 0))

    def select(self, code):
        set_lang(code)
        self.frame.destroy()
        self.callback()


# =========================
# APP
# =========================
class App:

    def __init__(self, root):

        self.root = root
        self.db = Database()

        self.root.title("Plant Tracker PRO")
        self.root.geometry("1200x700")
        self.root.configure(bg=Colors.BG)

        LanguageScreen(self.root, self.start)

    # =========================
    def start(self):

        self.build_ui()
        self.show_table()

    # =========================
    def build_ui(self):

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="white",
            foreground="black",
            rowheight=30,
            fieldbackground="white",
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            background="#2563eb",
            foreground="white",
            font=("Segoe UI", 10, "bold")
        )

        container = tk.Frame(self.root, bg=Colors.BG)
        container.pack(fill="both", expand=True)

        # SIDEBAR
        self.sidebar = tk.Frame(
            container,
            bg=Colors.SIDEBAR,
            width=240
        )

        self.sidebar.pack(side="left", fill="y")

        # LOGO
        tk.Label(
            self.sidebar,
            text="🌱 Plant Tracker",
            bg=Colors.SIDEBAR,
            fg="white",
            font=("Segoe UI", 18, "bold")
        ).pack(pady=30)

        # MAIN
        self.main = tk.Frame(container, bg=Colors.BG)
        self.main.pack(side="right", fill="both", expand=True)

        # BUTTONS
        def btn(text, cmd, color):

            b = tk.Button(
                self.sidebar,
                text=text,
                command=cmd,
                bg=color,
                fg="white",
                bd=0,
                pady=14,
                font=("Segoe UI", 10, "bold"),
                cursor="hand2"
            )

            b.pack(fill="x", padx=18, pady=6)

            b.bind("<Enter>", lambda e: b.config(bg="white", fg=color))
            b.bind("<Leave>", lambda e: b.config(bg=color, fg="white"))

        btn("📋 " + LANG["table"], self.show_table, Colors.BLUE)
        btn("➕ " + LANG["add"], self.show_add, Colors.GREEN)
        btn("📊 " + LANG["dashboard"], self.show_dashboard, Colors.PURPLE)
        btn("📈 " + LANG["graph"], self.show_graph, Colors.ORANGE)
        btn("💾 " + LANG["export"], self.export_csv, "#64748b")

        # STATUS BAR
        self.status = tk.Label(
            self.root,
            text=LANG["ready"],
            bg=Colors.BLUE,
            fg="white",
            anchor="w",
            padx=10
        )

        self.status.pack(fill="x")

        self.current = None

    # =========================
    def clear(self):

        if self.current:
            self.current.destroy()

    # =========================
    def show_table(self):

        self.clear()

        frame = tk.Frame(self.main, bg=Colors.BG)
        frame.pack(fill="both", expand=True, padx=25, pady=25)

        self.current = frame

        card = tk.Frame(
            frame,
            bg="white",
            padx=15,
            pady=15
        )

        card.pack(fill="both", expand=True)

        tk.Label(
            card,
            text="📋 Plant Records",
            bg="white",
            font=("Segoe UI", 18, "bold")
        ).pack(anchor="w", pady=(0, 10))

        self.tree = ttk.Treeview(
            card,
            columns=("ID", "Date", "Temp", "Humidity", "Height"),
            show="headings"
        )

        self.tree.pack(fill="both", expand=True)

        columns = [
            ("ID", 60),
            ("Date", 160),
            ("Temp", 120),
            ("Humidity", 120),
            ("Height", 120)
        ]

        for c, w in columns:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=w)

        tk.Button(
            card,
            text="🗑 " + LANG["delete"],
            bg=Colors.RED,
            fg="white",
            bd=0,
            pady=10,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            command=self.delete
        ).pack(pady=15)

        self.load()

    # =========================
    def load(self):

        for i in self.tree.get_children():
            self.tree.delete(i)

        data = self.db.fetch()

        for r in data:
            self.tree.insert("", "end", values=r)

        self.status.config(
            text=f"{LANG['records']}: {len(data)}"
        )

    # =========================
    def show_add(self):

        self.clear()

        frame = tk.Frame(self.main, bg=Colors.BG)
        frame.pack(fill="both", expand=True)

        self.current = frame

        card = tk.Frame(
            frame,
            bg="white",
            padx=35,
            pady=35
        )

        card.place(relx=0.5, rely=0.45, anchor="center")

        tk.Label(
            card,
            text="➕ Add Plant Data",
            bg="white",
            font=("Segoe UI", 20, "bold")
        ).grid(row=0, columnspan=2, pady=(0, 25))

        labels = [
            "Date",
            "Temperature",
            "Humidity",
            "Height"
        ]

        entries = []

        for i, l in enumerate(labels):

            tk.Label(
                card,
                text=l,
                bg="white",
                font=("Segoe UI", 11)
            ).grid(row=i + 1, column=0, sticky="w", pady=10)

            e = tk.Entry(
                card,
                font=("Segoe UI", 11),
                width=25
            )

            e.grid(row=i + 1, column=1, pady=10, padx=15)

            entries.append(e)

        entries[0].insert(
            0,
            datetime.now().strftime("%Y-%m-%d")
        )

        def save():

            try:

                self.db.insert(
                    entries[0].get(),
                    float(entries[1].get()),
                    float(entries[2].get()),
                    float(entries[3].get())
                )

                self.show_table()

            except:
                messagebox.showerror(
                    "Error",
                    "Invalid input"
                )

        tk.Button(
            card,
            text="💾 " + LANG["save"],
            bg=Colors.GREEN,
            fg="white",
            bd=0,
            pady=12,
            padx=20,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            command=save
        ).grid(row=6, columnspan=2, pady=20)

    # =========================
    def show_dashboard(self):

        self.clear()

        frame = tk.Frame(self.main, bg=Colors.BG)
        frame.pack(fill="both", expand=True)

        self.current = frame

        tk.Label(
            frame,
            text="📊 Dashboard",
            bg=Colors.BG,
            font=("Segoe UI", 24, "bold")
        ).pack(pady=30)

        avg, maxv, minv = self.db.stats()

        stats = [
            ("Average Height", avg, Colors.BLUE),
            ("Maximum Height", maxv, Colors.ORANGE),
            ("Minimum Height", minv, Colors.RED)
        ]

        cards = tk.Frame(frame, bg=Colors.BG)
        cards.pack()

        for t, v, c in stats:

            f = tk.Frame(
                cards,
                bg=c,
                padx=35,
                pady=35
            )

            f.pack(side="left", padx=15)

            tk.Label(
                f,
                text=t,
                bg=c,
                fg="white",
                font=("Segoe UI", 12)
            ).pack()

            value = "0"

            if v is not None:
                value = f"{v:.2f}"

            tk.Label(
                f,
                text=value,
                bg=c,
                fg="white",
                font=("Segoe UI", 24, "bold")
            ).pack(pady=10)

    # =========================
    def show_graph(self):

        if not MATPLOTLIB:
            messagebox.showerror(
                "Error",
                "matplotlib not installed"
            )
            return

        data = self.db.fetch()

        if not data:
            return

        d = [i[1] for i in data]
        t = [i[2] for i in data]
        h = [i[3] for i in data]
        ht = [i[4] for i in data]

        plt.figure(figsize=(10, 5))

        plt.plot(
            d,
            ht,
            label="Height",
            color=Colors.BLUE,
            linewidth=3
        )

        plt.plot(
            d,
            t,
            label="Temperature",
            color=Colors.ORANGE,
            linestyle="--"
        )

        plt.plot(
            d,
            h,
            label="Humidity",
            color=Colors.GREEN,
            linestyle=":"
        )

        plt.title("Plant Analytics")
        plt.xticks(rotation=45)

        plt.legend()
        plt.grid(alpha=0.3)

        plt.tight_layout()
        plt.show()

    # =========================
    def delete(self):

        for s in self.tree.selection():

            self.db.delete(
                self.tree.item(s)["values"][0]
            )

        self.load()

    # =========================
    def export_csv(self):

        file = filedialog.asksaveasfilename(
            defaultextension=".csv"
        )

        if file:

            with open(file, "w", newline="") as f:

                csv.writer(f).writerows(
                    self.db.fetch()
                )

            self.status.config(
                text="CSV exported successfully"
            )


# =========================
# START APP
# =========================
root = tk.Tk()

App(root)

root.mainloop()