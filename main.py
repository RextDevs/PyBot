import discord
from discord.ext import commands, tasks
from discord import app_commands
from discord.utils import get
import datetime, json, os, asyncio
from dotenv import load_dotenv
from tqdm import tqdm
from random import randint




#Iniciar progreso
#Config.json
with open("config.json","r") as j:
    datos=json.load(j)
    print(datos['versiones']['bot'])

#Token---------------------------
# carga las variables de entorno desde el archivo .env
load_dotenv()

# obtiene la clave de API de la variable de entorno
TOKEN = os.getenv('TOKEN')
CLIENTE = os.getenv('CLIENTE')
#--------------------------------


#Funciones requeridas----------------------

#Obtener prefix
def get_prefix(bot,message):
    tipo=str(type(message.guild)) #Verificar si el mensaje es de un servidor
    if tipo=="<class 'NoneType'>": #Si no es de un servidor, generar un numero random
        return str(randint(1,100000))
    #Cargar json
    with open("prefixes.json","r") as f:
        prefixes=json.load(f)
    #Verificar si el servidor esta en el json
    if str(message.guild.id) in prefixes:
        prefix=prefixes[str(message.guild.id)]
    else: #Si no esta, agregarlo
        prefixes[str(message.guild.id)]="/"
        #Guardar cambios
        with open("prefixes.json","w") as f:
            json.dump(prefixes,f,indent=4)
        prefix=prefixes[str(message.guild.id)]
    return prefix

#Verificar si el usuario es el dueño del bot (En eliminación)
def is_it_me(ctx):
    return ctx.author.id == "YOUR DISCORD ID"

#------------------------------------------

#Inicializar Bot--------------------------------------
intents = discord.Intents.all()
owners = [612786159306670112]
bot = commands.Bot(command_prefix=get_prefix,owner_ids=set(owners), description="Bot oficial de Rext", intents = intents, application_id=str(CLIENTE))
bot.remove_command('help')
#------------------------------------------

#Eventos----------------------------------

#Cuando se une a un servidor
@bot.event
async def on_guild_join(guild):
    print(f"Se unio a {guild.name}")
    with open('prefixes.json','r') as f:
        prefixes =json.load(f)
    prefixes[str(guild.id)] =","
    with open("prefixes.json","w") as f:
        json.dump(prefixes,f)
    #guardar en servidores nombre e id

#Evento de errores
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error,commands.MissingRequiredArgument): #Si falta un argumento
        await ctx.reply(f"Error encontrado, porfavor revise los argumentos de su mensaje o use {get_prefix()}help.")
    if isinstance(error,commands.MissingPermissions): #Si no tiene permisos
        await ctx.reply(f"Error encontrado, no tienes permisos para usar este comando.")
    if isinstance(error, commands.CommandNotFound): #Si el comando no existe
        await ctx.reply(f"Error encontrado, el comando no existe.")
    if isinstance(error, commands.BotMissingPermissions): #Si el bot no tiene permisos
        await ctx.reply(f"Requiero los permisos {error.missing_perms} para ejecutar este comando.")
    if isinstance(error, commands.ExtensionNotFound): #Si la extension no existe
        await ctx.reply(f"Error encontrado, la extension no existe.")
    if isinstance(error, commands.ExtensionAlreadyLoaded): #Si la extension ya esta cargada
        await ctx.reply(f"Error encontrado, la extension ya esta cargada.")
    if isinstance(error, commands.ExtensionNotLoaded): #Si la extension no esta cargada
        await ctx.reply(f"Error encontrado, la extension no esta cargada.")
    if isinstance(error, commands.DisabledCommand): #Si el comando esta deshabilitado
        await ctx.reply(f"Este comando esta en desactivado temporalmente.\nPuedes ir al servidor de soporte para ver mas información.")
    if isinstance(error, commands.CheckFailure): #Si el check falla
        await ctx.reply(f"Error encontrado, fallo la verificacion.")
    if isinstance(error, commands.NotOwner): #Si el usuario no es el dueño del bot
        await ctx.reply(f"Error encontrado, solo el dueño lo puede usar.")
    if isinstance(error, commands.CommandOnCooldown): #Si el comando esta en cooldown
        await ctx.reply(f"Error encontrado, el comando esta en cooldown.")
    if isinstance(error, commands.PrivateMessageOnly): #Si el comando solo se puede usar en privado
        await ctx.reply(f"Error encontrado, este comando solo se puede usar en privado.")
    if isinstance(error, commands.BadArgument): #Si el comando tiene un argumento invalido
        await ctx.reply(f"Error encontrado, el comando tiene un argumento invalido.")
    print(f"Error en {ctx.guild.name} por el comando {ctx.command}:\n{str(error)}")
    return

#Evento de mensaje
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if message.guild is None:
        return
    if message.content.startswith(f"<@{bot.user.id}>"):
        with open('prefixes.json','r') as f:
            prefixes =json.load(f)
        prefix = prefixes[str(message.guild.id)]
        await message.channel.send(f"Hola {message.author.mention}, mi prefix es `{prefix}`")
        return
    await bot.process_commands(message)
#------------------------------------------

#Comandos---------------------------------

@bot.tree.command(name="ping", description="comando de prueba")
async def ping1(interaction: discord.Interaction):
    #await interaction.response.send_message("pong")
    await interaction.response.send_message("!pong", ephemeral=True) #solo lo puede ver el que lo uso

@bot.command()#Ver los servidores del bot
@commands.is_owner()
async def servers(ctx):
    """Muestra todos los servidores en los que esta el bot"""
    #crear embed
    embed = discord.Embed(title="Servidores", description="Lista de servidores", color=0x00ff00)
    embed.add_field(name="Servidores", value=f"{len(bot.guilds)}", inline=True)
    embed.add_field(name="Usuarios", value=f"{len(set(bot.get_all_members()))}", inline=True)
    #añadir servidores
    for guild in bot.guilds:
        embed.add_field(name=guild.name, value=f"{guild.id}", inline=False)
    #enviar embed
    await ctx.send(embed=embed)
    return

#Mod
@bot.command() #Cambiar prefix
@commands.has_permissions(administrator=True)
async def setprefix(ctx,prefix):
    await ctx.send("Comando en proceso de eliminación")
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
@commands.bot_has_permissions(embed_links=True)
async def embed(ctx):
    embed = discord.Embed(title="Titulo uwu", description="Descripcion", timestamp=datetime.datetime.utcnow(), color=discord.Color.blue())
    await ctx.send(embed=embed)

#Dev
#Reiniciar archivo de comandos
@bot.command()
@commands.is_owner()
async def reload(ctx,extension):
        await bot.unload_extension(f'comandos.{extension}')
        await bot.load_extension(f'comandos.{extension}')
        await ctx.send(f"La extencion {extension} se recargo correctamente")
        print(f'Descarga y carga de {extension}')

#Cargar archivo de comandos
@bot.command()
@commands.is_owner()
async def load(ctx,extension):
    await bot.load_extension(f'comandos.{extension}')
    print(f'Se ha cargado: {extension}')
    await ctx.send(f'Se ha cargado: {extension} correctamente')

#Descargar archivo de comandos
@bot.command()
@commands.is_owner()
async def unload(ctx,extension):
    await bot.unload_extension(f'comandos.{extension}')
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

#Funcion para cargar los comandos---------------------------
async def load_extensions():
    progreso = tqdm(total=8, desc="Cargando comandos", unit="comandos", colour="green", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]")
    for filename in os.listdir('./comandos'):
        if filename.endswith(".py"):
            await bot.load_extension(f"comandos.{filename[:-3]}")
    progreso.update(1)
    for filename in os.listdir('./comandos/general'):
        if filename.endswith(".py"):
            await bot.load_extension(f"comandos.general.{filename[:-3]}")
    progreso.update(1)
    for filename in os.listdir('./comandos/mod'):
        if filename.endswith(".py"):
            await bot.load_extension(f"comandos.mod.{filename[:-3]}")
    progreso.update(1)
    for filename in os.listdir('./comandos/musica'):
        if filename.endswith(".py"):
            await bot.load_extension(f"comandos.musica.{filename[:-3]}")
    progreso.update(1)
    for filename in os.listdir('./comandos/diversion'):
        if filename.endswith(".py"):
            await bot.load_extension(f"comandos.diversion.{filename[:-3]}")
    progreso.update(1)
    for filename in os.listdir('./comandos/dev'):
        if filename.endswith(".py"):
            await bot.load_extension(f"comandos.dev.{filename[:-3]}")
    progreso.update(1)
    for filename in os.listdir('./comandos/owner'):
        if filename.endswith(".py"):
            await bot.load_extension(f"comandos.owner.{filename[:-3]}")
    progreso.update(1)
    for filename in os.listdir('./comandos/ai'):
        if filename.endswith(".py"):
            await bot.load_extension(f"comandos.ai.{filename[:-3]}")
    progreso.update(1)
#Iniciar bot---------------------------------
@bot.command()
@commands.is_owner()
async def sync(ctx) -> None:
    ftm = await ctx.bot.tree.sync()
    await ctx.send(f"{len(ftm)} comandos sincronizados")

async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)

asyncio.run(main())


#--------------------------------------------