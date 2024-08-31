import discord
from discord.ext import commands
import sqlite3

class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
       
        cursor.execute("""CREATE TABLE IF NOT EXISTS main (user_id INTEGER, balance INTEGER, bank INTEGER)""")
        print("Бот в сети")

    @commands.Cog.listener()
    async def on_message(self, message):
        
        if message.author.bot:
            return
        
        author = message.author
       
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
        
        cursor.execute("SELECT user_id FROM main WHERE user_id = ?", (author.id,))
        result = cursor.fetchone()
        if result is None:
           
            sql = "INSERT INTO main(user_id, balance, bank) VALUES (?, ?, ?)"
            val = (author.id, 100, 0)  
            cursor.execute(sql, val)
            db.commit()
      
        cursor.close()
        db.close()

