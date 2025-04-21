import pyodbc

server = 'NAVEEN-GARG-PC'
username = 'naveen'
password = '1234'

conn_str = f'DRIVER={{SQL Server}};SERVER={server};UID={username};PWD={password}'

conn = None
cursor = None

try:
    # Connect to SQL Server
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    # Execute SQL to fetch databases
    cursor.execute("SELECT name FROM sys.databases ORDER BY name ASC")
    databases = cursor.fetchall()

    print("Available Databases:")
    for db in databases:
        print(f"--> {db.name}")

except pyodbc.Error as e:
    print(f"Error while fetching databases:{e}")

finally:
    # Close cursor and connection safely
    if cursor:
        cursor.close()
    if conn:
        conn.close()
