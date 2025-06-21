import os
import shutil
import subprocess

# Название твоего приложения
app_name = 'up1'

# Путь к папке миграций
migrations_path = os.path.join(app_name, 'migrations')

# Удаляем все миграции кроме __init__.py
for file in os.listdir(migrations_path):
    if file != '__init__.py' and file.endswith('.py'):
        os.remove(os.path.join(migrations_path, file))
    elif file.endswith('.pyc'):
        os.remove(os.path.join(migrations_path, file))

print("🗑️ Миграции удалены.")

# Удалить базу данных, если SQLite
if os.path.exists('db.sqlite3'):
    os.remove('db.sqlite3')
    print("🗑️ База db.sqlite3 удалена.")

# Запускаем команды makemigrations и migrate
subprocess.run(['python', 'manage.py', 'makemigrations', app_name])
subprocess.run(['python', 'manage.py', 'migrate'])

print("✅ Новые миграции созданы и применены.")
