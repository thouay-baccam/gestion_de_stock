from databaseconnect import DatabaseConnect

class Category:
    def __init__(self, db_connection):
        self.db = db_connection

    def add_category(self, name):
        query = "INSERT INTO category (name) VALUES (%s)"
        self.db.execute_query(query, (name,))

    def delete_category(self, id):
        query = "DELETE FROM category WHERE id = %s"
        self.db.execute_query(query, (id,))

    def modify_category(self, id, new_name):
        query = "UPDATE category SET name = %s WHERE id = %s"
        self.db.execute_query(query, (new_name, id))

    def get_all_categories(self):
        query = "SELECT * FROM category"
        return self.db.fetch_all(query)