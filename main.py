import pandas as pd
import datetime
import os
import sqlite3
def insert_task(cur, con):
    cur.execute("SELECT MAX(id) FROM checklist")
    new_value_index = cur.fetchone()[0]
    if new_value_index is None:
        new_value_index = 0
    print(f"task {new_value_index + 1}")
    print("Task Name:")
    task_name = input()
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    
    cur.execute(
        "INSERT INTO checklist(task_name, date_posted, time_posted, completed) VALUES (?, ?, ?, ?)",
        (task_name, current_date, current_time, 0)
    )
    con.commit()
def modify_task(cur, con):
    cur.execute("SELECT MAX(id) FROM checklist")
    new_value_index = cur.fetchone()[0]
    data = con.execute("SELECT * FROM checklist")
    df = pd.DataFrame(data, columns=["ID", "Task Name", "Date Posted", "Time Posted", "Completion"])
    print(df)
    task = int(input("Task to Modify: "))
    if task >= 1 and task < new_value_index + 1:
        print()
        print("Enter 0 to edit Task Name")
        print("Enter 1 to edit Completion status")
        selection = -1
        selection = int(input())
        if selection == 0:
            new_task = input("Enter new task name: ")
            cur.execute(f'''UPDATE checklist
                        SET task_name = '{new_task}'
                        WHERE id = {task};''')
        elif selection == 1:
            new_task = int(input("Enter new completion status: "))
            cur.execute(f'''UPDATE checklist
                        SET completed = '{new_task}'
                        WHERE id = {task};''')
    con.commit()
def view_table(con):
    data = con.execute("SELECT * FROM checklist")
    df = pd.DataFrame(data, columns=["ID", "Task Name", "Date Posted", "Time Posted", "Completion"])
    print(df)
def main():
    if os.path.exists("check_list.db") is False:
        con = sqlite3.connect("check_list.db")
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS checklist(id integer PRIMARY KEY AUTOINCREMENT, task_name TEXT, date_posted TEXT, time_posted TEXT, completed INTEGER)")
        con.commit()
        con.close()
    con = sqlite3.connect("check_list.db")
    cur = con.cursor()
    selection = -1
    while selection != 4:
        selection = -1
        print("Choose an Option:")
        print("1. Insert Task")
        print("2. Modify Task")
        print("3. View Tasks")
        print("4. Quit")
        try:
            selection = int(input("Option Selection: "))
            match selection:
                case 1:
                    insert_task(cur, con)
                case 2:
                    modify_task(cur, con)
                case 3:
                    view_table(con)
                case 4:
                    break
                case _:
                    print("Invalid selection value")
                    print("Please enter an integer between 1 and 4")
        except Exception as exc:
            print(f"error: {exc}")
        con.commit()
    con.close()
if __name__ == "__main__":
    main()