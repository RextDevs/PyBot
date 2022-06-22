import time
import os
import discord
from discord.ext import commands
from discord.utils import get
import requests, json
from deep_translator import GoogleTranslator

class traductor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def traducir(self,ctx):
        languajes=['es','en','otros(aun no definidos)']
        with open("config.json","r") as j:
            versiones=json.load(j)
        await ctx.send(f"Este traductor esta en fase beta\n> version {versiones['versiones']['traductor']}")
        await ctx.send("Ingresa lo que desea traducir: `Solo español a ingles disponible actualmente`")
        def check(m):
            return m.author.id == ctx.author.id
        message = await self.bot.wait_for('message',check=check)
        
        textblob=GoogleTranslator(source='es',target='en')
        explanation=textblob.translate(message.content)
        await ctx.send(explanation)
def setup(bot):
    bot.add_cog(traductor(bot))