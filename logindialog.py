import tkinter as tk
from tkinter import simpledialog, messagebox
import mysql.connector

class LoginDialog(simpledialog.Dialog):
    def body(self, master):
        tk.Label(master, text="DB Host:").grid(row=0)
        tk.Label(master, text="DB User:").grid(row=1)
        tk.Label(master, text="DB Password:").grid(row=2)
        tk.Label(master, text="DB Name:").grid(row=3)

        self.db_host = tk.Entry(master)
        self.db_user = tk.Entry(master)
        self.db_password = tk.Entry(master, show ="*")
        self.database = tk.Entry(master)

        self.db_host.grid(row=0, column=1)
        self.db_user.grid(row=1, column=1)
        self.db_password.grid(row=2, column=1)
        self.database.grid(row=3, column=1)

        return self.db_host

    def apply(self):
        self.result = (
            self.db_host.get(),
            self.db_user.get(),
            self.db_password.get(),
            self.database.get(),
        )

def show_login_dialog():
    root = tk.Tk()
    root.withdraw()
    login = LoginDialog(root)
    if login.result:
        db_host, db_user, db_password, database = login.result
        try:
            db_connection = mysql.connector.connect(
                host=db_host,
                user=db_user,
                password=db_password,
                database=database
            )
            db_connection.close()
            root.destroy()
            return True, db_host, db_user, db_password, database
        except mysql.connector.Error as e:
            messagebox.showerror("Database Connection Failed", str(e))
            root.destroy()
            return False, None, None, None, None
    else:
        root.destroy()
        return False, None, None, None, None
