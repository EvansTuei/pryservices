from fastapi import FastAPI
import psycopg2
import os

app = FastAPI()

# Optional: fail fast if critical env vars are missing
required_env_vars = ["DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME"]
for var in required_env_vars:
    if not os.environ.get(var):
        raise ValueError(f"{var} is not set")


def get_connection():
    return psycopg2.connect(
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
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users;")

    # Get column names
    columns = [desc[0] for desc in cur.description]

    # Fetch data
    rows = cur.fetchall()

    # Convert to list of dictionaries (JSON-friendly)
    result = [dict(zip(columns, row)) for row in rows]

    # Clean up
    cur.close()
    conn.close()

    return {"data": result}