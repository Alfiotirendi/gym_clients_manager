import tkinter as tk
from tkinter import messagebox
from datetime import date
from services import subscription_service

class NewSubscription(tk.Toplevel):
    def __init__(self, parent, member_id, on_save_callback=None):
        super().__init__(parent)
        self.member_id = member_id
        self.on_save_callback = on_save_callback

        self.title("Nuovo Abbonamento")
        self.resizable(False, False)
        self.grab_set()

        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self)
        frame.pack(padx=10, pady=10)

        tk.Label(frame, text="Tipo abbonamento").grid(row=0, column=0, sticky="w")
        tk.Label(frame, text="Data inizio (YYYY-MM-DD)").grid(row=1, column=0, sticky="w")
        tk.Label(frame, text="Prezzo (€)").grid(row=2, column=0, sticky="w")

        self.tipo_var = tk.StringVar(value="Mensile")
        tk.OptionMenu(frame,self.tipo_var,"mensile","pilates","ingressi").grid(row=0,column=1,sticky="ew")
        self.data_inizio_var = tk.StringVar(value=date.today().isoformat())
        self.prezzo_var = tk.StringVar()

        
        tk.Entry(frame, textvariable=self.data_inizio_var).grid(row=1, column=1)
        tk.Entry(frame, textvariable=self.prezzo_var).grid(row=2, column=1)

        tk.Button(frame, text="Salva", command=self.save).grid(
            row=3, column=0, columnspan=2, pady=10
        )

    def save(self):
        try:
            prezzo = float(self.prezzo_var.get())
        except ValueError:
            messagebox.showerror("Errore", "Prezzo non valido")
            return

        data_inizio = self.data_inizio_var.get()
        tipo = self.tipo_var.get()

        try:
            subscription_service.add_monthly_subscription(
                self.member_id,tipo, data_inizio, prezzo,
            )
        except Exception as e:
            messagebox.showerror("Errore", str(e))
            return

        messagebox.showinfo("OK", "Abbonamento aggiunto")
        if self.on_save_callback:
            self.on_save_callback()
        self.destroy()
