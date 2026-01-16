import tkinter as tk
from tkinter import ttk
from gui.new_member import NewMember
import services.member_service as member_service
import services.subscription_service as subscription_service
from functions.validate import validate
import functions.filters as f
from gui.member_detail import MemberDetail
from gui.notification import get_notifications

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.state('zoomed')
        self.root.title("Gestione Palestra")

        style = ttk.Style()
        style.configure(
            "Treeview",
            font=("Arial",11)
        )
        style.configure(
            "Treeview.Heading",
            font=("Arial",12,"bold")
        )

        
        self.create_widgets()
        self.search_members()
        self.schedule_notifications()


    def create_widgets(self):
        #Titolo
        title = tk.Label(
            self.root,
            text="Gestionale Palestra",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=10)

        #Toolbar
        toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        #Spazio per il testo
        tk.Label(toolbar, text="Cerca:").pack(side=tk.LEFT, padx=5)
        self.search_var = tk.StringVar()

        search_entry = tk.Entry(
            toolbar,
            textvariable=self.search_var,
            width=25,
            font=("Arial",12)
        )
        search_entry.pack(side=tk.LEFT,padx=5)
        search_entry.bind("<Return>", lambda e: self.search_members())

        #Bottone ricerca
        search_btn = tk.Button(
            toolbar,
            text="Cerca",
            command=self.search_members
        )
        search_btn.pack(side=tk.LEFT, padx=5)

        #Ricarica
        ricarica_btn = tk.Button(
            toolbar,
            text="Ricarica lista",
            command=self.load_members_filtered
        )
        ricarica_btn.pack(side=tk.LEFT,padx=5)


        #Bottone iscritto
        add_btn = tk.Button(
            toolbar,
            text="Nuovo iscritto",
            command=self.add_member
        )
        add_btn.pack(side=tk.LEFT,padx=5)


        
        ###############Sezione abbonamenti
        tk.Label(toolbar, text="Abbonamenti:").pack(side=tk.LEFT, padx=5)
        #Bottone attivi
        attivi_btn = tk.Button(
            toolbar,
            text="Attivi",
            command=lambda :self.filter_members(5)
        )
        attivi_btn.pack(side=tk.LEFT,padx=5)
        #Bottone in scadenza abbonamenti
        inscadenzaabb_btn = tk.Button(
            toolbar,
            text="In scadenza",
            command=lambda :self.filter_members(1)
        )
        inscadenzaabb_btn.pack(side=tk.LEFT,padx=5)
        #Bottone abbonamenti scaduti
        scadutiabb_btn = tk.Button(
            toolbar,
            text="Scaduti",
            command=lambda :self.filter_members(2)
        )
        scadutiabb_btn.pack(side=tk.LEFT,padx=5)


        ###############Sezione certificati
        tk.Label(toolbar, text="Certificati:").pack(side=tk.LEFT, padx=5)
        #Bottone in scadenza certificati
        inscadenzacert_btn = tk.Button(
            toolbar,
            text="In scadenza",
            command=lambda :self.filter_members(3)
        )
        inscadenzacert_btn.pack(side=tk.LEFT,padx=5)
        #Bottone certificati scaduti
        scaduticert_btn = tk.Button(
            toolbar,
            text="Scaduti",
            command=lambda: self.filter_members(4)
        )
        scaduticert_btn.pack(side=tk.LEFT,padx=5)


        #notifiche
        self.notify_label = tk.Label(
            toolbar,
            text="0",
            width=3,
            height=1,
            bg="green",
            fg="white",
            font=("Arial", 11, "bold"),
            cursor="hand2"
        )
        self.notify_label.pack(side=tk.RIGHT,padx=10)
        self.notify_label.bind("<Button-1>", self.show_notifications)



        #Lista iscritti
        self.tree = ttk.Treeview(
            self.root,
            columns=("cognome", "nome", "telefono","data nascita","stato","tipo abb.","scadenza abb","certificato","scadenza cert"),
            show="headings"
        )

        self.tree.tag_configure("scaduto", background="#FFCCCC")  # rosso chiaro
        self.tree.bind("<Double-1>", self.on_member_double_click)

        #Nomi delle colonne
        self.tree.heading("cognome", text="Cognome")
        self.tree.heading("nome", text="Nome")
        
        self.tree.heading("telefono", text="Telefono")
        self.tree.heading("data nascita",text=("Data Nascita"))
        self.tree.heading("stato", text="Stato")
        self.tree.heading("tipo abb.", text="Tipo Abb.")
        self.tree.heading("scadenza abb", text="Scadenza Abb.")
        self.tree.heading("certificato", text="Certificato")
        self.tree.heading("scadenza cert", text="Scadenza Cert.")

        #Configurazione larghezza colonne
        self.tree.column("nome", width=150, anchor="w", stretch=False)
        self.tree.column("cognome", width=150, anchor="w", stretch=False)
        self.tree.column("telefono", width=110, anchor="center", stretch=False)
        self.tree.column("data nascita", width=120, anchor="center", stretch=False)
        self.tree.column("stato", width=140, anchor="center", stretch=False)
        self.tree.column("tipo abb.", width=140, anchor="center", stretch=False)
        self.tree.column("scadenza abb", width=120, anchor="center", stretch=False)
        self.tree.column("certificato", width=140, anchor="center", stretch=False)
        self.tree.column("scadenza cert", width=120, anchor="center", stretch=False)

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


    def load_members_filtered(self,members=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        if members is None:
            members = member_service.get_all_members_complete()

        for m in members:
            tipo,abb,cert,data_abb,data_cert = validate(m)
            tag=None
            if abb == "Scaduto" or cert == "Scaduto" or abb=="Assente" or cert=="Assente":
                tag = "scaduto"
                
            self.tree.insert(
                    "",
                    tk.END,
                    iid=m["id"],
                    values=(m["cognome"], m["nome"], m["telefono"],m["data_nascita"],abb,tipo,data_abb,cert,data_cert),
                    tags=(tag,) if tag else ()
                )

    def search_members(self):
        query= self.search_var.get().strip()
        members = member_service.search_members(query)
        self.load_members_filtered(members)
    
    def filter_members(self,case):
        all_members = member_service.get_all_members_complete()
        if case == 1:
            members = f.subscription_expiring(all_members)
        elif case==2:
            members = f.subscription_expired_or_missing(all_members)
        elif case==3:
            members = f.certificate_expiring(all_members)
        elif case==4:
            members = f.certificate_expired_missing(all_members)
        elif case==5:
            members = f.active(all_members)
        self.load_members_filtered(members)
        
    def on_member_double_click(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return
        
        member_id = selected_item[0]  

        # apri finestra dettaglio
        
        MemberDetail(self.root, member_id,self.search_members) 



    
    def new_payment(self):
        print("pagamento")
    
    def update_notifications(self):
        count, details = get_notifications()
        self.notify_label.config(text=str(count))
        self.notify_details = details  # salviamo i dettagli per mostrarli dopo


    def show_notifications(self, event=None):
        if not hasattr(self, "notify_details") or not self.notify_details:
            tk.messagebox.showinfo("Notifiche", "Nessuna notifica")
            return

        notif_text = "\n".join(self.notify_details)
        tk.messagebox.showinfo("Notifiche", notif_text)

    def add_member(self):
        NewMember(self.root,on_save_callback=self.search_members)
    
    def schedule_notifications(self):
        self.update_notifications()
        self.root.after(60*60*1000, self.schedule_notifications)  # ogni 10 minuti

    def run(self):
        self.root.mainloop()
