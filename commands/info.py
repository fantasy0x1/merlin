import discord
from discord.ext import commands
from assets.emojis import emojis
from rich import print

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[+] [bold blue]{self.__class__.__name__}[/bold blue] module is ready.')

    @commands.command(name='avatar', aliases=["av"], help='Get member avatar')
    async def avatar(self, ctx, *, member: discord.Member = None):
        member = member or ctx.author
        avatar_url = member.avatar.url
        embed = discord.Embed(
            description=f"**{emojis['blue_star']}  {member.name}\'s Avatar**",
            color=0x0910db
        )
        embed.set_image(url=avatar_url)
        embed.set_footer(
            text=f"Requested by: {ctx.author.name}",
            icon_url=avatar_url
        )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name='serverinfo', aliases=['guildinfo', 'srvinfo'], help='Get server info')
    async def serverinfo(self, ctx):
        guild = ctx.guild
        members = guild.member_count
        bots = len([m for m in guild.members if m.bot])
        humans = members - bots
        online = len([m for m in guild.members if m.status != discord.Status.offline])

        about_section = f"{emojis['about']} **About**\n‎ ‎ • Name: {guild.name}\n‎ ‎ • ID: {guild.id}\n‎ ‎ • Owner: {ctx.author.mention}\n‎ ‎ • Shard: {guild.shard_id}"
        users_section = f"{emojis['users']} **Users**\n‎ ‎ • Total Members: {members} (Online: {online})\n‎ ‎ • Humans: {humans}\n‎ ‎ • Bots: {bots}"
        channels_section = f"{emojis['channels']} **Channels**\n‎ ‎ • Text: {len(guild.text_channels)}\n‎ ‎ • Voice: {len(guild.voice_channels)}\n‎ ‎ • Categories: {len(guild.categories)}"
        created_at = guild.created_at.strftime("%b %d, %Y, %T")
        joined_at = ctx.author.joined_at.strftime("%b %d, %Y, %T")

        embed = discord.Embed(title="Server Information", color=0xffffff)
        embed.set_thumbnail(url=guild.icon.url)
        embed.add_field(name="", value=about_section, inline=False)
        embed.add_field(name="", value=users_section, inline=False)
        embed.add_field(name="", value=channels_section, inline=False)
        embed.add_field(name=f"{emojis['clock']} Created at", value=created_at, inline=True)
        embed.add_field(name=f"{emojis['clock']} Joined at", value=joined_at, inline=True)
        embed.set_footer(text=f"Requested by: {ctx.author.name}", icon_url=ctx.author.avatar.url)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Info(bot))