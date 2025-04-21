import pyodbc
import connectio

conn = None
cursor = None

try:
    conn = connectio.conn
    print("Connection established!")
    cursor = conn.cursor()

    create_table_query = """
    IF NOT EXISTS (
        SELECT * FROM INFORMATION_SCHEMA.TABLES 
        WHERE TABLE_NAME = 'employee'
    )
    CREATE TABLE employee (
        Eid INT IDENTITY(1,1) PRIMARY KEY,
        Ename VARCHAR(100),
        Ejob VARCHAR(100),
        Esalary FLOAT,
        Eaddress VARCHAR(255)
    );
    """

    cursor.execute(create_table_query)
    conn.commit()

    print("Table 'employee' created.")

except pyodbc.Error as e:
    print("Error creating table:")
    print(e)

finally:
    if cursor:
        cursor.close()
    if conn:
        conn.close()
