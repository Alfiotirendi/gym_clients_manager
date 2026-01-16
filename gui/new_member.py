import tkinter as tk
from tkinter import messagebox
from services import member_service
from datetime import date

class NewMember(tk.Toplevel):
    def __init__(self, parent, on_save_callback=None):
        super().__init__(parent)
        self.title("Nuovo iscritto")
        self.resizable(False, False)
        self.on_save_callback = on_save_callback

        self.create_widgets()
        self.grab_set()  # rende la finestra modale

    def create_widgets(self):
        frame = tk.Frame(self, padx=15, pady=15)
        frame.pack()

        # Nome
        tk.Label(frame, text="Nome").grid(row=0, column=0, sticky="w")
        self.nome_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.nome_var, width=30).grid(row=0, column=1)

        # Cognome
        tk.Label(frame, text="Cognome").grid(row=1, column=0, sticky="w")
        self.cognome_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.cognome_var, width=30).grid(row=1, column=1)

        # Telefono
        tk.Label(frame, text="Telefono").grid(row=2, column=0, sticky="w")
        self.tel_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.tel_var, width=30).grid(row=2, column=1)

        # Data di nascita
        tk.Label(frame, text="Data di nascita (YYYY-MM-DD)").grid(row=3, column=0, sticky="w")
        self.dob_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.dob_var, width=30).grid(row=3, column=1)
        #data iscrizione
        tk.Label(frame, text="Data di iscrizione (YYYY-MM-DD)").grid(row=4, column=0, sticky="w")
        self.iscr_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.iscr_var, width=30).grid(row=4, column=1)

        #Luogo nascita
        tk.Label(frame, text="Luogo nascita").grid(row=5, column=0, sticky="w")
        self.luog_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.luog_var, width=30).grid(row=5, column=1)

        #codice fiscale
        tk.Label(frame, text="Codice fiscale").grid(row=6, column=0, sticky="w")
        self.cod_var = tk.StringVar()
        tk.Entry(frame, textvariable=self.cod_var, width=30).grid(row=6, column=1)

        # Bottoni
        btn_frame = tk.Frame(frame)
        btn_frame.grid(row=7, column=0, columnspan=2, pady=10)

        tk.Button(btn_frame, text="Salva", command=self.save_member).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Annulla", command=self.destroy).pack(side=tk.LEFT)

    def save_member(self):
        nome = self.nome_var.get().strip().upper()
        cognome = self.cognome_var.get().strip().upper()
        telefono = self.tel_var.get().strip()
        iscr = self.iscr_var.get().strip()
        dob = self.dob_var.get().strip()
        cod=self.cod_var.get().strip().upper()
        luogo=self.luog_var.get().strip().upper()

        # Validazioni base
        if not nome or not cognome or not cod or not luogo or not dob :
            messagebox.showerror("Errore", "Campi obbligatori vuoti")
            return
        if telefono == "":
            telefono= "-"

        if iscr:
            try:
                date.fromisoformat(iscr)
            except ValueError:
                messagebox.showerror("Errore", "Data non valida (usa YYYY-MM-DD)")
                return           

        if dob:
            try:
                date.fromisoformat(dob)
            except ValueError:
                messagebox.showerror("Errore", "Data non valida (usa YYYY-MM-DD)")
                return

        member_service.add_member(
            nome=nome,
            cognome=cognome,
            telefono=telefono,
            data_nascita=dob,
            data_iscrizione=iscr,
            luogo_nascita=luogo,
            codice_fiscale=cod
        )

        if self.on_save_callback:
            self.on_save_callback()

        self.destroy()
    
