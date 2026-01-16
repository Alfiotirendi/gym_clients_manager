import tkinter as tk
from tkinter import ttk
from services import subscription_service, payment_service

class FullHistory(tk.Toplevel):
    def __init__(self, parent, member_id):
        super().__init__(parent)
        self.member_id = member_id
        self.title("Cronologia Completa")
        self.geometry("700x400")
        self.grab_set()  # modale

        # Notebook per separare Abbonamenti e Pagamenti
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Abbonamenti
        self.sub_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.sub_frame, text="Abbonamenti")

        self.sub_tree = ttk.Treeview(
            self.sub_frame,
            columns=("tipo","data_inizio","data_fine","prezzo"),
            show="headings"
        )
        for col, text in zip(
            ("tipo","data_inizio","data_fine","prezzo"),
            ("Tipo","Inizio","Fine","Prezzo (€)")
        ):
            self.sub_tree.heading(col, text=text)
            self.sub_tree.column(col, anchor="center", width=100, stretch=False)
        self.sub_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Pagamenti
        self.pay_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.pay_frame, text="Pagamenti")

        self.pay_tree = ttk.Treeview(
            self.pay_frame,
            columns=("data_pagamento","importo","metodo"),
            show="headings"
        )
        for col, text in zip(
            ("data_pagamento","importo","metodo"),
            ("Data","Importo (€)","Metodo")
        ):
            self.pay_tree.heading(col, text=text)
            self.pay_tree.column(col, anchor="center", width=120, stretch=False)
        self.pay_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.load_history()

    def load_history(self):
    # ABBONAMENTI
        for row in self.sub_tree.get_children():
            self.sub_tree.delete(row)
        subscriptions = subscription_service.get_subscriptions_by_member(self.member_id)
        for sub in subscriptions:  
            self.sub_tree.insert(
            "",
            "end",
            values=(sub["tipo"], sub["data_inizio"], sub["data_fine"], f"{sub['prezzo']:.2f}")
        )

        # PAGAMENTI
        for row in self.pay_tree.get_children():
            self.pay_tree.delete(row)
        payments = payment_service.get_payments_by_member(self.member_id)
        if payments:
            for pay in payments:  # solo prime 5
                self.pay_tree.insert(
                "",
                "end",
                values=(pay["data_pagamento"], f"{pay['importo']:.2f}", pay["metodo_pagamento"] or "-")
            )
        else:
            self.pay_tree.insert(
                "",
                "end",
                values=("-", "-", "-", "-")
            ) 
