import discord
import base64, urllib.parse, hashlib
from discord.ext import commands
from assets.emojis import emojis
from rich import print

def encode(type: str, data: str) -> discord.Embed:
    if type in ["base64", "b64"]: 
        encoded_bytes = base64.b64encode(data.encode('utf-8'))
        encoded_data = encoded_bytes.decode('utf-8')
        title = emojis['binary'] + " Base64 Encoder"
    elif type == "url":
        encoded_data = urllib.parse.quote_plus(data, safe=":/?=%")
        title = emojis['binary'] + " URL Encoder"
    elif type == "md5":
        encoded_data = hashlib.md5(data.encode()).hexdigest()
        title = emojis['binary'] + " MD5 Encoder"
    else:
        raise ValueError(f"Invalid encoding type: {type}")

    return discord.Embed(title=title, description=f"```{encoded_data}```", color=0xFFFFFF)

def decode(type: str, data: str) -> discord.Embed:
    if type in ["base64", "b64"]:
        decoded_data = bytes.decode(base64.b64decode(data))
        title = emojis["binary"] + " Base64 Decoder"
    elif type == "url":
        decoded_data = urllib.parse.unquote_plus(data)
        title = emojis["binary"] + " URL Decoder"
    else:
        raise ValueError(f"Unknown type: {type}")
    return discord.Embed(title=title, description=f"```{decoded_data}```", color=0xFFFFFF)

class Stringfy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[+] [bold blue]{self.__class__.__name__}[/bold blue] module is ready.')

    @commands.command()
    async def encode(self, ctx, type, *, data):
        """
        Encode the given data using the specified encoding type.
        """
        await ctx.send(embed=encode(type, data))

    @commands.command()
    async def decode(self, ctx, type, *, data):
        await ctx.send(embed=decode(type, data))

async def setup(bot):
    await bot.add_cog(Stringfy(bot))