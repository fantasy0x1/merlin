from discord.ext import commands
from rich import print

class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[+] [bold blue]{self.__class__.__name__}[/bold blue] module is ready.')

    @commands.command()
    async def ping(self, ctx):
        """Check the bot latency"""
        await ctx.send(f'Pong! {round(self.bot.latency * 1000)}ms')

async def setup(bot):
    await bot.add_cog(Debug(bot))

