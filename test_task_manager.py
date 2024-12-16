import unittest
from task_manager import TaskManager, Task
import os
from datetime import datetime


class TestTaskManager(unittest.TestCase):

    def setUp(self):
        self.db_path = "test_tasks.db"
        self.task_manager = TaskManager(db_file=self.db_path)
        self.test_date = datetime.now().strftime("%Y-%m-%d")

    def tearDown(self):
        self.task_manager.close()
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_add_task(self):
        task = Task("Test task 1", self.test_date, "10:00")
        self.task_manager.add_task(task)
        tasks = self.task_manager.get_tasks_by_date(self.test_date)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].text, "Test task 1")
        self.assertEqual(tasks[0].time, "10:00")

    def test_get_tasks_by_date(self):

        task1 = Task("Test task 1", self.test_date, "10:00")
        task2 = Task("Test task 2", self.test_date, "12:00")
        self.task_manager.add_task(task1)
        self.task_manager.add_task(task2)
        tasks = self.task_manager.get_tasks_by_date(self.test_date)
        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0].text, "Test task 1")
        self.assertEqual(tasks[1].text, "Test task 2")


    def test_update_task(self):
        task = Task("Test task 1", self.test_date, "10:00")
        self.task_manager.add_task(task)
        tasks = self.task_manager.get_tasks_by_date(self.test_date)
        task_id = tasks[0].id
        updated_task = Task("Updated test task", self.test_date, "11:00", id=task_id)
        self.task_manager.update_task(updated_task, task_id)
        updated_tasks = self.task_manager.get_tasks_by_date(self.test_date)
        self.assertEqual(updated_tasks[0].text, "Updated test task")
        self.assertEqual(updated_tasks[0].time, "11:00")

    def test_delete_task(self):
        task = Task("Test task 1", self.test_date, "10:00")
        self.task_manager.add_task(task)
        tasks = self.task_manager.get_tasks_by_date(self.test_date)
        task_id = tasks[0].id
        self.task_manager.delete_task(task_id)
        tasks = self.task_manager.get_tasks_by_date(self.test_date)
        self.assertEqual(len(tasks), 0)
    

    def test_get_task_by_id(self):
        task = Task("Test task 1", self.test_date, "10:00")
        self.task_manager.add_task(task)
        tasks = self.task_manager.get_tasks_by_date(self.test_date)
        task_id = tasks[0].id
        task_db = self.task_manager.get_task_by_id(task_id)
        self.assertEqual(task_db.text, "Test task 1")


if __name__ == '__main__':
    unittest.main()