
import discord
from discord.ext import commands
from discord.utils import get
import datetime, os
import requests, json
from random import randint
from deep_translator import GoogleTranslator
from discord import app_commands
from dotenv import load_dotenv

#Token de la nasa
load_dotenv()
key = os.getenv("NASA_API_KEY")
api=f"?api_key={key}"

class nasa(commands.Cog):
    def __init__(self, bot):
        self.bot= bot

    @app_commands.command(name="nasa", description="Imagen del dia por la nasa")
    @commands.bot_has_permissions(embed_links=True)
    async def fotonasa(self, interaction: discord.Interaction):
        await interaction.response.defer()
        #Leer jsons
        with open("config.json","r") as j:
            versiones=json.load(j)

        #Peticion
        url="https://api.nasa.gov/planetary/apod"+str(api)
        peticion = requests.get(url)
        respuesta = json.loads(peticion.content)

        textblob=GoogleTranslator(source='en',target='es')
        explanation=textblob.translate(respuesta['explanation'])
        title = textblob.translate(respuesta['title'])
        embed = discord.Embed(title=f"Imagen del dia **'{title}'**", description=f"Imagen del dia por la nasa\nVersión {versiones['versiones']['nasa']}", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
        embed.add_field(name='Descripcion', value=explanation[:1000])
        embed.set_image(url=respuesta['hdurl'])
        embed.set_footer(text=f"Por {respuesta['copyright']}, el {respuesta['date']}")
        await interaction.followup.send(embed=embed)
    
async def setup(bot):
    await bot.add_cog(nasa(bot))