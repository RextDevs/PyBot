#https://api.nasa.gov/planetary/apod?api_key=iWvPyqFGEu99AcbKIwZSQh1o0SRRj0x2RT01aVMb
import time
import os
import discord
from discord.ext import commands
from discord.utils import get
import datetime
import requests, json
from random import randint

from deep_translator import GoogleTranslator
api="?api_key=iWvPyqFGEu99AcbKIwZSQh1o0SRRj0x2RT01aVMb"
class nasa(commands.Cog):
    def __init__(self, bot):
        self.bot= bot
    

    @commands.command()
    async def fotonasa(self, ctx):
        with open("config.json","r") as j:
            versiones=json.load(j)

        url="https://api.nasa.gov/planetary/apod"+str(api)
        peticion = requests.get(url)
        respuesta = json.loads(peticion.content)

        textblob=GoogleTranslator(source='en',target='es')
        explanation=textblob.translate(respuesta['explanation'])
        #await ctx.send(explanation)
        #await ctx.send("La imagen del dia:")
        #await ctx.send(respuesta['hdurl'])
        '''
        texto=""
        seguir = True
        temp=""
        for i in explanation:
            
            if (str(temp)+str(i)) == "3.":
                seguir = False
            temp=i
            if seguir==True:
                texto=texto+str(i)

        print(texto)
        '''
        embed = discord.Embed(title="Imagen del dia", description=f"Imagen del dia por la nasa\nVersión {versiones['versiones']['nasa']}", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
        embed.add_field(name='Descripcion', value=explanation[:1000])
        embed.set_image(url=respuesta['hdurl'])
        await ctx.send(embed=embed)
    
def setup(bot):
    bot.add_cog(nasa(bot))