import time
import os
import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get
import requests, json
from deep_translator import GoogleTranslator

class traductor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="traductor", description="Traductor")
    async def traducir(self,interaction: discord.Interaction, lenguaje1:str, lenguaje2:str,*,texto:str):
        languajes=['es','en','otros(aun no definidos)']
        with open("config.json","r") as j:
            versiones=json.load(j)
        await interaction.response.send_message(f"Este traductor esta en fase beta\n> version {versiones['versiones']['traductor']}")
        textblob=GoogleTranslator(source='es',target='en')
        explanation=textblob.translate(texto)
        await interaction.response.edit_message(explanation)
async def setup(bot):
    await bot.add_cog(traductor(bot))