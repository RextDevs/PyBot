import discord,json
import asyncio
from discord.ext import commands

class TestCog(commands.Cog):
    def __init__(self, bot):
        self.bot= bot
    @commands.command()
    @commands.is_owner()
    async def ping(self, ctx):
        latency = self.bot.latency
        trueLatency = latency * 1000
        await ctx.send(f'It takes me {round(trueLatency)} milliseconds to respond.')

async def setup(bot):
    await bot.add_cog(TestCog(bot))