# 🧑‍💼 Employee Management System

This is a desktop-based Employee Management System built using Python Tkinter for the frontend and SQL Server for the backend. 
The app allows you to add, update, delete, search, and export employee records easily through a graphical interface.

# **🚀 Features**

--> Add new employees to the SQL Server database

--> Update and delete existing employee records

--> Search employees by name

--> View all records in a clean tabular format (Treeview)

--> Export employee data to CSV

--> Intuitive and user-friendly GUI

# 🛠️ Technologies Used

-> Frontend: Python Tkinter

-> Backend: Microsoft SQL Server

-> Database Driver: pyodbc

-> CSV Export: csv module

# **📷 UI Preview**

 Data base image:- ![image](https://github.com/user-attachments/assets/233bd5e4-09c6-4f7c-8658-b0f69e2494ff)

 Output image:- ![image](https://github.com/user-attachments/assets/98c71e10-7e25-484f-9737-ccc6bd2ba5b5)

# ⚙️ Setup Instructions

1. Clone the repository 

  git clone https://github.com/nvngrg/employ_management_app_using_sql_server_and_python/blob/main/emp_reg.py
  cd employee-management-app

**2. Install Python dependencies**

   pip install pyodbc

**3. Configure your SQL Server**

  * Create a database named `naveenDB`

  * Create a table using the following SQL:

    CREATE TABLE employee
    (
      Eid INT PRIMARY KEY IDENTITY(1,1),
      Ename VARCHAR(100),
      Ejob VARCHAR(100),
      Esalary VARCHAR(100),
      Eaddress VARCHAR(255)
    );
  * Update the connection string in `emp_reg.py` with your SQL Server credentials:
    
    pyodbc.connect
    (
      'DRIVER={SQL Server};'
      'SERVER=YOUR_SERVER_NAME;'
      'DATABASE=naveenDB;'
      'UID=YOUR_USERNAME;'
      'PWD=YOUR_PASSWORD'
   )
**4. Run the app**

    Run the app

# **💡 Future Enhancements**

  * Add login authentication
  
  * Implement dark/light theme toggle
  
  * Add pagination or filtering options
  
 *  Backup & restore functionality
