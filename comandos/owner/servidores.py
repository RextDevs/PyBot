import discord
import asyncio
from discord.ext import commands

class Servidoresc(commands.Cog):
    def __init__(self, bot):
        self.bot= bot

    @commands.command()
    @commands.is_owner()
    async def serversowner(self,ctx):
        await ctx.send("El bot esta en los siguientes servidores:")
        embed = discord.Embed(title="Servidores", description="", color=0x00ff00)
        for guild in self.bot.guilds:
            embed.add_field(name=guild.name, value=f"**id**: {guild.id}\n**owner**{guild.owner}", inline=False)
        await ctx.send(embed=embed)
        return


async def setup(bot):
    await bot.add_cog(Servidoresc(bot))