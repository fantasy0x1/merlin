import discord
from assets.emojis import emojis

def std(desc, msg, ctx):
    user_avatar = ctx.author.avatar

    embed_config = {
        "out": {"description": f"{emojis['tick_green']} **| {msg} **", "color": 0x00ff1e},
        "err": {"description": f"{emojis['tick_red']} **| {msg} **", "color": 0xff0000}
    }
    
    embed = discord.Embed(**embed_config[desc])
    embed.set_footer(text=f"Requested by: {ctx.author}", icon_url=user_avatar)

    return embed