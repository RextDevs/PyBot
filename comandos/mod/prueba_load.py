import time
import os
import discord
from discord.ext import commands
from discord.utils import get
from datetime import datetime
import requests, json
from random import randint

def is_it_me(ctx):
    return ctx.author.id == 612786159306670112

class loads(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.check(is_it_me)
    async def preload(self,ctx,extension):
            self.bot.unload_extension(f'comandos.{extension}')
            self.bot.load_extension(f'comandos.{extension}')
            print(f'unloaded and loaded {extension}')

def setup(bot):
	bot.add_cog(loads(bot))