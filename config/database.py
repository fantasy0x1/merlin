import sqlite3
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

OWNER_ID = int(os.getenv('OWNER_ID'))
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix=".", case_sensitive=True, intents=intents)

def create_tables():
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS snippets (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    content TEXT,
                    guild_id INTEGER
                )''')

    cur.execute('''CREATE TABLE IF NOT EXISTS operators_list (
                    id INTEGER PRIMARY KEY,
                    user TEXT,
                    guild_id INTEGER
                )''')

    conn.commit()
    conn.close()

def insert_operator(guild_id, user):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO operators_list (guild_id, user) VALUES (?, ?)', (guild_id, user))
    conn.commit()
    conn.close()

def delete_operator(guild_id, user):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('DELETE FROM operators_list WHERE guild_id = ? AND user = ?', (guild_id, user))
    conn.commit()
    conn.close()

def is_operator(guild_id, user):
    if user == OWNER_ID:
        return True
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM operators_list WHERE guild_id = ? AND user = ?', (guild_id, user))
    operator = cur.fetchone()
    conn.close()
    return operator is not None
        
def get_operators(guild):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT user FROM operators_list WHERE guild_id = ?',
                (guild.id,))
    operator_ids = cur.fetchall()
    return operator_ids


def db_exec(cmd):
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute(cmd)
    conn.commit()
    conn.close()