import tkinter as tk
from tkinter import messagebox

class Task:
    def __init__(self, description):
        self.description = description
        self.completed = False

    def __str__(self):
        status = '✓' if self.completed else '✗'
        return f"{status} {self.description}"

class ToDoApp:
    def __init__(self, root):
        self.tasks = []
        self.root = root
        self.root.title("To-Do List")

        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        self.task_listbox = tk.Listbox(self.frame, width=50, height=10)
        self.task_listbox.pack(side=tk.LEFT, padx=10)

        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL)
        self.scrollbar.config(command=self.task_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.task_listbox.config(yscrollcommand=self.scrollbar.set)

        self.entry = tk.Entry(root, width=50)
        self.entry.pack(pady=10)

        self.add_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=5)

        self.update_button = tk.Button(root, text="Update Task", command=self.update_task)
        self.update_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="Delete Task", command=self.delete_task)
        self.delete_button.pack(pady=5)

        self.save_button = tk.Button(root, text="Save Tasks", command=self.save_tasks)
        self.save_button.pack(pady=5)

        self.load_tasks()

    def add_task(self):
        task_description = self.entry.get()
        if task_description:
            task = Task(task_description)
            self.tasks.append(task)
            self.task_listbox.insert(tk.END, str(task))
            self.entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Task description cannot be empty.")

    def update_task(self):
        try:
            index = self.task_listbox.curselection()[0]
            self.tasks[index].completed = not self.tasks[index].completed
            self.task_listbox.delete(index)
            self.task_listbox.insert(index, str(self.tasks[index]))
        except IndexError:
            messagebox.showwarning("Warning", "Select a task to update.")

    def delete_task(self):
        try:
            index = self.task_listbox.curselection()[0]
            self.tasks.pop(index)
            self.task_listbox.delete(index)
        except IndexError:
            messagebox.showwarning("Warning", "Select a task to delete.")

    def save_tasks(self):
        with open('tasks.json', 'w') as file:
            json.dump([task.__dict__ for task in self.tasks], file)
        messagebox.showinfo("Info", "Tasks saved successfully.")

    def load_tasks(self):
        try:
            with open('tasks.json', 'r') as file:
                tasks_data = json.load(file)
                self.tasks = [Task(**data) for data in tasks_data]
                for task in self.tasks:
                    self.task_listbox.insert(tk.END, str(task))
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
