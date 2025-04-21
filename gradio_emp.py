import gradio as gr
import pyodbc

# SQL Server connection
def create_connection():
    conn = pyodbc.connect(
        r"Driver={SQL Server};"
        r"Server=NAVEEN-GARG-PC;"
        r"Database=EmployeeDB;"
        r"Trusted_Connection=yes;"
    )
    return conn

# Add employee
def add_employee(name, job, salary, address):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Employees (Ename, Ejob, Esalary, Eaddress) VALUES (?, ?, ?, ?)",
            (name, job, salary, address)
        )
        conn.commit()
        conn.close()
        return "✅ Employee added successfully!"
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Update employee
def update_employee(empid, name, job, salary, address):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Employees SET Ename=?, Ejob=?, Esalary=?, Eaddress=? WHERE Eid=?",
            (name, job, salary, address, empid)
        )
        conn.commit()
        conn.close()
        return "✅ Employee updated successfully!"
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Delete employee
def delete_employee(empid):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Employees WHERE Eid=?", (empid,))
        conn.commit()
        conn.close()
        return "✅ Employee deleted successfully!"
    except Exception as e:
        return f"❌ Error: {str(e)}"

# View all employees
def view_employees():
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Employees")
        rows = cursor.fetchall()
        conn.close()

        table = []
        for row in rows:
            table.append([row.Eid, row.Ename, row.Ejob, row.Esalary, row.Eaddress])
        return table
    except Exception as e:
        return [[f"❌ Error: {str(e)}"]]

# Gradio UI
def create_gradio_interface():
    with gr.Blocks(theme=gr.themes.Monochrome()) as demo:
        gr.Markdown("### Built with Python + SQL Server + Gradio UI")

        with gr.Tab("➕ Add Employee"):
            with gr.Column():
                empname = gr.Textbox(label="Name")
                empjob = gr.Textbox(label="Job")
                empsalary = gr.Textbox(label="Salary")
                empaddress = gr.Textbox(label="Address")
                add_button = gr.Button("Add")
                add_status = gr.Textbox(label="Status", interactive=False)
                add_button.click(
                    add_employee, 
                    inputs=[empname, empjob, empsalary, empaddress],
                    outputs=add_status
                )

        with gr.Tab("✏️ Update Employee"):
            with gr.Column():
                empid_upd = gr.Textbox(label="Employee ID")
                empname_upd = gr.Textbox(label="Updated Name")
                empjob_upd = gr.Textbox(label="Updated Job")
                empsalary_upd = gr.Textbox(label="Updated Salary")
                empaddress_upd = gr.Textbox(label="Updated Address")
                update_button = gr.Button("Update")
                update_status = gr.Textbox(label="Status", interactive=False)
                update_button.click(
                    update_employee,
                    inputs=[empid_upd, empname_upd, empjob_upd, empsalary_upd, empaddress_upd],
                    outputs=update_status
                )

        with gr.Tab("❌ Delete Employee"):
            with gr.Column():
                empid_del = gr.Textbox(label="Employee ID")
                delete_button = gr.Button("Delete")
                delete_status = gr.Textbox(label="Status", interactive=False)
                delete_button.click(delete_employee, inputs=empid_del, outputs=delete_status)

        with gr.Tab("📋 View All Employees"):
            with gr.Column():
                view_button = gr.Button("View All Employees")
                employee_table = gr.Dataframe(
                    headers=["ID", "Name", "Job", "Salary", "Address"],
                    interactive=False,
                    wrap=True
                )
                view_button.click(view_employees, outputs=employee_table)

    demo.launch()

# Run the app
if __name__ == "__main__":
    create_gradio_interface()
