from fastapi import FastAPI
import psycopg2
import os

app = FastAPI()

conn = psycopg2.connect(
    host=os.environ.get("DB_HOST"),
    port=os.environ.get("DB_PORT", 5432),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    dbname=os.environ.get("DB_NAME")
)

@app.get("/")
def read_root():
    return {"status": "ok"}

@app.get("/users")
def get_users():
    cur = conn.cursor()
    cur.execute("SELECT * FROM users;")
    rows = cur.fetchall()
    return {"data": rows}