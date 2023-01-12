
import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get
import datetime
import requests, json
from random import randint

class animales(commands.Cog):
    def __init__(self, bot):
        self.bot= bot
        
    @app_commands.command(name="dog", description="Muestra una imagen de un perro")
    @commands.bot_has_permissions(embed_links=True)
    @app_commands.describe(raza="Raza del perro, si no se especifica, se muestra una imagen aleatoria")
    @app_commands.choices(raza=[
        discord.app_commands.Choice(name="random", value="random"),
        discord.app_commands.Choice(name="list", value="list"),
        discord.app_commands.Choice(name="african", value="african"),
        discord.app_commands.Choice(name="australian", value="australian"),
        discord.app_commands.Choice(name="bouvier", value="bouvier"),
        discord.app_commands.Choice(name="boxer", value="boxer"),
        discord.app_commands.Choice(name="bulldog", value="bulldog"),
        discord.app_commands.Choice(name="chihuahua", value="chihuahua"),
        discord.app_commands.Choice(name="corgi", value="corgi"),
        discord.app_commands.Choice(name="husky", value="husky"),
        discord.app_commands.Choice(name="labrador", value="labrador"),
        discord.app_commands.Choice(name="pug", value="pug"),
        discord.app_commands.Choice(name="schnauzer", value="schnauzer"),
        discord.app_commands.Choice(name="shiba", value="shiba"),
        discord.app_commands.Choice(name="terrier", value="terrier"),
        
    ])
    async def dog(self,interaction: discord.Interaction, raza: discord.app_commands.Choice[str]=None):
        await interaction.response.defer()
        #Leer jsons
        with open("config.json","r") as j:
            versiones=json.load(j)
        embed = discord.Embed(title=f"Fotos de perros", description=f"versión: {versiones['versiones']['animales']['dog']}", timestamp=datetime.datetime.utcnow(), color=discord.Color.random())
        
        #si no se especifica raza
        if not raza:
            url="https://dog.ceo/api/breeds/image/random"
            peticion = requests.get(url)
            respuesta = json.loads(peticion.content)
            embed.set_image(url=respuesta['message'])
        #Si llama a list
        elif raza.name=="list":
            lista=['affenpinscher', 'african', 'airedale', 'akita', 'appenzeller', 'australian', 'basenji', 'beagle', 'bluetick', 'borzoi', 'bouvier', 'boxer', 'brabancon', 'briard', 'buhund', 'bulldog', 'bullterrier', 'cattledog', 'chihuahua', 'chow', 'clumber', 'cockapoo', 'collie', 'coonhound', 'corgi', 'cotondetulear', 'dachshund', 'dalmatian', 'dane', 'deerhound', 'dhole', 'dingo', 'doberman', 'elkhound', 'entlebucher', 'eskimo', 'finnish', 'frise', 'germanshepherd', 'greyhound', 'groenendael', 'havanese', 'hound', 'husky', 'keeshond', 'kelpie', 'komondor', 'kuvasz', 'labradoodle', 'labrador', 'leonberg', 'lhasa', 'malamute', 'malinois', 'maltese', 'mastiff', 'mexicanhairless', 'mix', 'mountain', 'newfoundland', 'otterhound', 'ovcharka', 'papillon', 'pekinese', 'pembroke', 'pinscher', 'pitbull', 'pointer', 'pomeranian', 'poodle', 'pug', 'puggle', 'pyrenees', 'redbone', 'retriever', 'ridgeback', 'rottweiler', 'saluki', 'samoyed', 'schipperke', 'schnauzer', 'segugio', 'setter', 'sharpei', 'sheepdog', 'shiba', 'shihtzu', 'spaniel', 'spitz', 'springer', 'stbernard', 'terrier', 'tervuren', 'vizsla', 'waterdog', 'weimaraner', 'whippet', 'wolfhound']
            url='https://dog.ceo/api/breeds/list/all'
            peticion = requests.get(url)
            respuesta = json.loads(peticion.content)
            razas=""
            for i in respuesta['message']:
                razas=razas+str(i)+"\n"
            embed.add_field(name='Razas:', value=f"{razas}") 
        #Si se especifica random
        elif raza.name=="random":
            url="https://dog.ceo/api/breeds/image/random"
            peticion = requests.get(url)
            respuesta = json.loads(peticion.content)
            embed.set_image(url=respuesta['message'])
        #Si se especifica una raza
        else:
            url=f'https://dog.ceo/api/breed/{raza.name}/images/random'
            peticion = requests.get(url)
            respuesta = json.loads(peticion.content)
            embed.set_image(url=respuesta['message'])
        await interaction.followup.send(embed=embed)

    @app_commands.command(name="cat", description="Muestra una foto de un gato")
    @commands.bot_has_permissions(embed_links=True)
    async def cat(self, interaction: discord.Interaction):
        await interaction.response.defer()
        with open("config.json","r") as j:
            versiones=json.load(j)
        url='https://cataas.com/cat?json=true'
        peticion = requests.get(url)
        respuesta = json.loads(peticion.content)
        urls='https://cataas.com'+str(respuesta['url'])
        embed = discord.Embed(title=f"Fotos de gatos", description=f"versión: {versiones['versiones']['animales']['cat']}", timestamp=datetime.datetime.utcnow(), color=discord.Color.random())
        embed.set_image(url=str(urls))
        await interaction.followup.send(embed=embed)
    @app_commands.command(name="capybara", description="Muestra una foto de una capibara")
    @commands.bot_has_permissions(embed_links=True)
    async def capybara(self, interaction: discord.Interaction):
        with open("config.json","r") as j:
            versiones=json.load(j)
        url='https://api.capybara-api.xyz/v1/image/random'
        peticion = requests.get(url)
        respuesta = json.loads(peticion.content)
        embed = discord.Embed(title=f"Fotos de capibaras", description=f"versión: {versiones['versiones']['animales']['capybara']}", timestamp=datetime.datetime.utcnow(), color=discord.Color.random())
        embed.set_image(url=str(respuesta['image_urls']['original']))
        await interaction.followup.send(embed=embed)
                
async def setup(bot):
    await bot.add_cog(animales(bot))