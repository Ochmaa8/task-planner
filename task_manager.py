import sqlite3
from datetime import datetime


class Task:
    """
    Класс, представляющий задачу.

    :param text: Текст задачи.
    :type text: str
    :param date: Дата выполнения задачи (в формате ГГГГ-ММ-ДД).
    :type date: str
    :param time: Время выполнения задачи (в формате ЧЧ:ММ).
    :type time: str
    :param id: Идентификатор задачи (генерируется базой данных).
    :type id: int, optional
    """

    def __init__(self, text, date, time, id=None):
        self.text = text
        self.date = date
        self.time = time
        self.id = id


class TaskManager:
    """
    Класс для управления задачами.

    :param db_file: Путь к файлу базы данных.
    :type db_file: str
    """

    def __init__(self, db_file="tasks.db"):
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        """
        Создаёт таблицу для задач, если она не существует.
        """
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT,
                date TEXT,
                time TEXT
            )
        """)
        self.conn.commit()

    def add_task(self, task):
        """
        Добавляет задачу в базу данных.

        :param task: Задача, которую нужно добавить.
        :type task: Task
        """
        self.cursor.execute(
            "INSERT INTO tasks (text, date, time) VALUES (?, ?, ?)", (task.text, task.date, task.time))
        self.conn.commit()

    def get_tasks_by_date(self, date):
        """
        Получает список задач на заданную дату.

        :param date: Дата, для которой нужно получить задачи (в формате ГГГГ-ММ-ДД).
        :type date: str
        :return: Список задач на заданную дату.
        :rtype: list[Task]
        """
        self.cursor.execute(
            "SELECT id, text, time FROM tasks WHERE date = ?", (date,))
        tasks_data = self.cursor.fetchall()
        tasks = []
        for id, text, time in tasks_data:
            tasks.append(Task(text, date, time, id))
        return tasks


    def update_task(self, task, id):
            """
            Обновляет задачу в базе данных.

            :param task: Обновленная задача.
            :type task: Task
            :param id: Идентификатор задачи, которую нужно обновить.
            :type id: int
            """
            self.cursor.execute("UPDATE tasks SET text=?, date=?, time=? WHERE id=?",
                                (task.text, task.date, task.time, id))
            self.conn.commit()


    def delete_task(self, id):
            """
            Удаляет задачу из базы данных.

            :param id: Идентификатор задачи, которую нужно удалить.
            :type id: int
            """
            self.cursor.execute("DELETE FROM tasks WHERE id=?", (id,))
            self.conn.commit()


    def get_task_by_id(self, id):
            """
            Получает задачу по её идентификатору.

            :param id: Идентификатор задачи, которую нужно получить.
            :type id: int
            :return: Задача с заданным идентификатором, или None, если задача не найдена.
            :rtype: Task, optional
            """
            self.cursor.execute(
                "SELECT text, date, time FROM tasks WHERE id=?", (id,))
            task_data = self.cursor.fetchone()
            if task_data:
                text, date, time = task_data
                return Task(text, date, time, id=id)
            return None


    def close(self):
        """
        Закрывает соединение с базой данных.
        """
        self.conn.close()
