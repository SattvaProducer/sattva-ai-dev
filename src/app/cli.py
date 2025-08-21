from datetime import datetime
import re

def normalize_date(s: str) -> str:
    """Попробовать распознать дату в разных форматах и вернуть ДДММГГГГ."""
    s = s.strip().lower()

    # 1) формат без разделителей: 29011988
    if s.isdigit() and len(s) == 8:
        return s

    # 2) стандартные цифровые форматы
    for fmt in ("%d.%m.%Y", "%d-%m-%Y", "%Y-%m-%d", "%d/%m/%Y"):
        try:
            dt = datetime.strptime(s, fmt)
            return dt.strftime("%d%m%Y")
        except ValueError:
            continue

    # 3) словари месяцев
    months_ru = {
        "январь": 1, "января": 1, "янв": 1,
        "февраль": 2, "февраля": 2, "фев": 2,
        "март": 3, "марта": 3, "мар": 3,
        "апрель": 4, "апреля": 4, "апр": 4,
        "май": 5, "мая": 5,
        "июнь": 6, "июня": 6, "июн": 6,
        "июль": 7, "июля": 7, "июл": 7,
        "август": 8, "августа": 8, "авг": 8,
        "сентябрь": 9, "сентября": 9, "сен": 9,
        "октябрь": 10, "октября": 10, "окт": 10,
        "ноябрь": 11, "ноября": 11, "ноя": 11,
        "декабрь": 12, "декабря": 12, "дек": 12,
    }

    months_en = {
        "january": 1, "jan": 1,
        "february": 2, "feb": 2,
        "march": 3, "mar": 3,
        "april": 4, "apr": 4,
        "may": 5,
        "june": 6, "jun": 6,
        "july": 7, "jul": 7,
        "august": 8, "aug": 8,
        "september": 9, "sep": 9,
        "october": 10, "oct": 10,
        "november": 11, "nov": 11,
        "december": 12, "dec": 12,
    }

    # 4) текстовые варианты: "29 января 1988", "29 jan 1988"
    parts = re.split(r"[ .,\-_/]+", s)
    if len(parts) == 3:
        day, month_raw, year = parts
        try:
            day = int(day)
            year = int(year)
        except ValueError:
            raise ValueError("День и год должны быть числами")

        # месяц (русский или английский)
        if month_raw in months_ru:
            month = months_ru[month_raw]
        elif month_raw in months_en:
            month = months_en[month_raw]
        else:
            raise ValueError(f"Неизвестный месяц: {month_raw}")

        # проверка даты
        dt = datetime(year, month, day)
        return dt.strftime("%d%m%Y")

    raise ValueError("Не удалось распознать дату, попробуйте другой формат.")
