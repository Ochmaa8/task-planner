from task_manager import TaskManager
from gui import TaskPlannerGUI
import argparse

def main():
    parser = argparse.ArgumentParser(description="Simple Task Planner")
    parser.add_argument("--db-path", type=str, default="tasks.db", help="Path to the SQLite database file")
    args = parser.parse_args()

    task_manager = TaskManager(args.db_path)
    gui = TaskPlannerGUI(task_manager)
    gui.run()
    task_manager.close()

if __name__ == "__main__":
    main()