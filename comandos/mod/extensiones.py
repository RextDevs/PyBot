import time
import os
import discord
from discord.ext import commands
from discord.utils import get
from datetime import datetime
import requests, json
from random import randint


class loads(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def preload(self,ctx,extension):
            await self.bot.unload_extension(f'comandos.{extension}')
            await self.bot.load_extension(f'comandos.{extension}')
            print(f'unloaded and loaded {extension}')

async def setup(bot):
	await bot.add_cog(loads(bot))