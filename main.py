import discord
from discord.ext import commands, tasks
from discord.utils import get
import datetime, json, os
from random import randint
#Config.json
with open("config.json","r") as j:
    datos=json.load(j)
    print(datos['versiones']['bot'])

#Token---------------------------
TOKEN = "YourToken"
#--------------------------------

#Funciones requeridas----------------------

#Obtener prefix
def get_prefix(bot,message):
    global prefix
    tipo=str(type(message.guild))
    if tipo=="<class 'NoneType'>":
        prefix=str(randint(1,100000))
        return prefix
    with open("prefixes.json","r") as f:
        prefixes=json.load(f)
    
    #Verificar si el servidor esta en el json
    if str(message.guild.id) in prefixes:
        prefix=prefixes[str(message.guild.id)]
    else: #Si no esta, agregarlo
        prefixes[str(message.guild.id)]=","
        #Guardar cambios
        with open("prefixes.json","w") as f:
            json.dump(prefixes,f,indent=4)
        prefix=prefixes[str(message.guild.id)]
    return prefix

#Verificar si el usuario es el dueño del bot
def is_it_me(ctx):
    return ctx.author.id == INT(IDdelDueño)

#------------------------------------------

#Bot--------------------------------------
intents = discord.Intents.default()  
intents.members = True 
owners = [TuId,IdDelDueño2...]
bot = commands.Bot(command_prefix=get_prefix,owners_id=set(owners), description="Bot de discord", intents = intents)
bot.remove_command('help')
#------------------------------------------

#Eventos----------------------------------

#Cuando se une a un servidor
@bot.event
async def on_guild_join(guild):
    with open('prefixes.json','r') as f:
        prefixes =json.load(f)
    prefixes[str(guild.id)] =","

    with open("prefixes.json","w") as f:
        json.dump(prefixes,f)

#Evento de errores
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error,commands.MissingRequiredArgument): #Si falta un argumento
        await ctx.reply(f"Error encontrado, porfavor revise los argumentos de su mensaje o use {prefix}help.")
    if isinstance(error,commands.MissingPermissions): #Si no tiene permisos
        await ctx.reply(f"Error encontrado, no tienes permisos para usar este comando.")
    if isinstance(error, commands.CommandNotFound): #Si el comando no existe
        await ctx.reply(f"Error encontrado, el comando no existe.")
    if isinstance(error, commands.BotMissingPermissions): #Si el bot no tiene permisos
        await ctx.reply(f"Error encontrado, el bot no tiene permisos para usar este comando.")
        await ctx.reply(f"Los permisos que faltan son: {error.missing_perms}")
    if isinstance(error, commands.ExtensionNotFound): #Si la extension no existe
        await ctx.reply(f"Error encontrado, la extension no existe.")
    if isinstance(error, commands.ExtensionAlreadyLoaded): #Si la extension ya esta cargada
        await ctx.reply(f"Error encontrado, la extension ya esta cargada.")
    if isinstance(error, commands.ExtensionNotLoaded): #Si la extension no esta cargada
        await ctx.reply(f"Error encontrado, la extension no esta cargada.")
    if isinstance(error, commands.DisabledCommand): #Si el comando esta deshabilitado
        await ctx.reply(f"Error encontrado, este comando esta deshabilitado.")
    if isinstance(error, commands.CheckFailure): #Si el check falla
        await ctx.reply(f"Error encontrado, fallo la verificacion.")
    if isinstance(error, commands.NotOwner): #Si el usuario no es el dueño del bot
        await ctx.reply(f"Error encontrado, el usuario no es el dueño del bot.")
    if isinstance(error, commands.PrivateMessageOnly): #Si el comando solo se puede usar en privado
        await ctx.reply(f"Error encontrado, este comando solo se puede usar en privado.")
    if isinstance(error, commands.BadArgument): #Si el comando tiene un argumento invalido
        await ctx.reply(f"Error encontrado, el comando tiene un argumento invalido.")
    await ctx.reply(f"Error: {error}")
    print(f"Error en  **{ctx.guild.name}**:\n```{str(error)}```")


#------------------------------------------

#Comandos---------------------------------


@bot.command()#Ver los servidores del bot
@commands.check(is_it_me)
async def servers(ctx):
    """Muestra todos los servidores en los que esta el bot"""
    await ctx.send(f'Estoy en {len(bot.guilds)} servidores')
    servidores={}
    for guild in bot.guilds:
        await ctx.send(f' - {guild.name}(id: {guild.id})')

#Mod
@bot.command() #Cambiar prefix
@commands.has_permissions(administrator=True)
async def setprefix(ctx,prefix):
    with open("prefixes.json","r") as f:
        prefixes=json.load(f)
    prefixes[str(ctx.guild.id)]=prefix
    with open("prefixes.json","w") as f:
        json.dump(prefixes,f)
    await ctx.send(f"Tu nuevo prefix es: {prefix}")

#General
#Sumas
@bot.command()
async def suma(ctx,n1: int,n2:int):
    resultado = n1+n2
    await ctx.send(f"El resultado es {resultado}")

#Embed de prueba
@bot.command()
async def embed(ctx):
    embed = discord.Embed(title="Titulo uwu", description="Descripcion", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    await ctx.send(embed=embed)

#Dev
#Reiniciar archivo de comandos
@bot.command()
@commands.check(is_it_me)
async def reload(ctx,extension):
        bot.unload_extension(f'comandos.{extension}')
        bot.load_extension(f'comandos.{extension}')
        await ctx.send(f"La extencion {extension} se recargo correctamente")
        print(f'Descarga y carga de {extension}')

#Cargar archivo de comandos
@bot.command()
@commands.check(is_it_me)
async def load(ctx,extension):
    bot.load_extension(f'comandos.{extension}')
    print(f'Se ha cargado: {extension}')
    await ctx.send(f'Se ha cargado: {extension} correctamente')

#Descargar archivo de comandos
@bot.command()
@commands.check(is_it_me)
async def unload(ctx,extension):
    bot.unload_extension(f'comandos.{extension}')
    print(f'unloaded {extension}')
    await ctx.send(f'unloaded {extension}')

#------------------------------------------------------------------------------

#Eventos del bot---------------------------
@tasks.loop(seconds=10)
async def my_background_task():
    actividad=randint(1,3)
    if actividad==1: #Mostrar version del bot
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=(f"versión: {datos['versiones']['bot']}")))
    elif actividad==2: #Mostrar cantidad de servidores
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=(f"{len(bot.guilds)} servidores")))
    elif actividad==3: #Mostrar creador del bot
        await(bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,name='Creador: ✨KikeRex✨')))

@bot.event
async def on_ready():
    print(f"Bot iniciado correctamente como {bot.user}")
    if not my_background_task.is_running():
        my_background_task.start()

#------------------------------------------

#Cargar archivos de comandos---------------------------
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

#------------------------------------------

#Iniciar bot---------------------------------
bot.run(TOKEN)
#--------------------------------------------