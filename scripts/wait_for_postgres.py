import time
import psycopg2
import os


def wait():
    host = os.getenv("POSTGRES_HOST", "postgres-db-test")  # matches your container_name
    port = int(os.getenv("POSTGRES_PORT", 5432))  # internal Postgres port
    user = os.getenv("POSTGRES_USER", "scentmatch_user")
    password = os.getenv("POSTGRES_PASSWORD", "scentmatch_password")
    dbname = os.getenv("POSTGRES_DB", "scentmatch_test_db")

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
