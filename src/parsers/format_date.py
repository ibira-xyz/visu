"""Parser for formatting dates into human readable strings."""
import datetime

dict_mes = {
    1: "janeiro",
    2: "fevereiro",
    3: "março",
    4: "abril",
    5: "maio",
    6: "junho",
    7: "julho",
    8: "agosto",
    9: "setembro",
    10: "outubro",
    11: "novembro",
    12: "dezembro"
}

def process_date(date: datetime.date):
    """Converts YYYY-MM-DD date to human readable date"""
    if isinstance(date, str):
        date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
    return f'{date.day} de {dict_mes[date.month]} de {date.year}'
