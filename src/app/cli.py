from src.core.numerology import calculate

def main():
    print("Калькулятор нумерологии. Введите дату в формате ДДММГГГГ (q — выход)")
    while True:
        try:
            s = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nПока!"); break
        if s.lower() in {"q", "quit", "exit"}:
            print("Пока!")
            break
        try:
            res = calculate(s)
            for k, v in res.items():
                print(f"{k}: {v}")
        except Exception as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
