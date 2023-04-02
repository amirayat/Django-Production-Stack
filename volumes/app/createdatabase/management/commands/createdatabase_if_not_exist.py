import os
import psycopg2
from psycopg2 import sql
from django.core.management.base import BaseCommand
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dotenv import load_dotenv


load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = int(os.getenv('DB_PORT'))


con = psycopg2.connect(
    dbname='postgres',
    user=DB_USER, 
    host=DB_HOST,
    password=DB_PASS,
    port=DB_PORT
    )

con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

cur = con.cursor()


class Command(BaseCommand):
    """
    Create a database if none exist
    Example:
        manage.py createdatabase_if_not_exist
    """

    def handle(self, *args, **options):

        cur.execute(
            sql.SQL("SELECT datname FROM pg_database;")
        )
        list_databases = [database[0] for database in cur.fetchall()]
        if not DB_NAME in list_databases:
            cur.execute(
                sql.SQL(f"CREATE DATABASE {DB_NAME}")
            )