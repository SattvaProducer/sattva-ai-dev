import tkinter as tk
from tkinter import messagebox
from src.core.numerology import calculate

def on_calc():
    date = entry.get().strip()
    try:
        res = calculate(date)
        msg = "\n".join(f"{k}: {v}" for k, v in res.items())
        messagebox.showinfo("Результат", msg)
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))

root = tk.Tk()
root.title("Тестовый нумерологический калькулятор")

tk.Label(root, text="Введите дату (ДДММГГГГ):").pack(padx=12, pady=(12, 6))
entry = tk.Entry(root)
entry.pack(padx=12, pady=6)
entry.focus()

tk.Button(root, text="Посчитать", command=on_calc).pack(padx=12, pady=(6, 12))

root.mainloop()
