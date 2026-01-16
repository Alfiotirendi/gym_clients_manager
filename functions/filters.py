from datetime import date, timedelta


# ===============================
# ABBONAMENTI
# ===============================

def subscription_missing(members):
    """Iscritti senza alcun abbonamento"""
    return [m for m in members if m["data_fine"] is None]

def active(members,days=32):
    today = date.today()
    limit = today + timedelta(days=days)

    return [
        m for m in members
        if m["data_fine"]
        and today.isoformat() <= m["data_fine"] <= limit.isoformat()
    ]   

def subscription_expired(members):
    """Abbonamento scaduto"""
    today = date.today().isoformat()
    return [
        m for m in members
        if m["data_fine"] is not None
        and m["data_fine"] < today
    ]


def subscription_expired_or_missing(members):
    """Abbonamento assente o scaduto"""
    today = date.today().isoformat()
    return [
        m for m in members
        if m["data_fine"] is None
        or m["data_fine"] < today
    ]


def subscription_expiring(members, days=7):
    """Abbonamento in scadenza"""
    today = date.today()
    limit = today + timedelta(days=days)

    return [
        m for m in members
        if m["data_fine"]
        and today.isoformat() <= m["data_fine"] <= limit.isoformat()
    ]


# ===============================
# CERTIFICATI
# ===============================

def certificate_missing(members):
    """Certificato assente"""
    return [
        m for m in members
        if m["presente"] != 1
    ]


def certificate_expired_missing(members):
    """Certificato scaduto"""
    today = date.today().isoformat()
    return [
        m for m in members
        if m["presente"] == 1
        and m["data_scadenza"] < today
        or m["presente"] != 1
    ]


def certificate_expiring(members, days=30):
    """Certificato in scadenza"""
    today = date.today()
    limit = today + timedelta(days=days)

    return [
        m for m in members
        if m["presente"] == 1
        and today.isoformat() <= m["data_scadenza"] <= limit.isoformat()
    ]
