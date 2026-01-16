from db.database import get_connection
from datetime import date,timedelta
from functions import addmonth

def add_subscription(member_id, tipo, data_inizio, data_fine, prezzo):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO subscriptions_new
        (member_id, tipo, data_inizio, data_fine, prezzo)
        VALUES (?, ?, ?, ?, ?)
    """, (member_id, tipo, data_inizio, data_fine, prezzo))

    conn.commit()
    conn.close()

def get_active_subscription(member_id):
    today = date.today().isoformat()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM subscriptions_new
        WHERE member_id = ?
        AND data_inizio <= ?
        AND data_fine >= ?
        ORDER BY data_fine DESC
        LIMIT 1
    """, (member_id, today, today))

    result = cursor.fetchone()
    conn.close()
    return result




def get_subscriptions_by_member(member_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT tipo, data_inizio, data_fine, prezzo
        FROM subscriptions_new
        WHERE member_id = ?
        ORDER BY data_inizio DESC
    """, (member_id,))

    results = cursor.fetchall()
    conn.close()
    return results

def get_latest_subscription(member_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
            SELECT member_id,tipo,data_fine
            FROM subscriptions_new
            WHERE member_id = ?
            ORDER BY data_fine DESC
            LIMIT 1
            
    """, (member_id,))

    results = cursor.fetchone()
    conn.close()
    return results



def add_monthly_subscription(member_id,tipo, data_inizio_str, prezzo):
    data_inizio = date.fromisoformat(data_inizio_str)
    data_fine = addmonth.add_one_month(data_inizio).isoformat()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO subscriptions_new (member_id, tipo, data_inizio, data_fine, prezzo)
        VALUES (?, ?, ?, ?, ?)
    """, (
        member_id,
        tipo,
        data_inizio_str,
        data_fine,
        prezzo
    ))

    conn.commit()
    conn.close()
