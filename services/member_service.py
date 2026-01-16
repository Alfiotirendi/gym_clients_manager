#file che conterrà le operazioni rigurado i membri 


from db.database import get_connection
from datetime import datetime


def get_member_by_id(member_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT *
        FROM members m
        LEFT JOIN (
            SELECT member_id,tipo, MAX(data_fine) AS data_fine
            FROM subscriptions_new
            GROUP BY member_id
        ) s ON s.member_id = m.id
                
        WHERE id LIKE ?
                   """,(member_id,))
    rows = cursor.fetchone()
    conn.close()
    return rows

def add_member(nome, cognome,data_nascita, data_iscrizione,luogo_nascita,codice_fiscale,telefono=None):
    """
    Aggiunge un nuovo iscritto al database
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO members (nome, cognome, telefono, data_iscrizione,data_nascita,luogo_nascita,codice_fiscale)
        VALUES (?, ?, ?, ?,?,?,?)
    """, (nome, cognome, telefono, data_iscrizione,data_nascita,luogo_nascita,codice_fiscale))

    conn.commit()
    conn.close()


def update_member(member_id, nome, cognome, iscrizione,luogo_nascita, codice_fiscale, telefono=None, data_nascita=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE members
        SET nome = ?, cognome = ?, telefono = ?, data_nascita = ?, data_iscrizione = ?,codice_discale = ?,luogo_nascita =?
        WHERE id = ?
    """, (nome, cognome, telefono, data_nascita, member_id,iscrizione,codice_fiscale,luogo_nascita))
    conn.commit()
    conn.close()

def remove_member(member_id):
    """
    elimina un iscritto
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM members WHERE id = ?", (member_id,))

    conn.commit()
    conn.close()


def get_all_members_complete():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            m.id,
            m.nome,
            m.cognome,
            m.telefono,
            m.data_nascita,
            m.data_iscrizione,
            
            s.tipo,
            s.data_fine AS data_fine,

            c.presente,
            c.data_scadenza

        FROM members m

        -- ultimo abbonamento (per data_fine)
        LEFT JOIN (
            SELECT member_id,tipo, MAX(data_fine) AS data_fine
            FROM subscriptions_new
            GROUP BY member_id
        ) s ON s.member_id = m.id

        -- certificato con scadenza più lontana
        LEFT JOIN (
            SELECT member_id,
                   MAX(data_scadenza) AS data_scadenza,
                   MAX(presente) AS presente
            FROM certificates
            GROUP BY member_id
        ) c ON c.member_id = m.id

        ORDER BY m.cognome, m.nome
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows

def search_members(query):
    conn = get_connection()
    cursor = conn.cursor()

    like = f"%{query}%"

    cursor.execute("""
        SELECT
            m.id,
            m.nome,
            m.cognome,
            m.telefono,
            m.data_nascita,
            m.data_iscrizione,

            s.tipo,
            s.data_fine AS data_fine,

            c.presente,
            c.data_scadenza

        FROM members m

        -- ultimo abbonamento (per data_fine)
        LEFT JOIN (
            SELECT member_id,tipo, MAX(data_fine) AS data_fine
            FROM subscriptions_new
            GROUP BY member_id
        ) s ON s.member_id = m.id

        -- certificato con scadenza più lontana
        LEFT JOIN (
            SELECT member_id,
                   MAX(data_scadenza) AS data_scadenza,
                   MAX(presente) AS presente
            FROM certificates
            GROUP BY member_id
        ) c ON c.member_id = m.id
        WHERE m.nome LIKE ?
           OR m.cognome LIKE ?
           OR m.telefono LIKE ?
        ORDER BY m.cognome, m.nome
    """, (like, like, like))

    rows = cursor.fetchall()
    conn.close()
    return rows
