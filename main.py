from fastapi import FastAPI
import psycopg2

app = FastAPI()


conn = psycopg2.connect("postgresql://username:<ENTER-SQL-USER-PASSWORD>@db-app-693.g8x.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full")

@app.get("/")
async def root():
    with conn.cursor() as cur:
        cur.execute("SELECT now()")
        res = cur.fetchall()
        conn.commit()
        print(res)
    return {"message": "Hello World"}
