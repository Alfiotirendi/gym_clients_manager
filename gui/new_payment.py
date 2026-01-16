import tkinter as tk
from tkinter import ttk, messagebox
from services import payment_service, receipt_service
from datetime import date

class NewPaymentWindow(tk.Toplevel):
    def __init__(self, parent, member_id):
        super().__init__(parent)
        self.member = member_id
        self.title("Nuovo pagamento")
        self.geometry("300x300")

        ttk.Label(self, text="Data inizio (YYYY-MM-DD)").pack()
        self.start_entry = ttk.Entry(self)
        self.start_entry.pack()

        ttk.Label(self, text="Data fine (YYYY-MM-DD)").pack()
        self.end_entry = ttk.Entry(self)
        self.end_entry.pack()

        ttk.Label(self, text="Importo (€)").pack()
        self.amount_entry = ttk.Entry(self)
        self.amount_entry.pack()

        ttk.Label(self, text="Metodo pagamento").pack()
        self.method_entry = ttk.Entry(self)
        self.method_entry.pack()

        ttk.Button(self, text="Salva e genera ricevuta",
                   command=self.save_payment).pack(pady=10)

    def save_payment(self):

        if not self.amount_entry or not self.start_entry or not self.end_entry :
            messagebox.showerror("Errore", "Campi obbligatori vuoti")
            return

        if self.start_entry and self.end_entry:
            try:
                date.fromisoformat(self.start_entry)
                date.fromisoformat(self.end_entry)

            except ValueError:
                messagebox.showerror("Errore", "Data non valida (usa YYYY-MM-DD)")
                return           


        try:
            payment_id = payment_service.add_payment(
                self.member,
                float(self.amount_entry.get()),
                self.method_entry.get()
            )

            receipt_service.generate_receipt(
                member_id=self.member,
                start=self.start_entry.get(),
                end=self.end_entry.get(),
            )

            messagebox.showinfo("OK", "Pagamento salvato e ricevuta creata")
            self.destroy()

        except Exception as e:
            messagebox.showerror("Errore", str(e))