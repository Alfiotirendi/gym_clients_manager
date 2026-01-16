import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "palestra.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Tabella iscritti
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS members (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        cognome TEXT NOT NULL,
        telefono TEXT,
        data_iscrizione TEXT NOT NULL,
        data_nascita TEXT NOT NULL,
        luogo_nascita TEXT NOT NULL,
        codice_fiscale TEXT NOT NULL
    )
    """)

    # Tabella certificati
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS certificates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id INTEGER NOT NULL UNIQUE,
        presente INTEGER NOT NULL CHECK(presente IN (0,1)),
        data_scadenza TEXT NOT NULL,
        FOREIGN KEY (member_id) REFERENCES members(id)
        ON DELETE CASCADE     
    )   
    """)

    # Tabella abbonamenti
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS subscriptions_new (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id INTEGER NOT NULL,
        tipo TEXT NOT NULL,
        data_inizio TEXT NOT NULL,
        data_fine TEXT NOT NULL,
        prezzo REAL,
        FOREIGN KEY (member_id) REFERENCES members(id)
        ON DELETE CASCADE
    )
    """)


    # Tabella pagamenti (per il futuro)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payments_new (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_id INTEGER NOT NULL,
        subscription_id INTEGER,
        data_pagamento TEXT NOT NULL,
        importo REAL NOT NULL,
        metodo_pagamento TEXT,
        numero_ricevuta TEXT,
        FOREIGN KEY (member_id) REFERENCES members(id),
        FOREIGN KEY (subscription_id) REFERENCES subscriptions_new(id)
        
    )
    """)

    conn.commit()
    conn.close()
