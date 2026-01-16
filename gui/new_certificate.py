import tkinter as tk
from tkinter import messagebox
from services import certificate_service
from datetime import date
from services import certificate_service

class NewCertificate(tk.Toplevel):
    def __init__(self, parent, member_id, on_save_callback=None):
        super().__init__(parent)
        self.member_id = member_id
        self.on_save_callback = on_save_callback

        self.title("Nuovo Certificato Medico")
        self.resizable(False, False)
        self.grab_set()

        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self, padx=10, pady=10)
        frame.pack()

        tk.Label(frame, text="Data scadenza (YYYY-MM-DD)").grid(row=1, column=0, sticky="w")
        self.scadenza_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.scadenza_var).grid(row=1, column=1)


        tk.Button(frame, text="Salva", command=self.save).grid(row=3, columnspan=2, pady=10)

    def save(self):
        if not self.scadenza_var.get():
            messagebox.showerror("Errore", "Inserisci la data di scadenza")
            return
        if self.scadenza_var.get():
            try:
                date.fromisoformat(self.scadenza_var.get())
            except ValueError:
                messagebox.showerror("Errore", "Data non valida (usa YYYY-MM-DD)")
                return
        presente =1
        certificate_service.add_or_update_certificate(
            self.member_id,
            presente,
            self.scadenza_var.get(),
        )

        if self.on_save_callback:
            self.on_save_callback()

        self.destroy()