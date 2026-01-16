from datetime import date, timedelta
from services import member_service,subscription_service,certificate_service


def get_notifications():
    """Ritorna il numero di notifiche e i dettagli."""
    today = date.today().isoformat()
    notif_count = 0
    details = []

    # 1. Abbonamenti in scadenza o scaduti
    all_members = member_service.get_all_members_complete()
    for m in all_members:
        # Abbonamento
        sub = subscription_service.get_latest_subscription(m["id"])
        if sub:
            if sub["data_fine"] < today:
                notif_count += 1
                details.append(f"Abbonamento scaduto: {m['nome']} {m['cognome']}")
            elif (date.fromisoformat(sub["data_fine"])- timedelta(days=7)) <= date.today():
                notif_count += 1
                details.append(f"Abbonamento in scadenza: {m['nome']} {m['cognome']}")
        else:
            notif_count += 1
            details.append(f"{m['nome']} {m['cognome']} non ha abbonamento")

        # Certificato
        cert = certificate_service.get_latest_certificate(m["id"])
        if cert:
            if cert["data_scadenza"] < today:
                notif_count += 1
                details.append(f"Certificato scaduto: {m['nome']} {m['cognome']}")
            elif (date.fromisoformat(cert["data_scadenza"]) - timedelta(days=7)) <= date.today():
                notif_count += 1
                details.append(f"Certificato in scadenza: {m['nome']} {m['cognome']}")
        else:
            notif_count += 1
            details.append(f"{m['nome']} {m['cognome']} non ha certificato")

        # Anniversario iscrizione
        data_iscrizione = date.fromisoformat(m["data_iscrizione"])
        if data_iscrizione.month == date.today().month and data_iscrizione.day == date.today().day:
            notif_count += 1
            details.append(f"Anniversario iscrizione: {m['nome']} {m['cognome']}")
        data_nascita = date.fromisoformat(m["data_nascita"])
        if data_nascita.month == date.today().month and data_nascita.day == date.today().day:
            notif_count += 1
            details.append(f"Compleanno: {m['nome']} {m['cognome']}")

    return notif_count, details
