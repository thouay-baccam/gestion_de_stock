from logindialog import show_login_dialog
from interface import Interface
from databaseconnect import DatabaseConnect

if __name__ == "__main__":
    login_success, db_host, db_user, db_password, database = show_login_dialog()

    if login_success:
        db = DatabaseConnect(db_host, db_user, db_password, database)
        gui = Interface(db)
        gui.run()
    else:
        print("Login failed or was cancelled.")
