from src.core.numerology import calculate

def test_sample():
    assert calculate("05112004") == {
        "Джива": 5,
        "Дхарма": 7,
        "Подход": 2,
        "Метод": 6,
        "Карма": 2,
    }
