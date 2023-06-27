from discord.ext import commands
from assets.emojis import emojis
from rich import print

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[+] [bold blue]{self.__class__.__name__}[/bold blue] module is ready.')

    @commands.command()
    async def master(self, ctx):
        """nyaaah uwu"""
        await ctx.send(f"ayaaaaaa, i luv **my master** {ctx.message.author.mention}")
        await ctx.send("https://i.giphy.com/media/SSPW60F2Uul8OyRvQ0/giphy.webp")


async def setup(bot):
    await bot.add_cog(Fun(bot))