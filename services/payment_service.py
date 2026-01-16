from db.database import get_connection
from datetime import date

def get_payments_by_member(member_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            p.id,
            p.data_pagamento,
            p.importo,
            p.metodo_pagamento,
            p.numero_ricevuta,
            s.tipo AS tipo_abbonamento
        FROM payments_new p
        LEFT JOIN subscriptions_new s ON p.subscription_id = s.id
        WHERE p.member_id = ?
        ORDER BY p.data_pagamento DESC
    """, (member_id,))

    rows = cursor.fetchall()
    conn.close()
    return rows



def add_payment(
    member_id,
    importo,
    metodo_pagamento=None,
    subscription_id=None
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO payments_new (
            member_id,
            subscription_id,
            data_pagamento,
            importo,
            metodo_pagamento
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        member_id,
        subscription_id,
        date.today().isoformat(),
        importo,
        metodo_pagamento
    ))

    conn.commit()
    payment_id = cursor.lastrowid
    conn.close()

    return payment_id
