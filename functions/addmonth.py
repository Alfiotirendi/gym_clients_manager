from datetime import date
def add_one_month(start_date: date) -> date:
    year = start_date.year
    month = start_date.month + 1

    if month > 12:
        month = 1
        year += 1

    day = start_date.day

    # gestisce mesi con meno giorni
    while True:
        try:
            return date(year, month, day)
        except ValueError:
            day -= 1