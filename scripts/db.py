import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="northwind",
        user="etl",
        password="demopass",
        host="localhost",
        port="5433"
    )
