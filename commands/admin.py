import discord
from discord.ext import commands
from rich import print
from core import embeds
from core.utils import cleanup_code
from config.database import is_operator
import subprocess
import io
import contextlib

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[+] [bold blue]{self.__class__.__name__}[/bold blue] module is ready.')

    @commands.command()
    async def clear(self, ctx, amount=10):
        """Clears the specified amount of messages from the current channel"""
        if is_operator(ctx.guild.id, ctx.author.id):
            await ctx.channel.purge(limit=amount)
            await ctx.send(embed=embeds.std("out", f"{str(amount)} messages cleared", ctx.message))
        else:
            await ctx.send(embed=embeds.std("err", f"User {ctx.author.mention} is not an operator.", ctx.message))

    @commands.command()
    @commands.is_owner()
    async def eval(self, ctx, *, code: str):
        """Not secure command"""

        code = cleanup_code(code)

        try:
            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                exec(code)

            output = stdout.getvalue()

            if output:
                await ctx.send(f"```\n{output}```")
            else:
                await ctx.send("```\nNone```")
        except Exception as e:
            await ctx.send(f"```\n{type(e).__name__}: {e}```")

    @commands.command()
    @commands.is_owner()
    async def sh(self, ctx, *, code):
        """Not secure command"""
        try:
            result = subprocess.check_output(code, shell=True, universal_newlines=True)
            await ctx.send(f"```\n{result}```")
        except subprocess.CalledProcessError as e:
            await ctx.send(f"```\n{e.output}```")
        except Exception as e:
            await ctx.send(f"```\n{type(e).__name__}: {e}```")

async def setup(bot):
    await bot.add_cog(Admin(bot))