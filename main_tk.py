import datetime
import os
import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
class CheckListApp:
    def __init__(self, root : Tk):
        self.root = root
        self.root.title("Checklist App")
        if os.path.exists("check_list.db") is False:
            self.conn = sqlite3.connect("check_list.db")
            self.cursor = self.conn.cursor()
            self.cursor.execute("CREATE TABLE IF NOT EXISTS checklist(id integer PRIMARY KEY AUTOINCREMENT, task_name TEXT, date_posted TEXT, time_posted TEXT, completed INTEGER)")
            self.conn.commit()
            self.conn.close()
        self.conn = sqlite3.connect("check_list.db")
        self.cursor = self.conn.cursor()
        self.task_item = StringVar()
        self.entry = Entry(root, textvariable=self.task_item, width=40)
        self.entry.pack(pady=5)
        self.add_btn = Button(root, text="Add Task", command=self.add_task)
        self.add_btn.pack(pady=5)
        self.task_frame = Frame(root)
        self.task_frame.pack()
        self.refresh()
    def add_task(self):
        task = self.task_item.get().strip()
        if task:
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            self.cursor.execute(
                "INSERT INTO checklist(task_name, date_posted, time_posted, completed) VALUES (?, ?, ?, ?)",
                (task, current_date, current_time, 0)
            )
            self.conn.commit()
            self.task_item.set("")
            self.refresh()
        else:
            messagebox.showwarning("Input Error", "Task cannot be empty.")
    def refresh(self):
        for widget in self.task_frame.winfo_children():
            widget.destroy()
        self.cursor.execute("SELECT * FROM checklist")
        for task_id, task, date_posted, time_posted, done in self.cursor.fetchall():
            task_frame = Frame(self.task_frame)
            task_frame.pack(fill="x", pady=2)

            var = IntVar(value=done)
            cb = Checkbutton(task_frame, text=f"{task} (Date: {date_posted}, Time: {time_posted})", variable=var,
                                command=lambda id=task_id, v=var: self.toggle_task(id, v))
            cb.pack(side="left", anchor="w")
            if done:
                cb.select()
            del_btn = Button(task_frame, text="Delete",
                                command=lambda id=task_id: self.delete_task(id))
            del_btn.pack(side="right")
    def toggle_task(self, task_id, var):
        self.cursor.execute("UPDATE checklist SET completed = ? WHERE id = ?", (var.get(), task_id))
        self.conn.commit()
    def delete_task(self, task_id):
        self.cursor.execute("DELETE FROM checklist WHERE id = ?", (task_id,))
        self.conn.commit()
        self.refresh()
    def __del__(self):
        self.conn.close()
def main():
    if os.path.exists("check_list.db") is False:
        con = sqlite3.connect("check_list.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS checklist(id integer PRIMARY KEY AUTOINCREMENT, task_name TEXT, date_posted TEXT, time_posted TEXT, completed INTEGER)")
        con.commit()
        con.close()
    con = sqlite3.connect("check_list.db")
    cur = con.cursor()
    root = Tk()
    app = CheckListApp(root)
    root.mainloop()
if __name__ == "__main__":
    main()