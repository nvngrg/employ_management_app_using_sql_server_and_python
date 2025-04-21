import pyodbc

# SQL Server connection details
server = 'NAVEEN-GARG-PC'
username = 'naveen'
password = '1234'

# Connect without specifying a database
conn_str = f'DRIVER={{SQL Server}};SERVER={server};UID={username};PWD={password}'
try:
    conn = pyodbc.connect(conn_str, autocommit=True)
    cursor = conn.cursor()

    # Define new database name
    new_db_name = 'naveenDB'  # Change this to your desired DB name

    # Create database
    cursor.execute(f"IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'{new_db_name}') CREATE DATABASE [{new_db_name}]")
    print(f" Database '{new_db_name}' created successfully.")

    cursor.close()
    conn.close()

except Exception as e:
    print("Database creation failed!")
    print(e)
