# main.py
from interface import Interface
from databaseconnect import DatabaseConnect

if __name__ == "__main__":
    db = DatabaseConnect('localhost', 'root', 'Teddy2212!', 'store')
    gui = Interface(db)
    gui.run()
