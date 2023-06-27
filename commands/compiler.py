import os
import discord
import requests
from discord.ext import commands
from assets.emojis import emojis
from rich import print
from dotenv import load_dotenv
from core.utils import cleanup_code

load_dotenv()

RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')

LANGUAGE_MAP = {
    "py": "python3",
    "python": "python3",
}

class Compiler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[+] [bold blue]{self.__class__.__name__}[/bold blue] module is ready.')

    @commands.command(aliases=["run"])
    async def compile(self, ctx, lang: str, *, code):
        """Compiles and runs the given code"""
        code = cleanup_code(code)
        lang = LANGUAGE_MAP.get(lang, lang)
        url = "https://online-code-compiler.p.rapidapi.com/v1/"

        payload = {
            "language": lang,
            "version": "latest",
            "code": code,
            "input": None
        }
        
        headers = {
            "content-type": "application/json",
            "X-RapidAPI-Key": RAPIDAPI_KEY,
            "X-RapidAPI-Host": "online-code-compiler.p.rapidapi.com"
        }

        response = requests.post(url, json=payload, headers=headers)
        result = response.json()
        output = result['output']

        embed = discord.Embed(description=f"**Output**", color=0xffffff)
        embed.add_field(name="", value=f"```{output}```", inline=False)
        embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.message.author.avatar)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Compiler(bot))