from fastapi import FastAPI
import psycopg
import os

app = FastAPI()


def get_connection():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL is not set")
    return psycopg.connect(db_url)


# 🚀 Run once when app starts
@app.on_event("startup")
def startup():
    with get_connection() as conn:
        with conn.cursor() as cur:
            # Create table if it doesn't exist
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name TEXT
                );
            """)

            # Check if table is empty
            cur.execute("SELECT COUNT(*) FROM users;")
            count = cur.fetchone()[0]

            # Insert sample data only if empty
            if count == 0:
                cur.execute("""
                    INSERT INTO users (name) VALUES
                    ('Evans'),
                    ('Alice'),
                    ('Bob');
                """)

        conn.commit()


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