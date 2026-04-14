import sqlite3

conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()

migrations = [
    "ALTER TABLE tasks ADD COLUMN priority INTEGER DEFAULT 1",
    "ALTER TABLE tasks ADD COLUMN status TEXT DEFAULT 'todo'",
    "ALTER TABLE tasks ADD COLUMN completed_at TEXT",
]

for sql in migrations:
    try:
        cursor.execute(sql)
        print(f'OK: {sql}')
    except Exception as e:
        print(f'Пропущено: {e}')

conn.commit()
conn.close()
print('Миграция завершена')
