# 🧭 Dev Guide — навигация, среды, Git и CUDA

Этот файл — быстрый справочник по работе с проектом **sattva-ai-dev** на Windows (PowerShell + VS Code).

---

## 1) Навигация в терминале (PowerShell)

**Показать текущую папку**
```powershell
pwd


  # Навигация
    Навигация в терминале (PowerShell / Windows)

Посмотреть текущую папку

cd

Содержимое папки

dir

Перейти в папку

cd имя_папки

👉 пример:

cd sattva-ai-dev

Подняться на уровень выше

cd ..

# Активация виртуал сред
    Активация виртуальных сред
Python 3.10 (.venv310)
.\.venv310\Scripts\activate

Python 3.13 (.venv)
.\.venv\Scripts\activate

После активации увидишь слева в консоли приписку:

(.venv310) PS D:\Sattva AI Ved\sattva-ai-dev>

Это значит, что ты работаешь в правильной среде.

    # Работа с Git после переноса папок
3) Создание/восстановление сред

Если сред ещё нет (или вы на новом ПК), делаем так из корня проекта:

# Python 3.10 → среда для CUDA/PyTorch
py -3.10 -m venv venvs\.venv310

# Python 3.13 → общая среда
py -3.13 -m venv venvs\.venv


Обновляем pip и ставим зависимости проекта:

# Активируй нужную среду (см. следующий раздел), затем:
python -m pip install --upgrade pip
pip install -r requirements.txt


Если requirements.txt ещё не заполнен — добавляй пакеты по мере необходимости и не забывай коммитить изменения.

4) Активация/переключение сред

Активировать Python 3.10 (CUDA/PyTorch):

.\venvs\.venv310\Scripts\Activate.ps1
# проверка
python --version


Активировать Python 3.13 (общая):

.\venvs\.venv\Scripts\Activate.ps1
# проверка
python --version


Выйти из текущей среды:

deactivate


Если PowerShell ругается на запуск скриптов, разреши их только на текущую сессию:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

5) Выбор интерпретатора в VS Code

Открой VS Code в корне репозитория.

Нажми Ctrl+Shift+P → Python: Select Interpreter.

Выбери один из путей:

.\venvs\.venv310\Scripts\python.exe — для CUDA/PyTorch

.\venvs\.venv\Scripts\python.exe — для общей разработки

(Опционально) Зафиксируй это в рабочей области:

// .vscode/settings.json
{
  "python.defaultInterpreterPath": ".\\venvs\\.venv310\\Scripts\\python.exe"
}