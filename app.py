"""
Система управления задачами — учебное приложение.
"""

import sqlite3
from datetime import datetime

DB_PATH = "tasks.db"

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app.log"),   # запись в файл
        logging.StreamHandler()            # вывод в консоль
    ]
)

logger = logging.getLogger(__name__)


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def add_task(title: str, description: str, priority: int = 1):
    """Добавить новую задачу."""

    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (title, description, priority, created_at) VALUES (?, ?, ?, ?)",
            (title, description, priority, datetime.now().isoformat())
        )
        conn.commit()
        task_id = cursor.lastrowid
        logger.info(f"Задача успешно добавлена: id={task_id}, title='{title}'")
        return task_id
    except sqlite3.OperationalError as e:
        raise
    finally:
        conn.close()


def list_tasks():
    """Получить все задачи."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, title, description, priority, status, created_at FROM tasks ORDER BY priority DESC"
        )
        tasks = cursor.fetchall()
        return tasks
    except sqlite3.OperationalError as e:
        raise
    finally:
        conn.close()


def complete_task(task_id: int):
    """Отметить задачу выполненной."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasks SET status = 'done', completed_at = ? WHERE id = ?",
            (datetime.now().isoformat(), task_id)
        )
        conn.commit()
        if cursor.rowcount == 0:
            logger.warning(f"Задача с id={task_id} не найдена для отметки выполнения")
        else:
            logger.info(f"Задача с id={task_id} успешно отмечена как выполненная")
    except sqlite3.OperationalError as e:
        raise
    finally:
        conn.close()

def export_report():
    """Сформировать отчёт и сохранить в файл."""
    import tabulate

    tasks = list_tasks()
    rows = []
    for t in tasks:
        rows.append([t["id"], t["title"], t["priority"], t["status"]])

    report = tabulate.tabulate(
        rows,
        headers=["ID", "Название", "Приоритет", "Статус"],
        tablefmt="grid"
    )

    with open("report.txt", "w", encoding="utf-8") as f:
        f.write(report)

    print(report)


if __name__ == "__main__":
    try:
        add_task("Изучить Python", "Пройти базовый курс по Python", priority=3)
        add_task("Настроить окружение", "Установить зависимости и запустить проект", priority=5)
        add_task("Написать отчёт", "Подготовить отчёт по практической работе", priority=2)

        complete_task(1)

        print("\n--- Список задач ---")
        tasks = list_tasks()
        for t in tasks:
            print(f"[{t['id']}] {t['title']} | приоритет: {t['priority']} | статус: {t['status']}")

        print("\n--- Отчёт ---")
        export_report()
        logger.info("Приложение успешно завершило работу")

    except Exception as e:
        logger.critical(f"Критическая ошибка в работе приложения: {e}", exc_info=True)
        print(f"Ошибка: {e}")
