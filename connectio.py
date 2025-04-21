import pyodbc

# Update with your actual SQL Server details
server = 'NAVEEN-GARG-PC'  # or use 'localhost\\SQLEXPRESS' if using any local name 
# database = 'YourDatabaseName'  # Replace with your database name
username = 'naveen' # Replace with your SQL Server username
password = '1234' # Replace with your SQL Server password

# Connection string
conn_str = f'DRIVER={{SQL Server}};SERVER={server};UID={username};PWD={password}' # add database={database} if you want to connect to a specific database

try:
    conn = pyodbc.connect(conn_str)
    print("Connection established!")
    print(conn)
except Exception as e:
    print("Connection failed!")
    print(e)
