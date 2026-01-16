import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from services import member_service,subscription_service,payment_service
from gui import modify_member,full_history,new_payment
from functions import validate


#, subscription_service, certificate_service, payment_service
from datetime import date



class MemberDetail(tk.Toplevel):
    def __init__(self, parent, member_id,on_save_callback=None):
        super().__init__(parent)
        self.member_id = member_id
        self.on_save_callback= on_save_callback
        self.title("Dettaglio Iscritto")
        self.resizable(False, False)
        self.grab_set()  # finestra modale

        self.create_widgets()
        self.load_member_info()
        self.create_history_section()

    def create_widgets(self):
        self.label = tk.Label(self, text="Anagrafica", font=("Arial", 10, "bold"))
        self.label.pack(pady=5)
        # Info membro
        self.info_label = tk.Label(self, text="", font=("Arial", 10))
        self.info_label.pack(pady=5)

        self.gestione_label = tk.Label(self, text="Gestisci", font=("Arial", 10, "bold"))
        self.gestione_label.pack(pady=5)
        

        # Pulsanti gestione
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Modifica Dati", command=self.modify).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Nuovo Abbonamento", command=self.add_subscription).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Nuovo Certificato", command=self.add_certificate).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Nuovo Pagamento", command=self.add_payment).pack(side=tk.LEFT, padx=5)

        # Cronologia 
        self.history_label = tk.Label(self, text="Cronologia abbonamenti e pagamenti", font=("Arial", 10, "bold"))
        self.history_label.pack(pady=10)

    def load_member_info(self):
        member = member_service.get_member_by_id(self.member_id)
        if member:
            stato= validate.state_validate(member)
            self.info_label.config(text=f"Nome:{member['nome']}\nCognome:{member['cognome']}\nTel: {member['telefono']}\nData nascita:{member['data_nascita']}\nData iscrizione:{member['data_iscrizione']}\nStato abbonamento:{stato}\nLuogo di nascita:{member['luogo_nascita']}\nCodice fiscale:{member['codice_fiscale']}")

    def modify(self):
        modify_member.ModifyMember(self,self.member_id,on_save_callback=self.refresh)

    def refresh(self):
        if self.on_save_callback:
            self.on_save_callback()
        self.destroy()

    
    def add_subscription(self):
        from gui.new_subscription import NewSubscription
        NewSubscription(self, self.member_id, on_save_callback=self.refresh)

    def add_certificate(self):
        from gui.new_certificate import NewCertificate
        NewCertificate(self, self.member_id, on_save_callback=self.refresh)

    def add_payment(self):
        new_payment.NewPaymentWindow(self, self.member_id)
    
    def create_history_section(self):
        frame = ttk.LabelFrame(self, text="Ultimi Movimenti")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

    # TREEVIEW ABBONAMENTI
        tk.Label(frame, text="Ultimi abbonamenti", font=("Arial", 10, "bold")).pack()
        self.sub_tree = ttk.Treeview(
        frame,
        columns=("tipo", "data_inizio", "data_fine", "prezzo"),
        show="headings",
        height=5
        )
        self.sub_tree.heading("tipo", text="Tipo")
        self.sub_tree.heading("data_inizio", text="Inizio")
        self.sub_tree.heading("data_fine", text="Fine")
        self.sub_tree.heading("prezzo", text="Prezzo")
    
        self.sub_tree.column("tipo", width=120, anchor="center")
        self.sub_tree.column("data_inizio", width=100, anchor="center")
        self.sub_tree.column("data_fine", width=100, anchor="center")
        self.sub_tree.column("prezzo", width=80, anchor="center")
    
        self.sub_tree.pack(fill="x", pady=5)

    # TREEVIEW PAGAMENTI
        tk.Label(frame, text="Ultimi pagamenti", font=("Arial", 10, "bold")).pack()
        self.pay_tree = ttk.Treeview(
        frame,
        columns=("data", "importo", "metodo"),
        show="headings",
        height=5
        )
        self.pay_tree.heading("data", text="Data")
        self.pay_tree.heading("importo", text="Importo (€)")
        self.pay_tree.heading("metodo", text="Metodo")

    
        self.pay_tree.column("data", width=100, anchor="center")
        self.pay_tree.column("importo", width=80, anchor="center")
        self.pay_tree.column("metodo", width=100, anchor="center")
    
        self.pay_tree.pack(fill="x", pady=5)

    # Bottone Vedi tutto
        tk.Button(self, text="Vedi tutta la cronologia", command=self.show_full_history).pack(pady=5)

        self.load_history()

    def load_history(self):
    # ABBONAMENTI
        for row in self.sub_tree.get_children():
            self.sub_tree.delete(row)
        subscriptions = subscription_service.get_subscriptions_by_member(self.member_id)
        for sub in subscriptions[:5]:  # solo prime 5
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
            for pay in payments[:5]:  # solo prime 5
                self.pay_tree.insert(
                "",
                "end",
                values=(pay["data_pagamento"], f"{pay['importo']:.2f}", pay["metodo_pagamento"] or "-")
            )
        else:
            self.pay_tree.insert(
                "",
                "end",
                values=("-", "-", "-")
            ) 
    def show_full_history(self):
        full_history.FullHistory(self, self.member_id)
