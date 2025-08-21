from datetime import datetime

def reduce_to_digit(n: int) -> int:
    """Свести число к одной цифре (1–9)."""
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n

def parse_ddmmyyyy(s: str):
    """Проверить формат ДДММГГГГ и валидность даты, вернуть (day, month, year)."""
    if len(s) != 8 or not s.isdigit():
        raise ValueError("Ожидаю 8 цифр: ДДММГГГГ, например 05112004")
    day = int(s[:2]); month = int(s[2:4]); year = int(s[4:])
    datetime(year, month, day)  # бросит исключение, если дата невозможна
    return day, month, year

def calculate(date_str: str):
    """Вернуть числа Джива, Дхарма, Подход, Метод, Карма."""
    day, month, year = parse_ddmmyyyy(date_str)

    jiva   = reduce_to_digit(day)
    dharma = reduce_to_digit(day + month)
    podhcha = reduce_to_digit(month)
    metod  = reduce_to_digit(sum(int(d) for d in str(year)))
    karma  = reduce_to_digit(jiva + dharma + podhcha + metod)

    return {
        "Джива": jiva,
        "Дхарма": dharma,
        "Подход": podhcha,
        "Метод": metod,
        "Карма": karma,
    }
