import discord
from discord.ext import commands
from core import embeds
from assets.emojis import emojis
from config.database import create_tables, insert_operator, delete_operator, is_operator, get_operators
from rich import print
from main import OWNER_ID

class Operators(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[+] [bold blue]{self.__class__.__name__}[/bold blue] module is ready.')

    @commands.group(invoke_without_command=True)
    async def op(self, ctx, user: discord.Member = None):
        """Operators management"""
        if not ctx.invoked_subcommand:
            operators = get_operators(ctx.guild)
            operator_mentions = []

            if not operators:
                embed=discord.Embed(description="" + emojis['tick_red'] + " **| No operators found on this server.**", color=0xff0000)
                embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=ctx.message.author.avatar)  
                await ctx.send(embed=embed)
            else:
                for operator in operators:
                    member = discord.utils.get(ctx.guild.members, id=int(operator[0]))
                    if member:
                        operator_mentions.append(member.mention)
                    else:
                        operator_mentions.append(f"unknown user with ID {operator[0]}")

                embed=discord.Embed(color=0x6e6d6d)
                if operator_mentions:
                    operator_mentions[0] = emojis['white_dot'] + '' + operator_mentions[0]  # Adicionar emoji ao primeiro operador
                embed.add_field(name="" + emojis['ops_icon'] + " Bot Operators", value=f"\n {emojis['white_dot']}".join(operator_mentions) + "\n", inline=False)
                await ctx.send(embed=embed)

    @op.command(name='set', aliases=["add"])
    async def set(self, ctx, user: commands.MemberConverter, member: discord.Member = None):
        """Add a member to operators list"""
        if is_operator(ctx.guild.id, ctx.author.id):
            insert_operator(ctx.guild.id, user.id)
            await ctx.send(embed=embeds.std("out", f"User {user.mention} added to operators list!", ctx.message))
        else:
            await ctx.send(embed=embeds.std("err", f"User {ctx.author.mention} is not an operator.", ctx.message))
    
    @op.command(name='rm', aliases=["remove", "del", "delete"])
    async def rm(self, ctx, user: commands.MemberConverter):
        """Remove a member from operators list"""
        if is_operator(ctx.guild.id, ctx.author.id):
            delete_operator(ctx.guild.id, user.id)
            await ctx.send(embed=embeds.std("out", f"User {user.mention} is no longer an operator!", ctx.message))
        else:
            await ctx.send(embed=embeds.std("err", f"User {ctx.author.mention} is not an operator.", ctx.message))

async def setup(bot):
    await bot.add_cog(Operators(bot))
