import time
import os
import discord
from discord.ext import commands
from discord.utils import get
import datetime
import requests, json
from random import randint

class animales(commands.Cog):
    def __init__(self, bot):
        self.bot= bot
        
    @commands.command()
    async def dog(self,ctx, raza:str=None):
        with open("config.json","r") as j:
            versiones=json.load(j)
        with open("prefixes.json","r") as f:
            prefixes=json.load(f)
        prefix=prefixes[str(ctx.guild.id)]
        embed = discord.Embed(title=f"Fotos de perros", description=f"versión: {versiones['versiones']['animales']['dog']}", timestamp=datetime.datetime.utcnow(), color=discord.Color.random())


        if not raza:
            url="https://dog.ceo/api/breeds/image/random"
            peticion = requests.get(url)
            respuesta = json.loads(peticion.content)
            embed.set_image(url=respuesta['message'])



        elif raza=="help":
            embed.add_field(name="Comandos disponibles", value=f"`{prefix}dog ` --> `Muestra una imagen aleatoria`\n`{prefix}dog [raza]` -->Muestra una imagen aleatoria de dicha raza\n{prefix}dog list -->muestra las razas disponibles")

        elif raza=="list":
            url='https://dog.ceo/api/breeds/list/all'
            peticion = requests.get(url)
            respuesta = json.loads(peticion.content)
            razas=""
            for i in respuesta['message']:
                razas=razas+str(i)+"\n"
            
            embed.add_field(name='Razas:', value=f"{razas}") 
        else:
            url='https://dog.ceo/api/breeds/list/all'
            peticion = requests.get(url)
            respuesta = json.loads(peticion.content)
            razavalida=False
            for i in respuesta['message']:
                if raza == i:
                    razavalida=True
            if razavalida==True:
                url=f'https://dog.ceo/api/breed/{raza}/images/random'
                peticion = requests.get(url)
                respuesta = json.loads(peticion.content)
                embed.set_image(url=respuesta['message'])
            else:
                await ctx.send("Raza no encontrada:c")
                return;
        await ctx.send(embed=embed)



    @commands.command()
    async def cat(self, ctx):
        with open("config.json","r") as j:
            versiones=json.load(j)
        url='https://cataas.com/cat?json=true'
        peticion = requests.get(url)
        respuesta = json.loads(peticion.content)
        urls='https://cataas.com'+str(respuesta['url'])
        embed = discord.Embed(title=f"Fotos de gatos", description=f"versión: {versiones['versiones']['animales']['cat']}", timestamp=datetime.datetime.utcnow(), color=discord.Color.random())
        embed.set_image(url=str(urls))
        await ctx.send(embed=embed)

                
def setup(bot):
    bot.add_cog(animales(bot))