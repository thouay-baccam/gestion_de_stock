from databaseconnect import DatabaseConnect

class Product:
    def __init__(self, db_connection):
        self.db = db_connection

    def add_product(self, name, description, price, quantity, id_category):
        query = """
        INSERT INTO product (name, description, price, quantity, id_category) 
        VALUES (%s, %s, %s, %s, %s)
        """
        self.db.execute_query(query, (name, description, price, quantity, id_category))

    def delete_product(self, id):
        query = "DELETE FROM product WHERE id = %s"
        self.db.execute_query(query, (id,))

    def modify_product(self, id, new_name, new_description, new_price, new_quantity, new_id_category):
        query = """
        UPDATE product 
        SET name = %s, description = %s, price = %s, quantity = %s, id_category = %s 
        WHERE id = %s
        """
        self.db.execute_query(query, (new_name, new_description, new_price, new_quantity, new_id_category, id))

    def get_all_products(self):
        query = "SELECT * FROM product"
        return self.db.fetch_all(query)
    
    def fetch_all_products(self):
        query = "SELECT * FROM product"
        self.db.cursor.execute(query)
        return self.db.cursor.fetchall()