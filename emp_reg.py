import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pyodbc
import csv

# Function to create a database connection
def get_db_connection():
    return pyodbc.connect(
        'DRIVER={SQL Server};'
        'SERVER=NAVEEN-GARG-PC;'
        'DATABASE=naveenDB;'
        'UID=naveen;'
        'PWD=1234'
    )

# Add a new employee to the database
def add_employee():
    empname = e2.get()
    empjob = e3.get()
    empsalary = e4.get()
    empaddress = e5.get()

    if not empname or not empjob or not empsalary or not empaddress:
        messagebox.showerror("Input Error", "All fields must be filled.")
        return

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO employee (Ename, Ejob, Esalary, Eaddress) VALUES (?, ?, ?, ?)"
        values = (empname, empjob, empsalary, empaddress)
        cursor.execute(sql, values)
        conn.commit()
        messagebox.showinfo("Success", "Employee record added successfully!")
        clear_entries()
        load_employees()

    except pyodbc.Error as err:
        messagebox.showerror("Database Error", f"Failed to insert employee: {err}")
    finally:
        if conn:
            conn.close()

# Update an existing employee record
def update_employee():
    selected_item = listBox.selection()
    if not selected_item:
        messagebox.showerror("Selection Error", "Please select an employee to update.")
        return

    empid = e1.get()
    empname = e2.get()
    empjob = e3.get()
    empsalary = e4.get()
    empaddress = e5.get()

    if not empname or not empjob or not empsalary or not empaddress:
        messagebox.showerror("Input Error", "All fields must be filled.")
        return

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "UPDATE employee SET Ename=?, Ejob=?, Esalary=?, Eaddress=? WHERE Eid=?"
        values = (empname, empjob, empsalary, empaddress, empid)
        cursor.execute(sql, values)
        conn.commit()
        messagebox.showinfo("Success", "Employee record updated successfully!")
        clear_entries()
        load_employees()

    except pyodbc.Error as err:
        messagebox.showerror("Database Error", f"Failed to update employee: {err}")
    finally:
        if conn:
            conn.close()

# Delete an employee from the database
def delete_employee():
    empid = e1.get()

    if not empid:
        messagebox.showerror("Selection Error", "Please select an employee to delete.")
        return

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "DELETE FROM employee WHERE Eid=?"
        cursor.execute(sql, (empid,))
        conn.commit()
        messagebox.showinfo("Success", "Employee record deleted successfully!")
        clear_entries()
        load_employees()

    except pyodbc.Error as err:
        messagebox.showerror("Database Error", f"Failed to delete employee: {err}")
    finally:
        if conn:
            conn.close()

# Load all employee records into the Treeview
def load_employees():
    for row in listBox.get_children():
        listBox.delete(row)

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employee ORDER BY Eid ASC")
        rows = cursor.fetchall()

        for row in rows:
            clean_row = tuple(str(col) for col in row)
            listBox.insert("", "end", values=clean_row)

    except pyodbc.Error as err:
        messagebox.showerror("Database Error", f"Failed to load employees: {err}")
    finally:
        if conn:
            conn.close()

# Search employees by name
def search_employees():
    keyword = search_entry.get().strip().lower()
    for row in listBox.get_children():
        listBox.delete(row)

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM employee WHERE LOWER(Ename) LIKE ?", ('%' + keyword + '%',))
        rows = cursor.fetchall()

        for row in rows:
            clean_row = tuple(str(col) for col in row)
            listBox.insert("", "end", values=clean_row)

    except pyodbc.Error as err:
        messagebox.showerror("Database Error", f"Search failed: {err}")
    finally:
        if conn:
            conn.close()

# Fill entry fields when a row in Treeview is selected
def on_treeview_select(event):
    selected_item = listBox.selection()
    if selected_item:
        employee = listBox.item(selected_item)
        empid, empname, empjob, empsalary, empaddress = employee['values']

        e1.config(state="normal")
        e1.delete(0, tk.END)
        e1.insert(0, empid)
        e1.config(state="disabled")

        e2.delete(0, tk.END)
        e2.insert(0, empname)

        e3.delete(0, tk.END)
        e3.insert(0, empjob)

        e4.delete(0, tk.END)
        e4.insert(0, empsalary)

        e5.delete(0, tk.END)
        e5.insert(0, empaddress)

# Clear all entry fields
def clear_entries():
    e1.config(state="normal")
    e1.delete(0, tk.END)
    e1.config(state="disabled")
    e2.delete(0, tk.END)
    e3.delete(0, tk.END)
    e4.delete(0, tk.END)
    e5.delete(0, tk.END)

# Export data to CSV
def export_to_csv():
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    try:
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Name', 'Job', 'Salary', 'Address'])
            for row_id in listBox.get_children():
                row = listBox.item(row_id)['values']
                writer.writerow(row)
        messagebox.showinfo("Success", f"Data exported successfully to {file_path}")
    except Exception as e:
        messagebox.showerror("Export Error", f"Failed to export data: {e}")

# ---------------- GUI Setup ----------------
root = tk.Tk()
root.title("Employee Management System")
root.configure(bg="#e6f2ff")
root.minsize(850, 600)
root.resizable(True, True)

root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(8, weight=1)

title = tk.Label(root, text="Employee Management System", font=("Helvetica", 18, "bold"), bg="#007acc", fg="white", pady=10)
title.grid(row=0, column=0, columnspan=6, sticky="ew")

label_font = ("Helvetica", 10, "bold")
entry_width = 30

# Labels and Entry fields
tk.Label(root, text="Employee ID", font=label_font, bg="#e6f2ff").grid(row=1, column=0, padx=10, pady=10, sticky="w")
tk.Label(root, text="Name", font=label_font, bg="#e6f2ff").grid(row=2, column=0, padx=10, pady=10, sticky="w")
tk.Label(root, text="Job", font=label_font, bg="#e6f2ff").grid(row=3, column=0, padx=10, pady=10, sticky="w")
tk.Label(root, text="Salary", font=label_font, bg="#e6f2ff").grid(row=4, column=0, padx=10, pady=10, sticky="w")
tk.Label(root, text="Address", font=label_font, bg="#e6f2ff").grid(row=5, column=0, padx=10, pady=10, sticky="w")

e1 = tk.Entry(root, width=entry_width, font=("Arial", 10))
e1.grid(row=1, column=1, padx=10, pady=10)
e1.config(state="disabled")

e2 = tk.Entry(root, width=entry_width, font=("Arial", 10))
e2.grid(row=2, column=1, padx=10, pady=10)

e3 = tk.Entry(root, width=entry_width, font=("Arial", 10))
e3.grid(row=3, column=1, padx=10, pady=10)

e4 = tk.Entry(root, width=entry_width, font=("Arial", 10))
e4.grid(row=4, column=1, padx=10, pady=10)

e5 = tk.Entry(root, width=entry_width, font=("Arial", 10))
e5.grid(row=5, column=1, padx=10, pady=10)

# Search bar
tk.Label(root, text="Search Name", font=label_font, bg="#e6f2ff").grid(row=1, column=2, padx=10, pady=10, sticky="w")
search_entry = tk.Entry(root, width=25, font=("Arial", 10))
search_entry.grid(row=1, column=3, padx=10, pady=10)
tk.Button(root, text="Search", width=12, command=search_employees, bg="#00aaff", fg="white", font=("Helvetica", 10, "bold")).grid(row=1, column=4, padx=10, pady=10)

# Buttons
btn_style = {"font": ("Helvetica", 10, "bold"), "bg": "#007acc", "fg": "white", "padx": 10, "pady": 5}
tk.Button(root, text="Add", width=12, command=add_employee, **btn_style).grid(row=6, column=0, padx=10, pady=15)
tk.Button(root, text="Update", width=12, command=update_employee, **btn_style).grid(row=6, column=1, padx=10, pady=15)
tk.Button(root, text="Delete", width=12, command=delete_employee, **btn_style).grid(row=6, column=2, padx=10, pady=15)
tk.Button(root, text="Export CSV", width=12, command=export_to_csv, **btn_style).grid(row=6, column=3, padx=10, pady=15)
tk.Button(root, text="Show All", width=12, command=load_employees, **btn_style).grid(row=6, column=4, padx=10, pady=15)

# Treeview Frame
tree_frame = tk.Frame(root)
tree_frame.grid(row=8, column=0, columnspan=6, padx=20, pady=10, sticky="nsew")
tree_frame.grid_rowconfigure(0, weight=1)
tree_frame.grid_columnconfigure(0, weight=1)

cols = ('ID', 'Name', 'Job', 'Salary', 'Address')
listBox = ttk.Treeview(tree_frame, columns=cols, show='headings')
style = ttk.Style()
style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'), background="#cce6ff")
style.map('Treeview', background=[('selected', '#4da6ff')])
style.configure("Treeview", rowheight=28, font=('Arial', 10))

for col in cols:
    listBox.heading(col, text=col)
    listBox.column(col, minwidth=0, width=140, anchor=tk.CENTER)

listBox.grid(row=0, column=0, sticky="nsew")
listBox.bind('<<TreeviewSelect>>', on_treeview_select)

# Scrollbar
scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=listBox.yview)
listBox.configure(yscrollcommand=scrollbar.set)
scrollbar.grid(row=0, column=1, sticky='ns')

# Load initial data
load_employees()

root.mainloop()
