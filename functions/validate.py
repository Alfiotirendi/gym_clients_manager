from datetime import date

def validate(m):
    today = date.today().isoformat()
    
    tipo =m["tipo"] if m["tipo"] else "-"

    if m["data_fine"] is None:
        stato = "Assente"
    elif m["data_fine"] < today:
        stato = "Scaduto"
    else:
        stato = "Attivo"
    
    if m["presente"] !=1:
        statoCert = "Assente"
    elif m["data_scadenza"] < today:
        statoCert = "Scaduto"
    else:
        statoCert = "Attivo"

    data_abb = m["data_fine"] if m["data_fine"] else "-"
    data_cert = m["data_scadenza"] if m["data_scadenza"] else "-"
    return (tipo,stato,statoCert,data_abb,data_cert)


def state_validate(m):
    today = date.today().isoformat()
    if m["data_fine"] is None:
        stato = "Assente"
    elif m["data_fine"] < today:
        stato = "Scaduto"
    else:
        stato = "Attivo"
    return stato
