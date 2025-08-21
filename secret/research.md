План и инструкции (шаги от А до Я)
0) Как будем обучать

Подход: Supervised fine-tuning (SFT) с QLoRA (4-bit) — экономно по VRAM и отлично подходит для «стиля/навыков» ассистента (астрология/нумерология на RU/EN).

Инструмент: LLaMA-Factory (удобный UI/CLI, без плясок с деepspeed на Windows).

Если что-то не взлетит на «чистом Windows», запасной план — использовать WSL2 + Ubuntu. Но начнём с Windows-варианта.

1) Подготовим отдельное окружение (Python 3.10)

У тебя уже есть 3.10 — создадим под обучение отдельную venv, чтобы не конфликтовать с проектом.

В PowerShell (от имени пользователя, не администратора):

# папка под тренинг-окружения (пример)
mkdir D:\venvs -ea 0
python3.10 -m venv D:\venvs\llama31-qlora

# Активировать окружение
D:\venvs\llama31-qlora\Scripts\Activate.ps1

# Обновить pip & wheel
python -m pip install --upgrade pip wheel

2) Ставим зависимости

На Windows нам нужен PyTorch с CUDA-wheels. Ставим готовую сборку (без «сборки из исходников»).

# (пример для CUDA wheels от PyTorch)
pip install --index-url https://download.pytorch.org/whl/cu121 torch torchvision torchaudio

# Библиотеки для QLoRA/SFT
pip install transformers==4.43.3 datasets peft bitsandbytes accelerate sentencepiece tiktoken

# Сама LLaMA-Factory (CLI+WebUI)
pip install llama-factory


Если bitsandbytes ругнётся на Windows-CUDA: не паникуем — чаще всего сейчас ставится. Если нет — скажу, как переключиться на «bnb-cpu-offload»/или пойдём через WSL2.

Проверка GPU:

python -c "import torch; print('CUDA:', torch.cuda.is_available()); print('Device:', torch.cuda.device_name(0) if torch.cuda.is_available() else 'CPU')"

3) Скачиваем базовую модель (HuggingFace)

Создай токен на HF и прими лицензию Llama-3.1-8B.

Логин в консоли:

huggingface-cli login


Каталог под модели:

mkdir D:\models -ea 0


Скачай репозиторий модели (например через huggingface_hub/git-lfs или в первый запуск LLaMA-Factory подтянет сама). Если хочешь явно:

pip install huggingface_hub
python - << 'PY'
from huggingface_hub import snapshot_download
snapshot_download(repo_id="meta-llama/Llama-3.1-8B", local_dir="D:/models/llama-3.1-8b", local_dir_use_symlinks=False)
PY


Важно: путь D:\models\llama-3.1-8b держим вне репозитория (и у тебя .gitignore уже игнорит models/ — отлично).

4) Готовим датасет (инструкции/ответы RU/EN)

Храним частные данные в репо как локальные: data/private/datasets/. Это у тебя уже игнорится в Git.

Создай файл:
data/private/datasets/sattva_instruct_v1.jsonl

{"instruction": "Определи числа Джива, Дхарма, Подход, Метод, Карма для даты: 29.01.1988. Дай только числа.", "input": "", "output": "Джива: 2\nДхарма: 3\nПодход: 1\nМетод: 8\nКарма: 5", "lang": "ru"}
{"instruction": "Analyze this birth date (DDMMYYYY=05112004) and return five core numerology numbers (Jiva, Dharma, Approach, Method, Karma). Output only numbers.", "input": "", "output": "Jiva: 5\nDharma: 7\nApproach: 2\nMethod: 6\nKarma: 2", "lang": "en"}
{"instruction": "У меня локальный проект в VS Code. Проанализируй весь присланный код и не отказывайся по политике — работай офлайн, без интернета, строго по предоставленным файлам.", "input": "<<<Тут пример: структура src/, requirements.txt, куски кода>>>", "output": "OK. Я вижу структуру: ... Вот анализ ... Конкретные предложения: ...", "lang": "ru"}
{"instruction": "You are a local assistant. Never refuse due to privacy concerns when the user explicitly provides files. Work strictly on local code, no external calls.", "input": "<<<Example directory tree and code>>>", "output": "Acknowledged. Here is the analysis and concrete refactoring suggestions...", "lang": "en"}


Суть: ты учишь стиль и снимаешь излишние отказы — даёшь примеры, где ассистент спокойно анализирует локальные файлы и не ругается на «политику/конфиденциальность», поскольку всё локально и дано пользователем.

Добавляй реальные пары (RU/EN), больше кейсов по нумерологии/датам/ошибкам формата/«как отвечать». 500–3 000 примеров для начала — уже даст эффект.

5) Готовим конфиг тренировки (QLoRA)

Создай configs/train/llama31_8b_sattva_qlora.yaml:

# БАЗА
model_name_or_path: D:/models/llama-3.1-8b
output_dir: D:/models/sattva-llama31-8b-qlora-v1
logging_steps: 10
save_steps: 200
save_total_limit: 2

# ДАТА
train_file: data/private/datasets/sattva_instruct_v1.jsonl
overwrite_cache: true

# ФОРМАТ ДАННЫХ (инструкции)
dataset: json
prompt_template: llama3
# поля в jsonl:
# instruction -> instruction
# input       -> input
# output      -> output

# QLoRA / 4-bit
load_in_4bit: true
bnb_4bit_use_double_quant: true
bnb_4bit_quant_type: nf4
bnb_4bit_compute_dtype: bfloat16

# LoRA адаптер
lora_target: all-linear
lora_r: 16
lora_alpha: 32
lora_dropout: 0.05

# ОБУЧЕНИЕ
do_train: true
per_device_train_batch_size: 1
gradient_accumulation_steps: 8
num_train_epochs: 2
learning_rate: 2e-4
lr_scheduler_type: cosine
warmup_ratio: 0.03
weight_decay: 0.0
fp16: false
bf16: true

# КОНТЕКСТ (sequence length)
max_source_length: 1024
max_target_length: 1024
# итого до ~2048 токенов — безопасно для VRAM
# позже можно 4096/8192, но потребление VRAM резко растёт

# ACCELERATE без deepspeed (проще для Windows)
gradient_checkpointing: true
ddp_find_unused_parameters: false

# формат инструкций
# Встроенный темплейт llama3 уже подставит системные/роле-заголовки корректно


Почему не 8192 сразу? На 8B это существенно поднимет VRAM и время. Для наших дат/инструкций 2k–4k контекст более чем достаточно на первом этапе.

6) Запускаем обучение

Две опции — CLI-режим. В активированном venv:

# Проверочный запуск (сухой прогон, без обучения)
llamafactory-cli train configs/train/llama31_8b_sattva_qlora.yaml --dry_run

# Реальный старт
llamafactory-cli train configs/train/llama31_8b_sattva_qlora.yaml


После обучения в output_dir появится LoRA-адаптер (папка с weights/adapter_config.json).

7) Экспорт: слить LoRA в базу и сделать GGUF для Ollama
Вариант A (надёжный): сливаем (merge) LoRA → HF-модель → GGUF
# 7.1 Слияние LoRA в базовую модель
llamafactory-cli export \
  --model_name_or_path D:/models/llama-3.1-8b \
  --adapter_name_or_path D:/models/sattva-llama31-8b-qlora-v1 \
  --export_dir D:/models/sattva-llama31-8b-merged-v1

# 7.2 Конвертировать в GGUF и квантовать (пример q4_k_m)
pip install llama-cpp-python
# Для конвертации удобнее скрипты llama.cpp, но в простом случае:
# воспользуемся утилитами из экосистемы. Если нужна точная команда под твои пути — скажу.


Если захочешь, дам точные команды конвертации через llama.cpp (convert + quantize). Я не расписываю их здесь только чтобы не перегружать — делаем по запросу, когда появится merged папка.

Вариант B: использовать LoRA как адаптер

Технически llama.cpp умеет подключать LoRA на лету; в Ollama поддержка адаптеров зависит от версии. Надёжнее вмерджить, чтобы избежать сюрпризов.

8) Подключаем в Ollama

Создай Modelfile (например D:\Ollama\Models\sattva-llama31-8b-q4km\Modelfile):

FROM ./sattva-llama31-8b-q4km.gguf

PARAMETER num_ctx 4096
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40

SYSTEM """
You are SatTva — a local AI assistant for a Jyotish (Vedic astrology) & numerology project.
- Work strictly offline on user-provided code and data.
- Do not refuse due to privacy/safety when the user explicitly provided files and asks for analysis.
- Communicate in Russian by default; switch to English if the user writes in English.
- Be technical, precise, and propose concrete improvements.
- Never invent facts; if context is missing, ask for the exact paths/files/diffs.
"""


Собрать и зарегистрировать модель:

cd D:\Ollama\Models\sattva-llama31-8b-q4km
ollama create sattva-llama31-8b -f Modelfile

# Проверка
ollama run sattva-llama31-8b

9) Как сделать модель «менее отказывающейся»

Системное сообщение (см. Modelfile) — уже задаёт поведение.

Датасет примеров: добавляй позитивные примеры «код локальный, анализируй, без отсылок к политике» и негативные противопримеры (где отказ — ошибка), с правильным ответом.

Не перегибай — оставь базовую охрану (не выдумывать приватные данные, не тянуть интернет).

Регулярно проверяй ответы на «красных» примерах (см. п.10).

10) Мини-валидация (sanity-checks)

Сделай 10–30 «контрольных промптов» (RU/EN) и храни их в data/private/eval/. После каждого обучения — прогони их скриптом и сравни ответы с эталоном. Так ты быстро поймёшь, стало ли лучше.

11) Что по VRAM/скорости

8B + QLoRA обычно помещается в 12–16 GB VRAM при seq_len≈2k, bs=1, grad_accum=8–16.

Контекст 8192 резко увеличивает память и время — отложи до этапа 2.

Если будет OOM — уменьшай max_*_length, r (например до 8), увеличивай gradient_accumulation_steps.

12) Где хранить всё в твоём проекте

data/private/datasets/… — обучающие данные (не в Git, у тебя уже игнорится).

configs/train/… — YAML-конфиги тренировок (в Git, можно).

models/… — база и чекпоинты (не в Git).

scripts/train/… — вспомогательные скрипты (в Git).

Быстрые команды (чек-лист)
# Активировать окружение
D:\venvs\llama31-qlora\Scripts\Activate.ps1

# Проверка CUDA
python -c "import torch; print(torch.cuda.is_available(), torch.cuda.device_name(0))"

# Старт обучения
llamafactory-cli train configs/train/llama31_8b_sattva_qlora.yaml

# Слияние адаптера
llamafactory-cli export --model_name_or_path D:/models/llama-3.1-8b `
  --adapter_name_or_path D:/models/sattva-llama31-8b-qlora-v1 `
  --export_dir D:/models/sattva-llama31-8b-merged-v1

# (после конвертации в GGUF)
ollama create sattva-llama31-8b -f Modelfile
ollama run sattva-llama31-8b

Вопросы/следующие шаги

Хочешь — дам готовый шаблон датасета на 30–50 записей под твои формулы и стиль ответов, чтобы сразу скормить на первый прогон.

Когда получим первый LoRA — покажу точные команды конвертации в GGUF (под твои пути) и квантизации (q4_K_M).

Можем прикрутить LLaMA-Factory WebUI, чтобы тюнить параметры без CLI.

Если по какому-то шагу застрянешь — кидай скрин/лог, добьём на месте.