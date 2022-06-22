import discord
import asyncio
from discord.ext import commands
import datetime,json

class helpdef(commands.Cog):
    def __init__(self, bot):
        self.bot= bot

    @commands.command()
    async def help(self,ctx):
        with open("config.json","r") as j:
            versiones=json.load(j)
        with open("prefixes.json","r") as f:
            prefixes=json.load(f)
        prefix=prefixes[str(ctx.guild.id)]
        embed=discord.Embed(title=f"Comados", description=f"Prefix: {prefix}\nVersion: {versiones['versiones']['bot']}", timestamp=datetime.datetime.utcnow(), color=discord.Color.dark_blue())
        embed.add_field(name='Dog',value='Una imagen aleatoria de perros\nUsos: dog <module>, use dog help para mas información')
        embed.add_field(name='traducir',value='Traduce un texto')
        embed.add_field(name='pokemon',value='Consultas a una pokedex, funciona tanto con id o nombre de un pokemon')
        await ctx.send(embed=embed)
        await ctx.send("Comando en desarrollo")
        


def setup(bot):
    bot.add_cog(helpdef(bot))