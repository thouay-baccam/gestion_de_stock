import tkinter as tk
import csv
from tkinter import ttk, messagebox, filedialog
from product import Product
from category import Category

class Interface:
    def __init__(self, db_connection):
        self.db = db_connection
        self.product = Product(db_connection)
        self.category = Category(db_connection)
        self.root = tk.Tk()
        self.root.title("Stock Manager by Thouay Baccam")
        self.setup_product_treeview()
        self.setup_product_management()   
        self.setup_category_management()
        self.populate_category_combobox()

    def setup_product_treeview(self):
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(pady=10, padx=10, fill=tk.X)

        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.product_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, selectmode="extended")
        self.product_tree.pack()

        tree_scroll.config(command=self.product_tree.yview)
        
        self.product_tree['columns'] = ('ID', 'Name', 'Description', 'Price', 'Quantity', 'Category', 'Category ID')

        self.product_tree.column("#0", width=0, stretch=tk.NO)
        self.product_tree.column("ID", anchor=tk.W, width=40)
        self.product_tree.column("Name", anchor=tk.W, width=120)
        self.product_tree.column("Description", anchor=tk.W, width=240)
        self.product_tree.column("Price", anchor=tk.W, width=80)
        self.product_tree.column("Quantity", anchor=tk.W, width=80)
        self.product_tree.column("Category", anchor=tk.W, width=120)
        self.product_tree.column("Category ID", anchor=tk.W, width=80)

        self.product_tree.heading("#0", text="", anchor=tk.W)
        self.product_tree.heading("ID", text="ID", anchor=tk.W)
        self.product_tree.heading("Name", text="Name", anchor=tk.W)
        self.product_tree.heading("Description", text="Description", anchor=tk.W)
        self.product_tree.heading("Price", text="Price", anchor=tk.W)
        self.product_tree.heading("Quantity", text="Quantity", anchor=tk.W)
        self.product_tree.heading("Category", text="Category", anchor=tk.W)
        self.product_tree.heading("Category ID", text="Category ID", anchor=tk.W)
        self.setup_filter()

        self.product_tree.tag_configure('oddrow', background="white")
        self.product_tree.tag_configure('evenrow', background="lightblue")

    def setup_product_management(self):
        pm_frame = tk.Frame(self.root)
        pm_frame.pack(fill=tk.X, padx=10, pady=10)

        input_frame = tk.Frame(pm_frame) 
        input_frame.grid(row=0, column=0, sticky="ew")

        input_frame.columnconfigure(0, weight=1)
        input_frame.columnconfigure(1, weight=1)
        input_frame.columnconfigure(2, weight=1)
        input_frame.columnconfigure(3, weight=1)

        tk.Label(input_frame, text="Name:").grid(row=0, column=0)
        self.name_entry = tk.Entry(input_frame, width=20)
        self.name_entry.grid(row=1, column=0, padx=5)

        tk.Label(input_frame, text="Description:").grid(row=0, column=1)
        self.description_entry = tk.Entry(input_frame, width=20)
        self.description_entry.grid(row=1, column=1, padx=5)

        tk.Label(input_frame, text="Price:").grid(row=0, column=2)
        self.price_entry = tk.Entry(input_frame, width=20)
        self.price_entry.grid(row=1, column=2, padx=5)

        tk.Label(input_frame, text="Quantity:").grid(row=0, column=3)
        self.quantity_entry = tk.Entry(input_frame, width=20)
        self.quantity_entry.grid(row=1, column=3, padx=5)

        tk.Label(input_frame, text="Category:").grid(row=0, column=4)
        self.category_combobox = ttk.Combobox(input_frame, width=18)
        self.category_combobox.grid(row=1, column=4, padx=5)

        # Buttons Frame
        buttons_frame = tk.Frame(pm_frame)
        buttons_frame.grid(row=0, column=1, sticky="e")

        tk.Button(buttons_frame, text="Add Product", command=self.add_product).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(buttons_frame, text="Modify Product", command=self.modify_product).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(buttons_frame, text="Delete Product", command=self.delete_product).grid(row=2, column=0, padx=5, pady=5)

        pm_frame.columnconfigure(0, weight=3)
        pm_frame.columnconfigure(1, weight=1)

    def setup_category_management(self):
        cm_frame = tk.Frame(self.root)
        cm_frame.pack(fill=tk.X, padx=10, pady=10, expand=False)

        cat_input_frame = tk.Frame(cm_frame)
        cat_input_frame.grid(row=0, column=0, sticky="ew")

        cat_input_frame.columnconfigure(0, weight=1)
        cat_input_frame.columnconfigure(1, weight=1)

        tk.Label(cat_input_frame, text="Category Name:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.category_name_entry = tk.Entry(cat_input_frame, width=20)
        self.category_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        tk.Label(cat_input_frame, text="Category ID (for modify/delete):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        self.category_id_entry = tk.Entry(cat_input_frame, width=20)
        self.category_id_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

        cat_buttons_frame = tk.Frame(cm_frame)
        cat_buttons_frame.grid(row=0, column=1, sticky="e")

        tk.Button(cat_buttons_frame, text="Add Category", command=self.add_category).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(cat_buttons_frame, text="Modify Category", command=self.modify_category).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(cat_buttons_frame, text="Delete Category", command=self.delete_category).grid(row=2, column=0, padx=5, pady=5)

        cm_frame.columnconfigure(0, weight=3)
        cm_frame.columnconfigure(1, weight=1)

    def get_category_names(self):
        return [category[1] for category in self.category.get_all_categories()]
    
    def populate_product_tree(self, products=None):
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)

        if products is None:
            products = self.product.fetch_all_products()

        for product in products:
            category_name = self.get_category_name_from_id(product[5])
            self.product_tree.insert("", 'end', values=(product[0], product[1], product[2], product[3], product[4], category_name, product[5]))
        
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
    
    def get_category_name_from_id(self, category_id):
        categories = self.category.get_all_categories()
        for category in categories:
            if category[0] == category_id:
                return category[1]
        return None

    def add_product(self):
        try:
            price = float(self.price_entry.get())
            quantity = int(self.quantity_entry.get())
        except ValueError as e:
            messagebox.showerror("Input Error", "Please enter a valid number for price and quantity.")
            return
        name = self.name_entry.get()
        description = self.description_entry.get()
        category_name = self.category_combobox.get()

        id_category = self.get_category_id_from_name(category_name)

        if id_category is not None:
            self.product.add_product(name, description, price, quantity, id_category)
            self.populate_product_tree()
        else:
            messagebox.showerror("Error", "Category not found")

    def delete_product(self): 
        selected_item = self.product_tree.selection()
        if selected_item:  
            product_id = self.product_tree.item(selected_item)['values'][0]      
            self.product.delete_product(product_id)   
            self.populate_product_tree()

            if not self.product.fetch_all_products():
                self.db.cursor.execute("ALTER TABLE product AUTO_INCREMENT = 1")
                self.db.conn.commit()
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
            new_id_category = self.get_category_id_from_name(self.category_combobox.get())
            
            self.product.modify_product(product_id, new_name, new_description, new_price, new_quantity, new_id_category) 
            self.populate_product_tree()
        else:   
            pass

    def add_category(self):
        category_name = self.category_name_entry.get()
        try:
            if category_name:
                self.category.add_category(category_name)
                self.populate_category_combobox()
            else:
                messagebox.showwarning("Warning", "Category name cannot be empty.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def delete_category(self):     
        category_id = self.category_id_entry.get()
        try:
            self.category.delete_category(category_id)
            self.populate_category_combobox()

            remaining_categories = self.category.get_all_categories()
            if not remaining_categories:
                self.db.cursor.execute("ALTER TABLE category AUTO_INCREMENT = 1")
                self.db.conn.commit()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def modify_category(self):
        category_id = self.category_id_entry.get()
        new_name = self.category_name_entry.get()
        try:
            if new_name and category_id.isdigit():
                self.category.modify_category(category_id, new_name)
                self.populate_category_combobox()
            else:
                messagebox.showwarning("Warning", "Please enter a valid category name and ID.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def refresh_data(self):
        self.populate_product_tree()
        self.populate_category_combobox()

    def setup_filter(self):
        filter_frame = tk.Frame(self.root)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(filter_frame, text="Filter by Category:").grid(row=0, column=0)
        self.filter_combobox = ttk.Combobox(filter_frame, values=self.get_category_names())
        self.filter_combobox.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(filter_frame, text="Apply Filter", command=self.apply_filter).grid(row=0, column=2, padx=5, pady=5)

    def apply_filter(self):
        selected_category_name = self.filter_combobox.get()
        if selected_category_name:
            selected_category_id = self.get_category_id_from_name(selected_category_name)
            filtered_products = self.filter_products_by_category(selected_category_id)
            self.populate_product_tree(filtered_products)
        else:
            self.populate_product_tree()

    def filter_products_by_category(self, category_id):
        all_products = self.product.fetch_all_products()
        return [product for product in all_products if product[5] == category_id]
    
    def export_to_csv(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if not filepath:
            return
        with open(filepath, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Name', 'Description', 'Price', 'Quantity', 'Category ID', 'Category Name'])
            for product in self.product.fetch_all_products():
                category_name = self.get_category_name_from_id(product[5])
                writer.writerow([product[0], product[1], product[2], product[3], product[4], product[5], category_name])
        messagebox.showinfo("Export Successful", "The data has been exported to csv successfully.")

    def create_export_button(self):
        export_button_frame = tk.Frame(self.root)
        export_button_frame.pack(side=tk.BOTTOM, anchor=tk.W, padx=10, pady=1)
        export_button = tk.Button(export_button_frame, text="Export to CSV", command=self.export_to_csv)
        export_button.pack()

    def run(self):
        self.root.geometry('850x625')
        self.root.resizable(width=False, height=False)
        self.populate_product_tree()
        self.populate_category_combobox()
        self.create_export_button()
        self.root.mainloop()