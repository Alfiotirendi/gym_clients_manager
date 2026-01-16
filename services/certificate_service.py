from db.database import get_connection
from datetime import date,timedelta

def add_or_update_certificate(member_id, presente, data_scadenza):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM certificates WHERE member_id = ?",
        (member_id,)
    )
    existing = cursor.fetchone()

    if existing:
        cursor.execute("""
            UPDATE certificates
            SET presente = ?, data_scadenza = ?
            WHERE member_id = ?
        """, (presente, data_scadenza, member_id))
    else:
        cursor.execute("""
            INSERT INTO certificates (member_id, presente, data_scadenza)
            VALUES (?, ?, ?)
        """, (member_id, presente, data_scadenza))

    conn.commit()
    conn.close()


def get_latest_certificate(member_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
            SELECT member_id, data_scadenza
            FROM certificates
            WHERE member_id = ?
            ORDER BY data_scadenza DESC
            LIMIT 1
            
    """, (member_id,))

    results = cursor.fetchone()
    conn.close()
    return results



def get_members_without_certificate():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT m.id, m.nome, m.cognome
        FROM members m
        LEFT JOIN certificates c ON m.id = c.member_id
        WHERE c.id IS NULL OR c.presente = 0
    """)

    results = cursor.fetchall()
    conn.close()
    return results