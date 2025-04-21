import pyodbc

# Connection details
server = 'NAVEEN-GARG-PC'
username = 'naveen'
password = '1234'
database = 'naveenDB'  # Name of your database
table_name = 'employee'  # Name of your table

# Connection string with the specific database
conn_str = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Initialize the connection and cursor
conn = None
cursor = None

try:
    # Establish the connection
    conn = pyodbc.connect(conn_str)
    
    # Create a cursor object
    cursor = conn.cursor()

    # Insert 15 records into the employee table (Data Science related jobs)
    records = [
        ('John Doe', 'Data Scientist', 75000, 'Bangalore, Karnataka'),
        ('Jane Smith', 'Machine Learning Engineer', 80000, 'Hyderabad, Telangana'),
        ('Alice Johnson', 'Data Analyst', 60000, 'Mumbai, Maharashtra'),
        ('Bob Brown', 'Business Intelligence Analyst', 55000, 'Pune, Maharashtra'),
        ('Carol White', 'AI Engineer', 85000, 'Chennai, Tamil Nadu'),
        ('David Green', 'Data Scientist', 78000, 'Delhi, Delhi'),
        ('Eva Black', 'Data Engineer', 70000, 'Kolkata, West Bengal'),
        ('Frank Clark', 'Machine Learning Scientist', 82000, 'Noida, Uttar Pradesh'),
        ('Grace Lewis', 'Data Analyst', 60000, 'Ahmedabad, Gujarat'),
        ('Hank Scott', 'AI Researcher', 90000, 'Chandigarh, Chandigarh'),
        ('Ivy Adams', 'Data Engineer', 72000, 'Bhubaneswar, Odisha'),
        ('Jack Carter', 'Data Scientist', 85000, 'Surat, Gujarat'),
        ('Kathy Evans', 'Machine Learning Engineer', 78000, 'Jaipur, Rajasthan'),
        ('Leo White', 'Data Analyst', 65000, 'Lucknow, Uttar Pradesh'),
        ('Mona Taylor', 'Business Intelligence Engineer', 70000, 'Indore, Madhya Pradesh')
    ]
    
    # Insert records into the employee table
    for record in records:
        cursor.execute(f"INSERT INTO {table_name} (Ename, Ejob, Esalary, Eaddress) VALUES (?, ?, ?, ?)", record)

    # Commit the changes
    conn.commit()
    print(f"records inserted successfully into the {table_name} table.")

except pyodbc.Error as e:
    print(f"An error occurred while inserting records in {table_name} table:")
    print(e)

finally:
    # Ensure the connection and cursor are closed
    if cursor is not None:
        cursor.close()
    if conn is not None:
        conn.close()
