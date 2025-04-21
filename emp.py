import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc

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
        cursor.execute("SELECT * FROM employee")
        rows = cursor.fetchall()

        for row in rows:
            clean_row = tuple(str(col) for col in row)  # Convert values to string
            listBox.insert("", "end", values=clean_row)

    except pyodbc.Error as err:
        messagebox.showerror("Database Error", f"Failed to load employees: {err}")
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

# GUI Setup
root = tk.Tk()
root.geometry('750x550')
root.title("Employee Registration System")

# Labels and Entries
tk.Label(root, text="Employee ID").grid(row=0, column=0, padx=10, pady=10)
tk.Label(root, text="Name").grid(row=1, column=0, padx=10, pady=10)
tk.Label(root, text="Job").grid(row=2, column=0, padx=10, pady=10)
tk.Label(root, text="Salary").grid(row=3, column=0, padx=10, pady=10)
tk.Label(root, text="Address").grid(row=4, column=0, padx=10, pady=10)

e1 = tk.Entry(root)
e1.grid(row=0, column=1, padx=10, pady=10)
e1.config(state="disabled")

e2 = tk.Entry(root)
e2.grid(row=1, column=1, padx=10, pady=10)

e3 = tk.Entry(root)
e3.grid(row=2, column=1, padx=10, pady=10)

e4 = tk.Entry(root)
e4.grid(row=3, column=1, padx=10, pady=10)

e5 = tk.Entry(root)
e5.grid(row=4, column=1, padx=10, pady=10)

# Buttons
tk.Button(root, text="Add", width=10, command=add_employee).grid(row=5, column=0, padx=10, pady=10)
tk.Button(root, text="Update", width=10, command=update_employee).grid(row=5, column=1, padx=10, pady=10)
tk.Button(root, text="Delete", width=10, command=delete_employee).grid(row=5, column=2, padx=10, pady=10)

# Treeview for displaying employees
cols = ('ID', 'Name', 'Job', 'Salary', 'Address')
listBox = ttk.Treeview(root, columns=cols, show='headings', height=10)

for col in cols:
    listBox.heading(col, text=col)
    listBox.column(col, minwidth=0, width=140, anchor=tk.CENTER)

listBox.grid(row=6, column=0, columnspan=3, padx=10, pady=20)
listBox.bind('<<TreeviewSelect>>', on_treeview_select)

# Load initial data
load_employees()

root.mainloop()
