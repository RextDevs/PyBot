import time
import os
import discord
from discord.ext import commands
from discord.utils import get
import datetime
import requests, json
from random import randint


class MusicaConect(commands.Cog):
    def __init__(self, bot):
        self.bot= bot
    @commands.command(pass_context = True)
    async def conectar(self,ctx):
        
        if not ctx.message.author.voice.channel:
            await ctx.send("No estas conectado a un canal de voz")
            return
        canal = ctx.message.author.voice.channel
        voz = get(self.bot.voice_clients,guild=ctx.guild)
        if voz and voz.is_connected():
            await voz.move_to(canal)
        else:
            voz = await canal.connect()
    @commands.command(pass_context = True)
    async def desconectar(self,ctx):
        canal =ctx.message.author.voice.channel
        voz = get(self.bot.voice_clients, guild=ctx.guild)
        await voz.disconnect()


def setup(bot):
    bot.add_cog(MusicaConect(bot))