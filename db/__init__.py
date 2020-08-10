from peewee import SqliteDatabase
from config import DB_FILE_NAME

db = SqliteDatabase(DB_FILE_NAME)
