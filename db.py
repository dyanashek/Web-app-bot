import sqlite3
import logging

database = sqlite3.connect("store.db")
cursor = database.cursor()

try:
    cursor.execute('''CREATE TABLE products(
        id INTEGER PRIMARY KEY,
        name VARCHAR,
        price REAL,
        link TEXT 
    )''')
except:
    logging.error('Products table already exists.')

try:
    cursor.execute('''CREATE TABLE users(
        id INTEGER PRIMARY KEY,
        user_id VARCHAR,
        cart TEXT
    )''')
except:
    logging.error('Users table already exists.')


# cursor.execute("DELETE FROM managers WHERE id=4")
# database.commit()
