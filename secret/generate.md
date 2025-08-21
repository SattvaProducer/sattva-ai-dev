# История генераций кодов sattva-coder

# 1. Проверка твоего задания и кода от ассистента

Ты дал задание:

сократить числа до единичного (если больше 9 → сложить цифры, пока не станет 1–9),
расчёты:

Число Дживы (день рождения)
Число Дхармы (день + месяц)
Число Подхода (месяц)
Число Метода (год)
Число Кармы (сумма всех предыдущих, тоже сведённая к 1–9)

Ошибки в сгенерированном коде:
Число Дживы
Он просто берёт day, но не сокращает до одного числа.
Например, 29 → должно быть 2+9=11 → 1+1=2.
Число Дхармы
Он пишет sum(int(i) for i in str(day + month)).
Это делает сокращение только один раз, а если получится снова двузначное число — дальше уже не доводит.
Число Подхода
Он просто берёт month, а не сокращает его (например, 12 → 1+2=3).
Число Метода (год)
Он суммирует цифры года, но опять только один раз.
Должно сводиться до одного числа. Например, 1988 → 1+9+8+8=26 → 2+6=8.
Число Кармы
Ошибка в коде: dharма_number и метод_number → у него даже переменные написаны с разными раскладками (латиница/кириллица), это упадёт с ошибкой.
И логика такая же: он суммирует числа, но сокращает только один раз.

 # Мы напишем функцию, которая принимает дату в формате "DDMMYYYY" и возвращает числа Дживы, Дхармы, Подхода, Метода и Кармы. 
  def numerology_calculator(date):
    # Разбиваем дату на день, месяц и год
    day = int(date[:2])
    month = int(date[2:4])
    year = int(date[4:])
    
    # Вычисляем число Дживы - это просто день рождения
    jiva_number = day
    
    # Вычисляем число Дхармы - складываем день и месяц, сведея к одному числу если нужно
    dharma_number = sum(int(i) for i in str(day + month)) if day + month >= 10 else day + month
    
    # Вычисляем число Подхода - это месяц
    podhcha_number = month
    
    # Вычисляем число Метода - это год, сведение к одному числу если нужно
    metod_number = sum(int(i) for i in str(year)) if year >= 10 else year
    
    # Вычисляем число Кармы - это сложение всех чисел, сведение к одному числу если нужно
    karma_number = sum(int(i) for i in str(jiva_number + dharma_number + podhcha_number + metod_number)) if jiva_number + dharма_number + podhcha_number + метод_number >= 10 else jiva_number + dharma_number + podhcha_number + метод_number
    
    # Возвращаем все числа
    return {'Jiva': jiva_number, 'Dharma': dharma_number, 'Podhcha': podhcha_number, 'Metod': metod_number, 'Karma': karma_number}
Теперь вы можете использовать эту функцию для любой даты. Например:


print(numerology_calculator("29011988"))
Это вернет словарь со всеми вычисленными числами нумерологии для даты "29.01.1988".
# Правильный вариант функции 
def reduce_to_single_digit(n: int) -> int:
    """Сводит число к одной цифре (1-9)."""
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n

def numerology_calculator(date: str):
    day = int(date[:2])
    month = int(date[2:4])
    year = int(date[4:])
    
    # 1. Число Дживы
    jiva_number = reduce_to_single_digit(day)
    
    # 2. Число Дхармы (день + месяц)
    dharma_number = reduce_to_single_digit(day + month)
    
    # 3. Число Подхода (месяц)
    podacha_number = reduce_to_single_digit(month)
    
    # 4. Число Метода (год)
    metod_number = reduce_to_single_digit(sum(int(i) for i in str(year)))
    
    # 5. Число Кармы (сумма всех)
    karma_number = reduce_to_single_digit(
        jiva_number + dharma_number + podhcha_number + metod_number
    )
    
    return {
        'Jiva': jiva_number,
        'Dharma': dharma_number,
        'Podacha': podacha_number,
        'Metod': metod_number,
        'Karma': karma_number
    }

print(numerology_calculator("29011988"))



# 2