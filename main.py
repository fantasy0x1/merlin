import asyncio
import os 
import discord
from dotenv import load_dotenv
from discord.ext import commands
from commands import debug, stringfy, operators, info, admin
from config.database import create_tables
from cogwatch import watch
from rich import print

intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='.', intents=intents)

create_tables()
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
OWNER_ID = int(os.getenv('OWNER_ID'))

class MerlinBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='.', intents=intents, help_command=commands.DefaultHelpCommand())
    
    @watch(path='commands', preload=True, debug=True, default_logger=True, colors=True)
    async def on_ready(self):
        print('[bold red][+] Bot ready. [/bold red]')

    async def on_message(self, message):
        if message.author.bot:
            return

        await self.process_commands(message)

async def main():
    client = MerlinBot()
    await client.start(TOKEN)

if __name__ == '__main__':
    asyncio.run(main())
