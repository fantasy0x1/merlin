import discord
from discord.ext import commands
from assets.emojis import emojis
from rich import print
import requests
import os
from core import embeds
from dotenv import load_dotenv

load_dotenv()

GITHUB_ACCESS_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN')

def repos(keyword: str) -> str:
    url = f"https://api.github.com/search/repositories?q={keyword}&order=desc&per_page=10"
    res = requests.get(url)

    if res.status_code == 200:
        data = res.json()
        repo_names = [f"{emojis['white_dot']} {repo['owner']['login']}/{repo['name']}" for repo in data["items"]]
        return repo_names
    else:
        return None

def users(keyword: str) -> str:
    url = f"https://api.github.com/search/users?q={keyword}&per_page=10"
    res = requests.get(url)

    if res.status_code == 200:
        data = res.json()
        users = [f"{emojis['white_dot']} {user['login']}" for user in data["items"]]
        return users
    else: 
        return None

def view(owner, repo_name, path=None):
    base_url = f"https://api.github.com/repos/{owner}/{repo_name}/contents"
    url = base_url if path is None else f"{base_url}/{path}"
    res = requests.get(url)

    if res.status_code == 200:
        data = res.json()
        contents = []
        if path:
            if isinstance(data, dict):
                _, ext = os.path.splitext(data['name'])
                content_res = requests.get(data['download_url'])
                if content_res.status_code == 200:
                    content = content_res.content.decode()
                    contents.append({
                        'name': data['name'],
                        'ext': ext,
                        'content': content
                    })
            else:
                for file in data:
                    _, ext = os.path.splitext(file['name'])
                    content_res = requests.get(file['download_url'])
                    if content_res.status_code == 200:
                        content = content_res.content.decode()
                        contents.append({
                            'name': file['name'],
                            'ext': ext,
                            'content': content
                        })
            return contents
        else:
            contents = [f"{emojis['white_dot']} {file['path']}" for file in data]
            return contents
    else:
        return None

def search_code(keyword: str) -> str:
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    gitbook_url = "https://book.hacktricks.xyz/"
    url = f"https://api.github.com/search/code?q={keyword}+in:file+language:markdown+repo:carlospolop/hacktricks"
    res = requests.get(url, headers=headers)

    if res.status_code == 200:
        data = res.json()
        if data["total_count"] > 0:
            items = data["items"]
            names = []
            paths = []

            for item in items:
                name = item["name"]
                path = item["path"]

                if name == "README.md":
                    path_parts = path.split("/")
                    title = path_parts[-2]
                    path = path.rsplit("/", 1)[0]
                else:
                    title = name.rsplit(".", 1)[0].strip()
                    path = path.rsplit(".", 1)[0]

                if "SUMMARY" in title or "SUMMARY" in path:
                    continue

                title = title.replace("-", " ")
                title = title.title()

                names.append(title)
                paths.append(path)

            paths_w = [f"{gitbook_url}{path}" for path in paths]

            print(names, paths_w)
            return names, paths_w
        else:
            print("No match found.")
    else:
        print("ERROR:" + str(res.status_code))


class Git(commands.Cog):
    """A collection of Github utilities."""

    def __init__(self, bot):
        self.bot = bot
 
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'[+] [bold blue]{self.__class__.__name__}[/bold blue] module is ready.')

    @commands.command(name='hacktricks', aliases=['ht'])
    async def hacktricks(self, ctx, keyword: str, user: discord.Member = None):
        """This command will search for code in Hacktricks repository."""
        user = ctx.message.author
        userAvatar = user.avatar
        names, gitbook_urls = search_code(keyword)  # Renomeei a variável para gitbook_urls

        if names and gitbook_urls:
            embed = discord.Embed(color=0xffffff)
            for name, url in zip(names, gitbook_urls):
                embed.add_field(name=f"{emojis['hacktricks']} Page: {name}", value=f"\n {url}", inline=False)
                # embed.add_field(name=url, value="", inline=False)
            embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=userAvatar)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(color=0xff0000)
            embed.add_field(name=f"{emojis['tick_red']} No contents found for keyword: {keyword}", value="")
            await ctx.send(embed=embed)


    @commands.group(invoke_without_command=True)
    async def git(self, ctx):
        """Some git utils"""
        await ctx.send(f"(cmd: `git`) missing argument\nusage: `{ctx.prefix}git <repos/users>`  ")


    @git.command(name='repos')
    async def repos(self, ctx, keyword, user: discord.Member = None):
        """This command will search for Github repositories."""
        user = ctx.message.author
        userAvatar = user.avatar
        repo_names = repos(keyword)
        
        if repo_names:
            embed=discord.Embed(color=0xffffff)
            embed.add_field(name=emojis['git_icon'] + "  Repositories found:", value="\n".join(repo_names), inline=False)
            embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=userAvatar)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(color=0xff0000)
            embed.add_field(name=f"{emojis['tick_red']} No repositories found for keyword: {keyword}", value="")
            await ctx.send(embed=embed)

    @git.command(name='users')
    async def users(self, ctx, keyword, user: discord.Member = None):
        """This command will search for Github users."""
        user  = ctx.message.author
        userAvatar = user.avatar
        users_list = users(keyword)
        if users_list:
            embed=discord.Embed(color=0xffffff)
            embed.add_field(name=emojis['git_icon'] + "  Users found:", value="\n".join(users_list), inline=False)
            embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=userAvatar)
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=embeds.std("err", f"No users found for keyword: `{keyword}`", ctx.message))

    @git.command(name='view') 
    async def view(self, ctx, keyword, filename=None, user: discord.Member = None):
        """This command will show the contents of a repository"""
        user  = ctx.message.author
        userAvatar = user.avatar

        if "/" not in keyword:
            await ctx.send(embed=embeds.std("err", f"You need to pass a valid repository keyword in the format `owner/repo_name`.", ctx.message))
            return

        owner, repo_name = keyword.split('/')
        file_contents = view(owner, repo_name, filename)

        if filename:
            if not file_contents:
                await ctx.send(embed=embeds.std("err", f"No contents found for keyword {filename}.", ctx.message))
                return
            else:
                for file in file_contents:
                    header = f"{emojis['git_icon']} **{file['name']}**\n```{file['ext'][1:]}\n"
                    footer = "\n```"
                    contents = file['content']
                    messages = [header + contents[i:i+1900] + footer for i in range(0, len(contents), 1800)]
                    for message in messages:
                        await ctx.send(message)
        if file_contents:
            embed=discord.Embed(color=0xffffff)
            embed.add_field(name=emojis['git_icon'] + "  Contents found:", value="\n".join(file_contents), inline=False)
            embed.set_footer(text="Requested by: " + ctx.author.name, icon_url=userAvatar)
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=embeds.std("err", f"No repositories found for keyword: `{keyword}`", ctx.message))



async def setup(bot):
    await bot.add_cog(Git(bot))
