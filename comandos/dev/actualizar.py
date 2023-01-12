import discord
import asyncio
from discord.ext import commands

class a(commands.Cog):
    def __init__(self, bot):
        self.bot= bot

    @commands.command()
    async def est(self,ctx):
        await ctx.send("Comando en desarrollo")
        #channel = self.bot.get_channel(839211378774638622)
        #await channel.send('holaaa')
        #enviar id del canal
        await ctx.send(f'{ctx.channel.id}')
        


async def setup(bot):
    await bot.add_cog(a(bot))