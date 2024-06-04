from aiogram.dispatcher.filters.state import State, StatesGroup
import sqlite3

con = sqlite3.connect('base.db')
cur = con.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(user_id INTEGER, user_name TEXT, user TEXT);""")
con.commit()

class dialog(StatesGroup):
    spam = State()
blacklist = State()
whitelist = State()
