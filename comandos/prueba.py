import discord
import asyncio
from discord.ext import commands

class TestCog(commands.Cog):
    def __init__(self, bot):
        self.bot= bot
    @commands.command()
    async def ping(self, ctx):
        latency = self.bot.latency
        trueLatency = latency * 1000
        await ctx.send(f'It takes me {round(trueLatency)} milliseconds to respond.')



    # @commands.Cog.listener()
    # async def on_message(self,message):
    #     print(f"{message.author} ha dicho {message.content}")


def setup(bot):
    bot.add_cog(TestCog(bot))