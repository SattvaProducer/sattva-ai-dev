import os     # Для запуска скрипта в терминале python create_folders.py
import yaml

# Загружаем структуру из project_structure.yaml
with open("project_structure.yaml", "r", encoding="utf-8") as f:
    structure = yaml.safe_load(f)

def create_folder(path, description=None):
    """
    Создаёт папку с README.md и .gitkeep (если пустая).
    """
    os.makedirs(path, exist_ok=True)

    # Если есть описание, кладём README.md
    if description:
        readme_path = os.path.join(path, "README.md")
        if not os.path.exists(readme_path):
            with open(readme_path, "w", encoding="utf-8") as f:
                f.write(f"# {os.path.basename(path)}\n\n{description}\n")

    # Если папка пуста (только что создана или только README), добавляем .gitkeep
    if len(os.listdir(path)) == 0 or os.listdir(path) == ["README.md"]:
        gitkeep_path = os.path.join(path, ".gitkeep")
        if not os.path.exists(gitkeep_path):
            with open(gitkeep_path, "w", encoding="utf-8") as f:
                f.write("# keep folder\n")

def process_structure(base_path, items):
    """
    Рекурсивно создаёт папки из YAML структуры.
    """
    for key, value in items.items():
        current_path = os.path.join(base_path, key)

        if isinstance(value, list):
            # Ветка с подпапками
            create_folder(current_path)
            for sub in value:
                if isinstance(sub, dict):
                    for sub_key, sub_desc in sub.items():
                        sub_path = os.path.join(current_path, sub_key)
                        create_folder(sub_path, sub_desc)
                else:
                    sub_path = os.path.join(current_path, sub)
                    create_folder(sub_path)
        elif isinstance(value, dict):
            # Вложенные структуры
            create_folder(current_path)
            process_structure(current_path, value)
        else:
            # Обычная папка с описанием
            create_folder(current_path, str(value))

def generate_readme_structure(items, indent=0):
    """
    Генерация README_STRUCTURE.md в виде списка.
    """
    lines = []
    for key, value in items.items():
        lines.append("  " * indent + f"- **{key}/**")
        if isinstance(value, list):
            for sub in value:
                if isinstance(sub, dict):
                    for sub_key, sub_desc in sub.items():
                        lines.append("  " * (indent + 1) + f"- {sub_key}/ — {sub_desc}")
                else:
                    lines.append("  " * (indent + 1) + f"- {sub}/")
        elif isinstance(value, dict):
            lines.extend(generate_readme_structure(value, indent + 1))
        else:
            lines.append("  " * (indent + 1) + f"- {value}")
    return lines

# Запуск
if "folders" in structure:
    process_structure(".", structure["folders"])

    readme_lines = ["# 📂 Project Structure\n"]
    readme_lines.extend(generate_readme_structure(structure["folders"]))
    with open("README_STRUCTURE.md", "w", encoding="utf-8") as f:
        f.write("\n".join(readme_lines))

    print("✅ Папки созданы, README.md и .gitkeep добавлены, README_STRUCTURE.md обновлён.")
else:
    print("❌ В project_structure.yaml нет секции 'folders'")