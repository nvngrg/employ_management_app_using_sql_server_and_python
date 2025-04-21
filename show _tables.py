import pyodbc

# Connection details
server = 'NAVEEN-GARG-PC'
username = 'naveen'
password = '1234'
database = 'naveenDB'  # Change this to the name of your database

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

    # Execute the query to get all tables sorted alphabetically
    cursor.execute("""
        SELECT table_name 
        FROM INFORMATION_SCHEMA.TABLES 
        WHERE table_type = 'BASE TABLE' 
        ORDER BY table_name ASC
    """)

    # Fetch all results
    tables = cursor.fetchall()

    # Print the tables in sorted order
    print(f"Tables in {database} Database:")
    for table in tables:
        print(f"==> {table.table_name}")

except pyodbc.Error as e:
    print("An error occurred while fetching tables:")
    print(e)

finally:
    # Ensure the connection and cursor are closed
    if cursor is not None:
        cursor.close()
    if conn is not None:
        conn.close()
