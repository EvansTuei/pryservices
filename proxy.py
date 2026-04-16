from fastapi import FastAPI
import psycopg
import os

app = FastAPI()

# Optional: fail fast if critical env vars are missing
required_env_vars = ["DB_HOST", "DB_USER", "DB_PASSWORD", "DB_NAME"]
for var in required_env_vars:
    if not os.environ.get(var):
        raise ValueError(f"{var} is not set")


def get_connection():
    return psycopg.connect(
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
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users;")
            
            columns = [desc.name for desc in cur.description]
            rows = cur.fetchall()

            result = [dict(zip(columns, row)) for row in rows]

    return {"data": result}

@app.get("/test-db")
def test_db():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1;")
                return {"result": cur.fetchone()}
    except Exception as e:
        return {"error": str(e)}