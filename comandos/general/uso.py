import discord
import asyncio
import psutil
from discord.ext import commands

class uso(commands.Cog):
    def __init__(self, bot):
        self.bot= bot

    @commands.command()
    async def usocpu(self,ctx):
        print('The CPU usage is: ', psutil.cpu_percent(4)) 
        print('RAM memory % used:', psutil.virtual_memory()[2])
        


def setup(bot):
    bot.add_cog(uso(bot))