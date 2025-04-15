import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import ttkbootstrap as tb

# Database connection
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Toor",
        database="CarRentalDB"
    )

# Add new customer function
def add_customer(first, last, email, phone, tree):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = "INSERT INTO Customers (first_name, last_name, email, phone) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (first.get(), last.get(), email.get(), phone.get()))
        conn.commit()
        messagebox.showinfo("Success", "Customer added successfully!")

        # Refresh the customer table after adding a new customer
        run_query("SELECT * FROM Customers", tree)

        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))


# Search customer and show rentals
def search_customer(search_field, search_value, info_label, rental_tree):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = f"SELECT * FROM Customers WHERE {search_field} LIKE %s"
        cursor.execute(query, (f"%{search_value.get()}%",))
        rows = cursor.fetchall()

        if not rows:
            messagebox.showinfo("Info", "No customer found")
            return

        customer = rows[0]
        info_label.config(text=f"Customer Info:\nID: {customer[0]}\nName: {customer[1]} {customer[2]}\nEmail: {customer[3]}\nPhone: {customer[4]}")

        customer_id = customer[0]
        rental_query = """
            SELECT Rentals.rental_id, Cars.car_type, Rentals.rental_start_date, Rentals.rental_end_date
            FROM Rentals
            JOIN Cars ON Rentals.car_id = Cars.car_id
            WHERE Rentals.customer_id = %s
        """
        cursor.execute(rental_query, (customer_id,))
        rental_rows = cursor.fetchall()

        rental_tree.delete(*rental_tree.get_children())
        rental_tree["columns"] = ["rental_id", "car_type", "start_date", "end_date"]
        rental_tree["show"] = "headings"
        for col in rental_tree["columns"]:
            rental_tree.heading(col, text=col)
        for row in rental_rows:
            rental_tree.insert("", tk.END, values=row)

        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# View all customers
def view_customers(tree):
    run_query("SELECT * FROM Customers", tree)

# Add new car
def add_car(car_type, car_color, car_price):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = "INSERT INTO Cars (car_type, car_color, car_price) VALUES (%s, %s, %s)"
        cursor.execute(query, (car_type.get(), car_color.get(), car_price.get()))
        conn.commit()
        messagebox.showinfo("Success", "Car added successfully!")
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# View all cars
def view_cars(tree):
    run_query("SELECT * FROM Cars", tree)


# Display query results
def run_query(query, tree):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        cols = [desc[0] for desc in cursor.description]

        tree.delete(*tree.get_children())
        tree["columns"] = cols
        tree["show"] = "headings"

        for col in cols:
            tree.heading(col, text=col)

        for row in rows:
            tree.insert("", tk.END, values=row)

        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# UI Setup
app = tb.Window(themename="superhero")
app.title("Car Rental Management")
app.geometry("1100x750")

notebook = ttk.Notebook(app)
notebook.pack(fill='both', expand=True)

# --------------------- Customers Tab ---------------------
# --------------------- Customers Tab ---------------------
cust_tab = ttk.Frame(notebook)
notebook.add(cust_tab, text="Customers")

mode_var = tk.StringVar(value="existing")

mode_frame = ttk.LabelFrame(cust_tab, text="Customer Type")
mode_frame.pack(fill='x', padx=10, pady=5)

def update_mode():
    if mode_var.get() == "existing":
        search_container.pack(fill='both', expand=True, padx=10, pady=5)
        add_form_frame.pack_forget()
    else:
        search_container.pack_forget()
        add_form_frame.pack(fill='x', padx=10, pady=5)
        run_query("SELECT * FROM Customers", new_customer_table)

ttk.Radiobutton(mode_frame, text="Existing", variable=mode_var, value="existing", command=update_mode).pack(side='left', padx=10)
ttk.Radiobutton(mode_frame, text="New", variable=mode_var, value="new", command=update_mode).pack(side='left', padx=10)

search_container = ttk.Frame(cust_tab)

# Left search frame
search_frame = ttk.LabelFrame(search_container, text="Search Existing Customer")
search_frame.pack(side='left', fill='y', padx=5, pady=5)

search_field = tk.StringVar()
search_menu = ttk.Combobox(
    search_frame,
    textvariable=search_field,
    values=["customer_id", "first_name", "last_name", "email", "phone"]
)

search_field.set("customer_id")
search_entry = ttk.Entry(search_frame)
search_btn = ttk.Button(search_frame, text="Search")

search_menu.pack(fill='x', padx=5, pady=2)
search_entry.pack(fill='x', padx=5, pady=2)
search_btn.pack(padx=5, pady=5)

# Right display frame
details_frame = ttk.LabelFrame(search_container, text="Customer Details and Rental History")
details_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)

# Editable fields for update
edit_fields = {}
for label in ["First Name", "Last Name", "Email", "Phone"]:
    row = ttk.Frame(details_frame)
    row.pack(fill='x', padx=5, pady=2)
    ttk.Label(row, text=label, width=10).pack(side='left')
    entry = ttk.Entry(row)
    entry.pack(fill='x', expand=True)
    edit_fields[label] = entry

# Buttons for update and delete
btn_frame = ttk.Frame(details_frame)
btn_frame.pack(pady=5)

update_btn = ttk.Button(btn_frame, text="Update Customer")
delete_btn = ttk.Button(btn_frame, text="Delete Customer")
update_btn.pack(side='left', padx=5)
delete_btn.pack(side='left', padx=5)
cust_info_label = ttk.Label(details_frame, text="Customer Info:", anchor="w", justify='left')
cust_info_label.pack(fill='x', padx=5, pady=5)



# Rental table
rental_table = ttk.Treeview(details_frame)
rental_table.pack(fill='both', expand=True, padx=5, pady=5)

# Placeholder to store current customer_id
current_customer_id = tk.IntVar()

def search_customer(search_field, search_value, info_label, rental_tree):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = f"SELECT * FROM Customers WHERE {search_field} LIKE %s"
        cursor.execute(query, (f"%{search_value.get()}%",))
        rows = cursor.fetchall()

        if not rows:
            messagebox.showinfo("Info", "No customer found")
            return

        customer = rows[0]
        current_customer_id.set(customer[0])  # Store for update/delete

        info_label.config(text=f"Customer Info:\nID: {customer[0]}\nName: {customer[1]} {customer[2]}\nEmail: {customer[3]}\nPhone: {customer[4]}")
        edit_fields["First Name"].delete(0, tk.END)
        edit_fields["First Name"].insert(0, customer[1])
        edit_fields["Last Name"].delete(0, tk.END)
        edit_fields["Last Name"].insert(0, customer[2])
        edit_fields["Email"].delete(0, tk.END)
        edit_fields["Email"].insert(0, customer[3])
        edit_fields["Phone"].delete(0, tk.END)
        edit_fields["Phone"].insert(0, customer[4])

        rental_query = """
            SELECT Rentals.rental_id, Cars.car_type, Rentals.rental_start_date, Rentals.rental_end_date
            FROM Rentals
            JOIN Cars ON Rentals.car_id = Cars.car_id
            WHERE Rentals.customer_id = %s
        """
        cursor.execute(rental_query, (customer[0],))
        rental_rows = cursor.fetchall()

        rental_tree.delete(*rental_tree.get_children())
        rental_tree["columns"] = ["rental_id", "car_type", "start_date", "end_date"]
        rental_tree["show"] = "headings"
        for col in rental_tree["columns"]:
            rental_tree.heading(col, text=col)
        for row in rental_rows:
            rental_tree.insert("", tk.END, values=row)

        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Update customer information
def update_customer():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = """
            UPDATE Customers SET first_name=%s, last_name=%s, email=%s, phone=%s WHERE customer_id=%s
        """
        data = (
            edit_fields["First Name"].get(),
            edit_fields["Last Name"].get(),
            edit_fields["Email"].get(),
            edit_fields["Phone"].get(),
            current_customer_id.get()
        )
        cursor.execute(query, data)
        conn.commit()
        messagebox.showinfo("Success", "Customer updated successfully")
        cursor.close()
        conn.close()
        # Refresh the customer details and rental history
        search_customer(search_field.get(), search_entry, cust_info_label, rental_table)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Delete customer
def delete_customer():
    confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this customer?")
    if not confirm:
        return
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Customers WHERE customer_id=%s", (current_customer_id.get(),))
        conn.commit()
        messagebox.showinfo("Deleted", "Customer deleted successfully")
        cust_info_label.config(text="Customer Info:")
        for entry in edit_fields.values():
            entry.delete(0, tk.END)
        rental_table.delete(*rental_table.get_children())
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Configure buttons
search_btn.config(command=lambda: search_customer(search_field.get(), search_entry, cust_info_label, rental_table))
update_btn.config(command=update_customer)
delete_btn.config(command=delete_customer)

#Add New Customer
# Add form frame
add_form_frame = ttk.LabelFrame(cust_tab, text="Add New Customer")

# Container for form fields
form_frame = ttk.Frame(add_form_frame)
form_frame.pack(padx=20, pady=10, fill='x')

# Entry variables
f_name = ttk.Entry(form_frame)
l_name = ttk.Entry(form_frame)
email = ttk.Entry(form_frame)
phone = ttk.Entry(form_frame)

fields = [
    ("First Name", f_name),
    ("Last Name", l_name),
    ("Email", email),
    ("Phone", phone)
]

# Grid layout for proper table-like alignment
for i, (label_text, entry) in enumerate(fields):
    ttk.Label(form_frame, text=label_text, anchor='w').grid(row=i, column=0, sticky='w', padx=5, pady=5)
    entry.grid(row=i, column=1, sticky='ew', padx=5, pady=5)

form_frame.columnconfigure(1, weight=1)  # Let entry column expand

# Add button centered below the form
ttk.Button(add_form_frame, text="Add Customer", command=lambda: add_customer(f_name, l_name, email, phone, new_customer_table)).pack(pady=10)




# Table to show newly added customers
new_customer_table = ttk.Treeview(add_form_frame)
new_customer_table.pack(fill='both', expand=True, padx=10, pady=10)


# --------------------- Inventory Tab ---------------------
inventory_tab = ttk.Frame(notebook)
notebook.add(inventory_tab, text="Inventory")

# Mode selection for Existing or New Car
car_mode_var = tk.StringVar(value="existing")  # Default to 'existing'

car_mode_frame = ttk.LabelFrame(inventory_tab, text="Car Type")
car_mode_frame.pack(fill='x', padx=10, pady=5)

# Store selected car ID
current_car_id = tk.IntVar()

def update_car_mode():
    if car_mode_var.get() == "existing":
        search_car_container.pack(fill='both', expand=True, padx=10, pady=5)
        add_car_form_frame.pack_forget()
    else:
        search_car_container.pack_forget()
        add_car_form_frame.pack(fill='x', padx=10, pady=5)
        run_query("SELECT * FROM Cars", new_car_table)

ttk.Radiobutton(car_mode_frame, text="Existing", variable=car_mode_var, value="existing", command=update_car_mode).pack(side='left', padx=10)
ttk.Radiobutton(car_mode_frame, text="New", variable=car_mode_var, value="new", command=update_car_mode).pack(side='left', padx=10)

# --------------------- Existing Car Search ---------------------

search_car_container = ttk.Frame(inventory_tab)

# Left search frame for Car
search_car_frame = ttk.LabelFrame(search_car_container, text="Search Existing Car")
search_car_frame.pack(side='left', fill='y', padx=5, pady=5)

car_search_field = tk.StringVar()
car_search_menu = ttk.Combobox(
    search_car_frame,
    textvariable=car_search_field,
    values=["car_id", "car_type", "car_color"]
)

car_search_field.set("car_id")
car_search_entry = ttk.Entry(search_car_frame)
car_search_btn = ttk.Button(search_car_frame, text="Search")

car_search_menu.pack(fill='x', padx=5, pady=2)
car_search_entry.pack(fill='x', padx=5, pady=2)
car_search_btn.pack(padx=5, pady=5)

# Right display frame for Car
car_details_frame = ttk.LabelFrame(search_car_container, text="Car Details")
car_details_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)

# Editable fields for car update
car_edit_fields = {}
for label in ["Car Type", "Car Color", "Car Price"]:
    row = ttk.Frame(car_details_frame)
    row.pack(fill='x', padx=5, pady=2)
    ttk.Label(row, text=label, width=10).pack(side='left')
    entry = ttk.Entry(row)
    entry.pack(fill='x', expand=True)
    car_edit_fields[label] = entry

# Buttons for update and delete
car_btn_frame = ttk.Frame(car_details_frame)
car_btn_frame.pack(pady=5)

car_update_btn = ttk.Button(car_btn_frame, text="Update Car")
car_delete_btn = ttk.Button(car_btn_frame, text="Delete Car")
car_update_btn.pack(side='left', padx=5)
car_delete_btn.pack(side='left', padx=5)

# Car info label
car_info_label = ttk.Label(car_details_frame, text="Car Info:", anchor="w", justify='left')
car_info_label.pack(fill='x', padx=5, pady=5)

# Car Search functionality
def search_car(search_field, search_value, info_label):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = f"SELECT * FROM Cars WHERE {search_field} LIKE %s"
        cursor.execute(query, (f"%{search_value.get()}%",))
        rows = cursor.fetchall()

        if not rows:
            messagebox.showinfo("Info", "No car found")
            return

        car = rows[0]
        current_car_id.set(car[0])  # Store car_id for update/delete

        info_label.config(text=f"Car Info:\nID: {car[0]}\nType: {car[1]}\nColor: {car[2]}\nPrice: ${car[3]}")
        car_edit_fields["Car Type"].delete(0, tk.END)
        car_edit_fields["Car Type"].insert(0, car[1])
        car_edit_fields["Car Color"].delete(0, tk.END)
        car_edit_fields["Car Color"].insert(0, car[2])
        car_edit_fields["Car Price"].delete(0, tk.END)
        car_edit_fields["Car Price"].insert(0, car[3])

        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Update car information
def update_car():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        query = """
            UPDATE Cars SET car_type=%s, car_color=%s, car_price=%s WHERE car_id=%s
        """
        data = (
            car_edit_fields["Car Type"].get(),
            car_edit_fields["Car Color"].get(),
            car_edit_fields["Car Price"].get(),
            current_car_id.get()
        )
        cursor.execute(query, data)
        conn.commit()
        messagebox.showinfo("Success", "Car updated successfully")
        cursor.close()
        conn.close()
        # Refresh the car details
        search_car(car_search_field.get(), car_search_entry, car_info_label)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Delete car
def delete_car():
    confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this car?")
    if not confirm:
        return
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Cars WHERE car_id=%s", (current_car_id.get(),))
        conn.commit()
        messagebox.showinfo("Deleted", "Car deleted successfully")
        car_info_label.config(text="Car Info:")
        for entry in car_edit_fields.values():
            entry.delete(0, tk.END)
        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Configure buttons
car_search_btn.config(command=lambda: search_car(car_search_field.get(), car_search_entry, car_info_label))
car_update_btn.config(command=update_car)
car_delete_btn.config(command=delete_car)

# --------------------- Add New Car ---------------------
# Add form frame for new car
add_car_form_frame = ttk.LabelFrame(inventory_tab, text="Add New Car")

# Container for form fields
car_form_frame = ttk.Frame(add_car_form_frame)
car_form_frame.pack(padx=20, pady=10, fill='x')

# Entry variables for new car
car_type = ttk.Entry(car_form_frame)
car_color = ttk.Entry(car_form_frame)
car_price = ttk.Entry(car_form_frame)

car_fields = [
    ("Car Type", car_type),
    ("Car Color", car_color),
    ("Car Price", car_price)
]

# Grid layout for car form
for i, (label_text, entry) in enumerate(car_fields):
    ttk.Label(car_form_frame, text=label_text, anchor='w').grid(row=i, column=0, sticky='w', padx=5, pady=5)
    entry.grid(row=i, column=1, sticky='ew', padx=5, pady=5)

car_form_frame.columnconfigure(1, weight=1)  # Let entry column expand

# Add button centered below the form
ttk.Button(add_car_form_frame, text="Add Car", command=lambda: add_car(car_type, car_color, car_price)).pack(pady=10)

# Table to show newly added cars
new_car_table = ttk.Treeview(add_car_form_frame)
new_car_table.pack(fill='both', expand=True, padx=10, pady=10)

# Configure default mode to show existing car by default
update_car_mode()



# --------------------- Rentals Tab ---------------------
rentals_tab = ttk.Frame(notebook)
notebook.add(rentals_tab, text="Rentals")

rental_mode_var = tk.StringVar(value="existing")

# Mode selection: Create or View/Modify
rental_mode_frame = ttk.LabelFrame(rentals_tab, text="Rental Mode")
rental_mode_frame.pack(fill='x', padx=10, pady=5)

def update_rental_mode():
    if rental_mode_var.get() == "existing":
        modify_rental_frame.pack(fill='both', expand=True, padx=10, pady=5)
        create_rental_frame.pack_forget()
    else:
        create_rental_frame.pack(fill='x', padx=10, pady=5)
        modify_rental_frame.pack_forget()

ttk.Radiobutton(rental_mode_frame, text="Existing Rentals", variable=rental_mode_var, value="existing", command=update_rental_mode).pack(side='left', padx=10)
ttk.Radiobutton(rental_mode_frame, text="New Rental", variable=rental_mode_var, value="new", command=update_rental_mode).pack(side='left', padx=10)

# ------------------ Create New Rental Section ------------------
create_rental_frame = ttk.LabelFrame(rentals_tab, text="Create New Rental")

# Layout using grid for form fields
form = ttk.Frame(create_rental_frame)
form.pack(padx=20, pady=10, fill='x')

# Entry widgets
cust_id = ttk.Entry(form)
car_id = ttk.Entry(form)
start = ttk.Entry(form)
end = ttk.Entry(form)

# Labels and fields in grid
labels = ["Customer ID", "Car ID", "Start Date (YYYY-MM-DD)", "End Date (YYYY-MM-DD)"]
entries = [cust_id, car_id, start, end]

for i, (label, entry) in enumerate(zip(labels, entries)):
    ttk.Label(form, text=label, anchor="w").grid(row=i, column=0, sticky="w", padx=5, pady=5)
    entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5)

form.columnconfigure(1, weight=1)

# Label to show estimated price
estimated_price_label = ttk.Label(create_rental_frame, text="Estimated Invoice: $0.00", font=("Helvetica", 10, "bold"))
estimated_price_label.pack(pady=5)

# Estimate rental cost
def estimate_rental():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        car_id_val = car_id.get()
        cursor.execute("SELECT car_price FROM Cars WHERE car_id = %s", (car_id_val,))
        result = cursor.fetchone()

        if not result:
            messagebox.showerror("Error", "Invalid Car ID")
            return

        daily_rate = result[0]
        from datetime import datetime
        start_date = datetime.strptime(start.get(), "%Y-%m-%d")
        end_date = datetime.strptime(end.get(), "%Y-%m-%d")
        num_days = (end_date - start_date).days

        if num_days <= 0:
            messagebox.showerror("Error", "End date must be after start date.")
            return

        total = round(num_days * daily_rate, 2)
        estimated_price_label.config(text=f"Estimated Invoice: ${total}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# --- Rental Summary Frame (initially hidden) ---
rental_summary_frame = ttk.LabelFrame(create_rental_frame, text="Rental Summary")
rental_summary_frame.pack(fill='x', padx=20, pady=10)
rental_summary_frame.pack_forget()  # hide by default

rental_summary_label = ttk.Label(rental_summary_frame, text="", justify="left", font=("Segoe UI", 10, "bold"))
rental_summary_label.pack(anchor="w", padx=10, pady=5)

# --- Create Rental and Show Summary ---
def create_rental_after_estimate():
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Insert rental
        cursor.execute("""
            INSERT INTO Rentals (customer_id, car_id, rental_start_date, rental_end_date)
            VALUES (%s, %s, %s, %s)
        """, (cust_id.get(), car_id.get(), start.get(), end.get()))
        rental_id = cursor.lastrowid

        # Calculate duration and cost
        cursor.execute("SELECT car_price, car_type FROM Cars WHERE car_id = %s", (car_id.get(),))
        car_data = cursor.fetchone()
        if not car_data:
            messagebox.showerror("Error", "Car not found.")
            return
        car_price, car_type_str = car_data

        cursor.execute("SELECT first_name, last_name FROM Customers WHERE customer_id = %s", (cust_id.get(),))
        cust_data = cursor.fetchone()
        if not cust_data:
            messagebox.showerror("Error", "Customer not found.")
            return
        cust_full_name = f"{cust_data[0]} {cust_data[1]}"

        from datetime import datetime
        days = (datetime.strptime(end.get(), "%Y-%m-%d") - datetime.strptime(start.get(), "%Y-%m-%d")).days
        if days <= 0:
            messagebox.showerror("Error", "End date must be after start date.")
            return
        total = round(days * car_price, 2)

        
        conn.commit()

        #messagebox.showinfo("Success", f"Rental created! Invoice: ${total}")

        # Show summary
        summary_text = f"""
Customer: {cust_full_name}
Car Type: {car_type_str}
Duration: {days} day(s)
Cost: ${total}
"""
        rental_summary_label.config(text=summary_text.strip())
        rental_summary_frame.pack(fill='x', padx=20, pady=10)

        cursor.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))


# Buttons
btns = ttk.Frame(create_rental_frame)
btns.pack(pady=10)

ttk.Button(btns, text="Estimate Price", command=estimate_rental).pack(side="left", padx=10)
ttk.Button(btns, text="Create Rental", command=create_rental_after_estimate).pack(side="left", padx=10)


# ------------------ View & Modify Existing Rentals ------------------
modify_rental_frame = ttk.LabelFrame(rentals_tab, text="View & Modify Rentals")

# Rental table
rental_table = ttk.Treeview(modify_rental_frame)
rental_table.pack(fill='both', expand=True, padx=10, pady=10)

def view_all_rentals():
    run_query("""
        SELECT Rentals.rental_id, Customers.first_name, Customers.last_name,
               Cars.car_type, Rentals.rental_start_date, Rentals.rental_end_date
        FROM Rentals
        JOIN Customers ON Rentals.customer_id = Customers.customer_id
        JOIN Cars ON Rentals.car_id = Cars.car_id
    """, rental_table)

ttk.Button(modify_rental_frame, text="View All Rentals", command=view_all_rentals).pack(pady=5)

# Update rental details
update_rental_frame = ttk.LabelFrame(modify_rental_frame, text="Modify Rental")
update_rental_frame.pack(fill='x', padx=10, pady=5)

update_fields = {
    "Rental ID": ttk.Entry(update_rental_frame),
    "Start Date": ttk.Entry(update_rental_frame),
    "End Date": ttk.Entry(update_rental_frame)
}

for label, entry in update_fields.items():
    row = ttk.Frame(update_rental_frame)
    row.pack(fill='x', padx=5, pady=2)
    ttk.Label(row, text=label, width=15).pack(side='left')
    entry.pack(fill='x', expand=True)

def update_rental():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        rental_id = update_fields["Rental ID"].get()
        new_start = update_fields["Start Date"].get()
        new_end = update_fields["End Date"].get()

        cursor.execute("""
            UPDATE Rentals SET rental_start_date = %s, rental_end_date = %s WHERE rental_id = %s
        """, (new_start, new_end, rental_id))

        cursor.execute("""
            SELECT car_price FROM Cars 
            JOIN Rentals ON Rentals.car_id = Cars.car_id 
            WHERE Rentals.rental_id = %s
        """, (rental_id,))
        daily_rate = cursor.fetchone()[0]
        from datetime import datetime
        num_days = (datetime.strptime(new_end, "%Y-%m-%d") - datetime.strptime(new_start, "%Y-%m-%d")).days
        new_total = round(num_days * daily_rate, 2)

        cursor.execute("""
            UPDATE Invoices SET invoice_amount = %s WHERE rental_id = %s
        """, (new_total, rental_id))

        conn.commit()
        messagebox.showinfo("Success", f"Rental updated! New Invoice: ${new_total}")
        cursor.close()
        conn.close()
        view_all_rentals()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def delete_rental():
    rental_id = update_fields["Rental ID"].get()
    if not rental_id:
        messagebox.showerror("Error", "Enter Rental ID to delete.")
        return
    confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this rental?")
    if not confirm:
        return
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Rentals WHERE rental_id = %s", (rental_id,))
        conn.commit()
        messagebox.showinfo("Deleted", "Rental deleted successfully")
        cursor.close()
        conn.close()
        view_all_rentals()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Update/Delete buttons
btn_row = ttk.Frame(update_rental_frame)
btn_row.pack(pady=5)
ttk.Button(btn_row, text="Update Rental", command=update_rental).pack(side='left', padx=5)
ttk.Button(btn_row, text="Delete Rental", command=delete_rental).pack(side='left', padx=5)

# Load default view
update_rental_mode()



# --------------------- Reports Tab ---------------------
report_tab = ttk.Frame(notebook)
notebook.add(report_tab, text="Reports")

frame1 = ttk.LabelFrame(report_tab, text="List All Tables")
frame1.pack(fill='x', padx=10, pady=10)

frame2 = ttk.LabelFrame(report_tab, text="Predefined Queries")
frame2.pack(fill='x', padx=10, pady=10)

tree = ttk.Treeview(report_tab)
tree.pack(fill='both', expand=True, padx=10, pady=10)

queries = {
    "All Customers": "SELECT * FROM Customers",
    "All Cars": "SELECT * FROM Cars",
    "All Rentals": "SELECT * FROM Rentals",
    "All Invoices": "SELECT * FROM Invoices",
    "Total Earnings per Car": """
        SELECT Cars.car_id, Cars.car_type, SUM(Invoices.invoice_amount) AS TotalEarnings
        FROM Cars
        JOIN Rentals ON Rentals.car_id = Cars.car_id
        JOIN Invoices ON Invoices.rental_id = Rentals.rental_id
        GROUP BY Cars.car_id
    """,
    "Total Rentals per Customer": """
        SELECT Customers.customer_id, Customers.first_name, Customers.last_name, COUNT(*) AS TotalRentals
        FROM Rentals
        JOIN Customers ON Rentals.customer_id = Customers.customer_id
        GROUP BY Customers.customer_id
    """,
    "Most Rented Cars": """
        SELECT Cars.car_id, Cars.car_type, COUNT(Rentals.rental_id) AS NumberOfRentals
        FROM Cars
        JOIN Rentals ON Rentals.car_id = Cars.car_id
        GROUP BY Cars.car_id
        ORDER BY NumberOfRentals DESC
    """
}

for label in ["All Customers", "All Cars", "All Rentals", "All Invoices"]:
    ttk.Button(frame1, text=label, width=30, command=lambda q=queries[label]: run_query(q, tree)).pack(side='left', padx=5, pady=5)

for label in ["Total Earnings per Car", "Total Rentals per Customer", "Most Rented Cars"]:
    ttk.Button(frame2, text=label, width=35, command=lambda q=queries[label]: run_query(q, tree)).pack(side='left', padx=5, pady=5)

app.mainloop()