import tkinter as tk
from services import member_service
from tkinter import messagebox
from datetime import date

class ModifyMember(tk.Toplevel):
    def __init__(self, parent, member_id, on_save_callback=None):
        super().__init__(parent)
        self.member_id = member_id
        self.on_save_callback = on_save_callback  # funzione da chiamare dopo il salvataggio
        self.title("Dettaglio Iscritto")
        self.resizable(False, False)
        self.grab_set()  # modale

        self.create_widgets()
        self.load_member_info()

    def create_widgets(self):
        # Sezione info base
        self.form_frame = tk.Frame(self)
        self.form_frame.pack(padx=10, pady=10)

        tk.Label(self.form_frame, text="Nome:").grid(row=0, column=0, sticky=tk.W, pady=2)
        tk.Label(self.form_frame, text="Cognome:").grid(row=1, column=0, sticky=tk.W, pady=2)
        tk.Label(self.form_frame, text="Telefono:").grid(row=2, column=0, sticky=tk.W, pady=2)
        tk.Label(self.form_frame, text="Data di nascita (YYYY-MM-DD):").grid(row=3, column=0, sticky=tk.W, pady=2)

        self.nome_var = tk.StringVar()
        self.cognome_var = tk.StringVar()
        self.telefono_var = tk.StringVar()
        self.datanascita_var = tk.StringVar()

        tk.Entry(self.form_frame, textvariable=self.nome_var, width=25).grid(row=0, column=1, pady=2)
        tk.Entry(self.form_frame, textvariable=self.cognome_var, width=25).grid(row=1, column=1, pady=2)
        tk.Entry(self.form_frame, textvariable=self.telefono_var, width=25).grid(row=2, column=1, pady=2)
        tk.Entry(self.form_frame, textvariable=self.datanascita_var, width=25).grid(row=3, column=1, pady=2)
        #data di iscrizione 
        tk.Label(self.form_frame, text="Data di iscrizione (YYYY-MM-DD)").grid(row=4, column=0, sticky="w")
        self.iscr_var = tk.StringVar()
        tk.Entry(self.form_frame, textvariable=self.iscr_var, width=30).grid(row=4, column=1)

        #Luogo nascita
        tk.Label(self.form_frame, text="Luogo nascita").grid(row=5, column=0, sticky="w")
        self.luog_var = tk.StringVar()
        tk.Entry(self.form_frame, textvariable=self.luog_var, width=30).grid(row=5, column=1)

        #codice fiscale
        tk.Label(self.form_frame, text="Codice fiscale").grid(row=6, column=0, sticky="w")
        self.cod_var = tk.StringVar()
        tk.Entry(self.form_frame, textvariable=self.cod_var, width=30).grid(row=6, column=1)

        # Bottone salva
        tk.Button(self.form_frame, text="Salva", command=self.save_member).grid(row=7, column=0, columnspan=2, pady=10)

    def load_member_info(self):
        member = member_service.get_member_by_id(self.member_id)
        if member:
            self.nome_var.set(member["nome"])
            self.cognome_var.set(member["cognome"])
            self.telefono_var.set(member["telefono"] or "")
            datan = member["data_nascita"]
            self.datanascita_var.set(datan)
            self.iscr_var.set(member["data_iscrizione"])
            self.luog_var.set(member["luogo_nascita"])
            self.cod_var.set(member["codice_fiscale"])


    def save_member(self):
        # qui puoi aggiungere validazioni se vuoi
        nome = self.nome_var.get().strip().upper()
        cognome = self.cognome_var.get().strip().upper()
        telefono = self.telefono_var.get().strip()
        dob = self.datanascita_var.get().strip()
        iscr = self.iscr_var.get().strip()
        cod=self.cod_var.get().strip().upper()
        luogo=self.luog_var.get().strip().upper()

        if not nome or not cognome or cod or luogo or dob :
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
        if len(cod) != 16:
            messagebox.showerror("Errore", "Codice fiscale non valido")
            return 


        if dob:
            try:
                date.fromisoformat(dob)
            except ValueError:
                messagebox.showerror("Errore", "Data non valida (usa YYYY-MM-DD)")
                return
            
        # Aggiorna nel database
        member_service.update_member(self.member_id, nome, cognome, telefono, dob,iscr,luogo,cod)

        tk.messagebox.showinfo("Salvato", "Dati aggiornati correttamente!")

        # Chiudi la finestra
        self.destroy()

        # Ricarica la lista nella finestra principale
        if self.on_save_callback:
            self.on_save_callback()
