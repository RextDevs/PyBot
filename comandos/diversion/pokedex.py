import time
import os
import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get
import datetime
import requests, json
from random import randint

def versiones():
    with open("config.json","r") as j:
        datos=json.load(j)
        return datos

class pokedex(commands.Cog):
    def __init__(self, bot):
        self.bot= bot

    @app_commands.command(name="pokedex", description="Muestra la información de un pokemon")
    #@commands.command() #Comentado por futura eliminacion
    @commands.bot_has_permissions(embed_links=True)
    async def pokedex(self, interaction:discord.Interaction, codigo: str) -> None:
        version=versiones()
        if not codigo:
            await interaction.response.send_message("Pokemon no encontrado, enseñando uno random")
            codigo=randint(1,850)
        url = 'http://pokeapi.co/api/v2/pokemon/'
        peticion = requests.get(url+str(codigo))
        #no encontrado
        if str(peticion)=="<Response [404]>":
            await interaction.response.send_message(str(peticion))
            await interaction.response.send_message("Pokemon no encontrado, enseñando uno random")
            codigo=randint(1,850)
            peticion = requests.get(url+str(codigo))
        respuesta = json.loads(peticion.content)
        embed = discord.Embed(title=f"POKEDEX", description=f"Versión {version['versiones']['pokedex']}", timestamp=datetime.datetime.utcnow(), color=discord.Color.random())
        embed.add_field(name='Nombre', value=f"{respuesta['name']}") 
        embed.add_field(name='ID', value=f"{respuesta['id']}")
        embed.add_field(name='Peso', value=f"{respuesta['height']} Kg")
        #Tipo 
        tipos=""
        for tipo in respuesta['types']:
            tipos=tipos+str(f"{tipo['slot']} tipo: {tipo['type']['name']}\n")
        embed.add_field(name='Tipo', value=f"{tipos}")
        #stats
        stats=""
        for i in respuesta['stats']:
            stats= str(stats)+str(f"{i['stat']['name']}: {i['base_stat']}")+str("\n")
        embed.add_field(name='Estadisticas base', value=f"{stats}")
        #en juegos:
        juegoss=""
        for juegos in respuesta["game_indices"]:
            juegoss=juegoss+ str(f"{juegos['version']['name']}, ")
        embed.add_field(name='Juegos:"', value=f"{juegoss}")
        embed.set_thumbnail(url=f"{respuesta['sprites']['front_default']}")
        await interaction.response.send_message(embed=embed)
        #await ctx.send(respuesta['sprites']['other']['official-artwork']['front_default'])

async def setup(bot):
    await bot.add_cog(pokedex(bot))