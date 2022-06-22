from pickle import FALSE
import time
import os
import discord
from discord.ext import commands, tasks
from discord.utils import get
import datetime
import requests, json
from random import randint
#Config.json
with open("config.json","r") as j:
    datos=json.load(j)
    print(datos['versiones']['bot'])

TOKEN = "YOURTOKEN"
#prefix='p,'
def get_prefix(bot,message):
    global prefix
    tipo=str(type(message.guild))
    if tipo=="<class 'NoneType'>":
        prefix=str(randint(1,100000))
        return prefix
    with open("prefixes.json","r") as f:
        prefixes=json.load(f)
    prefix=prefixes[str(message.guild.id)]
    return prefixes[str(message.guild.id)]


intents = discord.Intents.default()  
intents.members = True 
bot = commands.Bot(command_prefix=get_prefix, description="Es un bot de ayuda uwu", intents = intents)
bot.remove_command('help')

@bot.event
async def on_guild_join(guild):
    with open('prefixes.json','r') as f:
        prefixes =json.load(f)
    prefixes[str(guild.id)] =","

    with open("prefixes.json","w") as f:
        json.dump(prefixes,f)
@bot.command()
async def servers(ctx):
    """Muestra todos los servidores en los que esta el bot"""
    await ctx.send(f'Estoy en {len(bot.guilds)} servidores')
    servidores={}
    for guild in bot.guilds:
        await ctx.send(f' - {guild.name}(id: {guild.id})')

@bot.command()
@commands.has_permissions(administrator=True)
async def setprefix(ctx,prefix):
    with open("prefixes.json","r") as f:
        prefixes=json.load(f)
    prefixes[str(ctx.guild.id)]=prefix
    with open("prefixes.json","w") as f:
        json.dump(prefixes,f)
    await ctx.send(f"Tu nuevo prefix es: {prefix}")



#------------------------------------------------------------------------------
#General
@bot.command()
async def suma(ctx,n1: int,n2:int):
    resultado = n1+n2
    await ctx.send(f"El resultado es {resultado}")

@bot.command()
async def embed(ctx):
    embed = discord.Embed(title="Titulo uwu", description="Descripcion", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    await ctx.send(embed=embed)

def is_it_me(ctx):
    return ctx.author.id == 612786159306670112




@bot.command()
@commands.check(is_it_me)
async def reload(ctx,extension):
        bot.unload_extension(f'comandos.{extension}')
        bot.load_extension(f'comandos.{extension}')
        await ctx.send("La extencion {extension} se recargo correctamente")
        print(f'Descarga y carga de {extension}')
#load
@bot.command()
@commands.check(is_it_me)
async def load(ctx,extension):
    bot.load_extension(f'comandos.{extension}')
    print(f'Se ha cargado: {extension}')
    await ctx.send(f'Se ha cargado: {extension} correctamente')
#unload
@bot.command()
@commands.check(is_it_me)
async def unload(ctx,extension):
    
    bot.unload_extension(f'comandos.{extension}')
    print(f'unloaded {extension}')
    await ctx.send(f'unloaded {extension}')




#events
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error,commands.MissingRequiredArgument):
       await ctx.reply(f"Error Fatal encontrado, porfavor revise los argumentos de su mensaje o use {prefix}help.")
       
    if isinstance(error,commands.MissingPermissions):
       print(error.missing_perms)
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("El comando no existe o esta en mantenimiento")
    if isinstance(error, commands.BotMissingPermissions):
        await ctx.send("No tengo los permisos necesarios")
    if isinstance(error, commands.ExtensionNotFound):
        await ctx.send("La extension no existe")
    
    await ctx.send(f"<**Error Encontrado**> {error}")
    print(f"Error en  **{ctx.guild.name}**:\n```{str(error)}```")
    

@tasks.loop(seconds=10)
async def my_background_task():
    actividad=randint(1,4)
    if actividad==1:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=(f"versión: {datos['versiones']['bot']}")))
    elif actividad==2:
        await bot.change_presence(activity=discord.Game(name='{Servidores} servidores'))
    elif actividad==3:
        await(bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name='Creador: Kikerex')))
    elif actividad==4:
        prefixe=get_prefix
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,name=f',help'))
@bot.event
async def on_ready():
    print("El bot esta en linea")
    my_background_task.start()
    #await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=(f"versión: {datos['versiones']['bot']}")))
   

for filename in os.listdir('./comandos'):
    if filename.endswith(".py"):
        bot.load_extension(f"comandos.{filename[:-3]}")
for filename in os.listdir('./comandos/general'):
    if filename.endswith(".py"):
        bot.load_extension(f"comandos.general.{filename[:-3]}")
for filename in os.listdir('./comandos/mod'):
    if filename.endswith(".py"):
        bot.load_extension(f"comandos.mod.{filename[:-3]}")
for filename in os.listdir('./comandos/musica'):
    if filename.endswith(".py"):
        bot.load_extension(f"comandos.musica.{filename[:-3]}")
for filename in os.listdir('./comandos/diversion'):
    if filename.endswith(".py"):
        bot.load_extension(f"comandos.diversion.{filename[:-3]}")

for filename in os.listdir('./comandos/dev'):
    if filename.endswith(".py"):
        bot.load_extension(f"comandos.dev.{filename[:-3]}")
bot.run(TOKEN)