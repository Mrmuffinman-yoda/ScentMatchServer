import time
import psycopg2
import os


def wait():
    host = os.getenv("DB_HOST")
    dbname = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    port = os.getenv("DB_PORT")

    while True:
        try:
            conn = psycopg2.connect(
                dbname=dbname, user=user, password=password, host=host, port=port
            )
            conn.close()
            print("✅ Postgres is ready!")
            break
        except psycopg2.OperationalError as e:
            print("⏳ Waiting for Postgres...:", str(e))
            time.sleep(1)


if __name__ == "__main__":
    wait()
