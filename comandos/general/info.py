import discord
from discord.ext import commands
from discord.utils import get
import datetime
from random import randint
class infosrv(commands.Cog):
    def __init__(self, bot):
        self.bot= bot
    @commands.command()
    async def info(self,ctx):
        embed = discord.Embed(title=f"{ctx.guild.name}", description="A", timestamp=datetime.datetime.utcnow(), color=discord.Color.dark_blue())
        embed.add_field(name="Servidor creado el:", value=f"{ctx.guild.created_at}")
        embed.add_field(name="Owner: ", value=f"{ctx.guild.owner}")
        embed.add_field(name="Region", value=f"{ctx.guild.region}")
        embed.add_field(name="ID", value=f"{ctx.guild.id}")
        embed.add_field(name="Miembros", value=f"{ctx.guild.member_count}")
        embed.add_field(name="Roles", value=f"{len(ctx.guild.roles)}")
        embed.add_field(name="Canales", value=f"{len(ctx.guild.channels)}")
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(infosrv(bot))