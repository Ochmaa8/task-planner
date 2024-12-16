import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import calendar
from datetime import date, timedelta
from task_manager import Task, TaskManager
import os

class TaskPlannerGUI:

    def __init__(self, task_manager):
        self.task_manager = task_manager
        self.window = tk.Tk()
        self.window.title("Планировщик задач")
        self.window.geometry("800x600")
        self.db_path = tk.StringVar(value="tasks.db")

        self._create_menu()
        self.current_date = date.today()
        self.calendar_frame = tk.Frame(self.window)
        self.calendar_frame.pack(pady=20)

        self.task_frame = tk.Frame(self.window)
        self.task_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        # Add scrollbar to task frame
        self.scrollbar = tk.Scrollbar(self.task_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tasks_listbox = tk.Listbox(self.task_frame, width=50, yscrollcommand=self.scrollbar.set, font=("Helvetica", 10))
        self.tasks_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.tasks_listbox.bind('<Double-1>', self.edit_selected_task)

        self.scrollbar.config(command=self.tasks_listbox.yview)

        # Create the "Add task" button only once and pack it:
        self.add_task_btn = tk.Button(self.task_frame, text="Add task", command=self._add_task_window) # Changed
        self.add_task_btn.pack(pady=10) # Now packed only once

        self.update_calendar()

    def _add_task_window(self):
        """
        Open add task window
        """
        self.add_task_window(self.tasks_listbox.date if hasattr(self.tasks_listbox, 'date') else date.today())

    def _create_menu(self):
        """
        Создаёт меню приложения.
        """
        menubar = tk.Menu(self.window)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Set DB Path", command=self.set_db_path)
        menubar.add_cascade(label="File", menu=filemenu)
        self.window.config(menu=menubar)

    def set_db_path(self):
        """
        Открывает диалог выбора пути к базе данных.
        """
        file_path = filedialog.askopenfilename(defaultextension=".db")
        if file_path:
            self.db_path.set(file_path)
            self.task_manager = TaskManager(file_path)
            self.update_calendar()
            messagebox.showinfo("Info", f"Set DB path: {file_path}")
    
    def update_calendar(self):
        """
        Обновляет отображение календаря.
        """
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()
        
        cal = calendar.monthcalendar(self.current_date.year, self.current_date.month)
        day_names = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

        # Labels для дней недели
        for i, day in enumerate(day_names):
            label = tk.Label(self.calendar_frame, text=day)
            label.grid(row=0, column=i)

        # Кнопки для дней месяца
        row_count = 1
        for week in cal:
            for col_count, day in enumerate(week):
                if day == 0:
                    label = tk.Label(self.calendar_frame, text=" ", width=3)
                else:
                    button = tk.Button(self.calendar_frame, text=str(day), width=3, command=lambda d=day: self.show_tasks(date(self.current_date.year, self.current_date.month, d)))
                    button.grid(row=row_count, column=col_count, padx=2, pady=2)
            row_count +=1

        # Кнопки для навигации по месяцам
        prev_button = tk.Button(self.calendar_frame, text="<", command=self.prev_month)
        prev_button.grid(row=row_count, column=0)

        month_label = tk.Label(self.calendar_frame, text=self.current_date.strftime("%B %Y"))
        month_label.grid(row=row_count, column=2, columnspan=3)

        next_button = tk.Button(self.calendar_frame, text=">", command=self.next_month)
        next_button.grid(row=row_count, column=6)
        
    def prev_month(self):
        """
        Переходит к предыдущему месяцу.
        """
        self.current_date = self.current_date.replace(day=1) - timedelta(days=1)
        self.update_calendar()

    def next_month(self):
        """
        Переходит к следующему месяцу.
        """
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(year=self.current_date.year+1, month=1, day=1)
        else:
            self.current_date = self.current_date.replace(day=1, month=self.current_date.month+1)
        self.update_calendar()

    def show_tasks(self, date):
        """
        Oтображает список задач на выбранную дату.

        :param date: Дата, для которой нужно отобразить задачи.
        :type date: datetime.date
        """
        self.tasks_listbox.delete(0, tk.END)  # Очистить
        self.tasks_listbox.date = date

        tasks = self.task_manager.get_tasks_by_date(date.strftime("%Y-%m-%d"))
        for task in tasks:

            text_lines = self._wrap_text(f"{task.time}: {task.text}")
            self.tasks_listbox.insert(tk.END, f"{task.id} {text_lines[0]}" )
            for line in text_lines[1:]:
                self.tasks_listbox.insert(tk.END, f" {line}" )


    def _wrap_text(self, text, max_line_length=40):
        """
        Разбивает длинный текст на несколько строк для отображения в Listbox.
        """
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            if len(current_line + " " + word) <= max_line_length:
                current_line += (" " if current_line else "") + word
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines

    def add_task_window(self, date):
        """
        Открывает окно для добавления задачи.

        :param date: Дата, к которой нужно привязать задачу.
        :type date: datetime.date
        """
        window = tk.Toplevel(self.window)
        window.title("Add task")

        task_label = tk.Label(window, text="Task text")
        task_label.pack()
        text_field = tk.Entry(window)
        text_field.pack()

        time_label = tk.Label(window, text="Task time")
        time_label.pack()
        time_field = tk.Entry(window)
        time_field.pack()

        add_task = tk.Button(window, text="Add", command=lambda: self.add_task(date, text_field.get(), time_field.get(), window))
        add_task.pack()

    def add_task(self, date, text, time, window):
        """
        Добавляет задачу в базу данных и обновляет отображение.

        :param date: Дата задачи.
        :type date: datetime.date
        :param text: Текст задачи.
        :type text: str
        :param time: Время задачи.
        :type time: str
        :param window: Окно добавления задачи.
        :type window: tkinter.Toplevel
        """
        task = Task(text, date.strftime("%Y-%m-%d"), time)
        self.task_manager.add_task(task)
        window.destroy()
        self.show_tasks(date)
    
    def edit_selected_task(self, event):
        """
        Обрабатывает двойной клик на задаче в списке задач, открывая окно редактирования.

        :param event: Событие двойного клика.
        :type event: tkinter.Event
        """
        selected_task_index = self.tasks_listbox.curselection()
        if not selected_task_index:
            return
        selected_task_text = self.tasks_listbox.get(selected_task_index)
        task_id = int(selected_task_text.split()[0])

        task_date = self.tasks_listbox.date
        self.edit_task_window(task_id, task_date)

    def edit_task_window(self, task_id, date):
        """
        Открывает окно для редактирования задачи.

        :param task_id: Идентификатор задачи, которую нужно редактировать.
        :type task_id: int
        :param date: Дата, к которой привязана задача.
        :type date: datetime.date
        """
        task = self.task_manager.get_task_by_id(task_id)
        if not task:
            messagebox.showerror("Error", "Task not found")
            return

        window = tk.Toplevel(self.window)
        window.title("Edit task")

        task_label = tk.Label(window, text="Task text")
        task_label.pack()
        text_field = tk.Entry(window)
        text_field.insert(0, task.text)
        text_field.pack()

        time_label = tk.Label(window, text="Task time")
        time_label.pack()
        time_field = tk.Entry(window)
        time_field.insert(0, task.time)
        time_field.pack()

        edit_task_btn = tk.Button(window, text="Edit", command=lambda: self.edit_task(task_id, date, text_field.get(), time_field.get(), window))
        edit_task_btn.pack()
        
        delete_task_btn = tk.Button(window, text="Delete", command=lambda: self.delete_task(task_id, date, window))
        delete_task_btn.pack()
    
    def edit_task(self, id, date, text, time, window):
        """
        Редактирует задачу в базе данных и обновляет отображение.

        :param id: Идентификатор задачи.
        :type id: int
        :param date: Дата задачи.
        :type date: datetime.date
        :param text: Текст задачи.
        :type text: str
        :param time: Время задачи.
        :type time: str
        :param window: Окно редактирования задачи.
        :type window: tkinter.Toplevel
        """
        task = Task(text, date.strftime("%Y-%m-%d"), time, id=id)
        self.task_manager.update_task(task, id)
        window.destroy()
        self.show_tasks(date)

    def delete_task(self, id, date, window):
        """
        Удаляет задачу из базы данных и обновляет отображение.

        :param id: Идентификатор задачи.
        :type id: int
        :param date: Дата, к которой была привязана задача.
        :type date: datetime.date
        :param window: Окно удаления задачи.
        :type window: tkinter.Toplevel
        """
        self.task_manager.delete_task(id)
        window.destroy()
        self.show_tasks(date)

    def run(self):
        """
        Запускает главный цикл приложения.
        """
        self.window.mainloop()