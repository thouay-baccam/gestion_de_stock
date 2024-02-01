import tkinter as tk
from tkinter import ttk, messagebox
from product import Product
from category import Category
from databaseconnect import DatabaseConnect

class Interface:
    def __init__(self, db_connection):
        self.db = db_connection
        self.product = Product(db_connection)
        self.category = Category(db_connection)
        self.root = tk.Tk()
        self.root.title("Gestion de Stock")
        self.setup_product_treeview()
        self.setup_product_management()   
        self.setup_category_management()
        self.populate_category_combobox()

        self.refresh_button = tk.Button(self.root, text="Refresh", command=self.refresh_data)
        self.refresh_button.pack()
    
    def setup_product_treeview(self):
        self.product_tree = ttk.Treeview(self.root)
        self.product_tree['columns'] = ('ID', 'Name', 'Description', 'Price', 'Quantity', 'Category', 'Category ID')

        self.product_tree.column("#0", width=0, stretch=tk.NO)
        self.product_tree.column("ID", anchor=tk.W, width=40)
        self.product_tree.column("Name", anchor=tk.CENTER, width=80)
        self.product_tree.column("Description", anchor=tk.CENTER, width=120)
        self.product_tree.column("Price", anchor=tk.CENTER, width=60)
        self.product_tree.column("Quantity", anchor=tk.CENTER, width=60)
        self.product_tree.column("Category", anchor=tk.CENTER, width=60)
        self.product_tree.column("Category ID", anchor=tk.CENTER, width=80)

        # Create Headings
        self.product_tree.heading("#0", text="", anchor=tk.W)
        self.product_tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.product_tree.heading("Name", text="Name", anchor=tk.CENTER)
        self.product_tree.heading("Description", text="Description", anchor=tk.CENTER)
        self.product_tree.heading("Price", text="Price", anchor=tk.CENTER)
        self.product_tree.heading("Quantity", text="Quantity", anchor=tk.CENTER)
        self.product_tree.heading("Category", text="Category", anchor=tk.CENTER)
        self.product_tree.heading("Category ID", text="Category ID", anchor=tk.CENTER)

        self.product_tree.pack(fill=tk.BOTH, expand=True)


    def setup_product_management(self):     
        pm_frame = tk.Frame(self.root)
        pm_frame.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(pm_frame, text="Name:").grid(row=0, column=0, sticky=tk.W)
        self.name_entry = tk.Entry(pm_frame)
        self.name_entry.grid(row=0, column=1)

        tk.Label(pm_frame, text="Description:").grid(row=1, column=0, sticky=tk.W)
        self.description_entry = tk.Entry(pm_frame)
        self.description_entry.grid(row=1, column=1)

        tk.Label(pm_frame, text="Price:").grid(row=2, column=0, sticky=tk.W)
        self.price_entry = tk.Entry(pm_frame)
        self.price_entry.grid(row=2, column=1)

        tk.Label(pm_frame, text="Quantity:").grid(row=3, column=0, sticky=tk.W)
        self.quantity_entry = tk.Entry(pm_frame)
        self.quantity_entry.grid(row=3, column=1)

        tk.Label(pm_frame, text="Category:").grid(row=4, column=0, sticky=tk.W)
        self.category_combobox = ttk.Combobox(pm_frame)
        self.category_combobox.grid(row=4, column=1)

        tk.Button(pm_frame, text="Add Product", command=self.add_product).grid(row=5, column=2, pady=5)
        tk.Button(pm_frame, text="Modify Product", command=self.modify_product).grid(row=5, column=3, pady=5)
        tk.Button(pm_frame, text="Delete Product", command=self.delete_product).grid(row=5, column=4, pady=5)


    def setup_category_management(self): 
        cm_frame = tk.Frame(self.root)
        cm_frame.pack(fill=tk.X, padx=10, pady=10)
       
        tk.Label(cm_frame, text="Category Name:").grid(row=0, column=0, sticky=tk.W)
        self.category_name_entry = tk.Entry(cm_frame)
        self.category_name_entry.grid(row=0, column=1)
   
        tk.Label(cm_frame, text="Category ID (for modify/delete):").grid(row=1, column=0, sticky=tk.W)
        self.category_id_entry = tk.Entry(cm_frame)
        self.category_id_entry.grid(row=1, column=1)

        tk.Button(cm_frame, text="Add Category", command=self.add_category).grid(row=2, column=0, pady=5)
        tk.Button(cm_frame, text="Modify Category", command=self.modify_category).grid(row=2, column=1, pady=5)
        tk.Button(cm_frame, text="Delete Category", command=self.delete_category).grid(row=2, column=2, pady=5)


    def populate_product_tree(self):
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
        
        products = self.product.fetch_all_products()
        for product in products:
            product_id, name, description, price, quantity, category_id = product

            category_name = self.get_category_name_from_id(category_id)

            self.product_tree.insert("", 'end', values=(product_id, name, description, price, quantity, category_name, category_id))
            

    def populate_category_combobox(self):
        categories = self.category.get_all_categories()
        category_names = [category[1] for category in categories]
        self.category_combobox['values'] = category_names

    def get_category_id_from_name(self, category_name):
        categories = self.category.get_all_categories()
        for category in categories:
            if category[1] == category_name:
                return category[0] 
        return None


    def add_product(self):
        name = self.name_entry.get()
        description = self.description_entry.get()
        price = self.price_entry.get()
        quantity = self.quantity_entry.get()
        category_name = self.category_combobox.get()

        id_category = self.get_category_id_from_name(category_name)

        if id_category is not None:
            self.product.add_product(name, description, price, quantity, id_category)
            self.populate_product_tree()
        else:
            messagebox.showerror("Error", "Category not found")

    def get_category_name_from_id(self, category_id):
        categories = self.category.get_all_categories()
        for category in categories:
            if category[0] == category_id:
                return category[1]  # Return the category name
        return None


    def delete_product(self): 
        selected_item = self.product_tree.selection()
        if selected_item:  
            product_id = self.product_tree.item(selected_item)['values'][0]      
            self.product.delete_product(product_id)   
            self.populate_product_tree()
        else:
            pass


    def modify_product(self):
        selected_item = self.product_tree.selection()
        if selected_item:  
            product_id = self.product_tree.item(selected_item)['values'][0]
     
            new_name = self.name_entry.get()
            new_description = self.description_entry.get()
            new_price = self.price_entry.get()
            new_quantity = self.quantity_entry.get()
            new_id_category = self.category_combobox.get()
            
            self.product.modify_product(product_id, new_name, new_description, new_price, new_quantity, new_id_category) 
            self.populate_product_tree()
        else:   
            pass


    def add_category(self):      
        category_name = self.category_name_entry.get()     
        self.category.add_category(category_name)
        

    def delete_category(self):     
        category_id = self.category_id_entry.get()
        self.category.delete_category(category_id)
        self.populate_category_combobox() 

        
    def modify_category(self):  
        category_id = self.category_id_entry.get()
        new_name = self.category_name_entry.get()
        self.category.modify_category(category_id, new_name)
        self.populate_category_combobox()

        

    def refresh_data(self):
        self.populate_product_tree()

    def run(self):
        self.root.mainloop()

    
    
