import psycopg2

conn = psycopg2.connect(
    dbname="mydb",
    user="user",
    password="password",
    host="localhost",
    port=5432

)

def save_query(user_input: str, response: str):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (question, answer) VALUES (%s, %s)", (user_input, response))
    conn.commit()
    cursor.close()

def get_queries():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs")
    queries = cursor.fetchall()
    cursor.close()
    return queries
