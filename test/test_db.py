from app.db.connection import get_connection

try:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES;")
    result = cursor.fetchall()
    tables = [row[0] for row in result]
    print(f"Tables in database: {tables}")

    conn.close()

except Exception as e:
    print(f"Error connecting to database: {e}")
