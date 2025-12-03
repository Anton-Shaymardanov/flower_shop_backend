import psycopg

conn = psycopg.connect(
    dbname="flower_shop",
    user="postgres",
    password="TEST",
    host="localhost",
    port="5432",
)
print("OK: connected")
conn.close()
