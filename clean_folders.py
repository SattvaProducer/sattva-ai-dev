import os

def remove_empty_dirs(path="."):
    for root, dirs, files in os.walk(path, topdown=False):
        for d in dirs:
            dir_path = os.path.join(root, d)

            # Если в папке только .gitkeep — удаляем его
            gitkeep = os.path.join(dir_path, ".gitkeep")
            if os.path.isfile(gitkeep) and len(os.listdir(dir_path)) == 1:
                os.remove(gitkeep)

            # Удаляем папку, если она пустая
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
                print(f"🗑 Удалена пустая папка: {dir_path}")

if __name__ == "__main__":
    remove_empty_dirs()
    print("✨ Очистка завершена")
