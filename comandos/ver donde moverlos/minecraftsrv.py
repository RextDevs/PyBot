from sys import prefix
import discord
import asyncio
from discord.ext import commands
import requests, random, json


class srvbeta(commands.Cog):
    def __init__(self, bot):
        self.bot= bot
    
    @commands.command()
    @commands.bot_has_permissions(embed_links=True)
    async def minecraft(self, ctx, module: str=None, ip:str=None,puerto:str=None, edicion:str=None):
        #Cargar json de versiones
        with open("config.json","r") as j:
            versiones=json.load(j)
        #Cargar json de los prefixes
        with open("prefixes.json","r") as j:
            prefixes=json.load(j)
        prefix=prefixes[f"{ctx.guild.id}"]

        #FUNCIONES
        #Funcion para preguntar edicion, ip y puerto
        async def preguntar(edicion,ip,puerto):
            #Verificar si el usuario es el que mando el mensaje
            def check(m):
                return m.author.id == ctx.author.id
            #Verificar si existe edicion
            if edicion==None or (edicion != "1" and edicion != "2"):
                await ctx.send(f'{ctx.author.mention} Por favor especifica la edicion que deseas ver:\nJava: 1\nBedrock: 2')
                edicion = await self.bot.wait_for('message',check=check)
                edicion = edicion.content
            #Verificar si existe ip
            if ip==None:
                await ctx.send(f'{ctx.author.mention} Ingresa la IP del servidor')
                ip = await self.bot.wait_for('message',check=check)
                ip = ip.content
            #Verificar si existe puerto
            if puerto==None:
                await ctx.send(f'{ctx.author.mention} Ingresa el puerto del servidor, ingrese **NA** si no tiene puerto')
                puerto = await self.bot.wait_for('message',check=check)
                puerto = puerto.content
            if puerto == "NA":
                if edicion == "1":
                    puerto = "25565"
                elif edicion == "2":
                    puerto = "19132"
            return edicion,ip,puerto
        #Funcion para realizar peticion
        async def realizarpeticion(edicion, ip, puerto):
            global peticion
            
            #Asignar variables con api
            api1= "https://api.mcsrvstat.us/2/" #Java IP:PORT
            api1_simple= "https://api.mcsrvstat.us/simple/" #JAVA IP:PORT no json
            api1_bedrock= "https://api.mcsrvstat.us/bedrock/2/" #Bedrock IP:PORT
            api2="https://mcapi.us/server/status?" #ip=...&port=...
            api2_imagen="https://mcapi.us/server/image?" #ip=...&port=...&theme=...&title=...
            api3="https://mcstatus.snowdev.com.br/api/query/v3/" #Java y bedrock? IP:PORT VIP
            api4="https://api.minetools.eu/query/"#NAH, bedrock IP/PORT
            
            estadopeticion ="no"
            while estadopeticion == "no":
                #Crear variable aleatoria para revisar que api usar
                api = random.randint(1,3)
                #Realizar peticion
                if edicion == "1":
                    if api == 1:
                        peticion = requests.get(f'https://api.mcsrvstat.us/2/{ip}:{puerto}')
                        #verificar que la peticion sea correcta
                        if peticion.status_code == 200:
                            estadopeticion = "si"
                            peticion = peticion.json()
                            if peticion["online"] == True:
                                #Asignar variables
                                version = peticion["version"]
                                online = "online"
                                maxplayers = peticion["players"]["max"]
                                onlineplayers = peticion["players"]["online"]
                            else:
                                online="offline"
                        else:
                            online="offline"
                    elif api == 2:
                        peticion = requests.get(f'https://mcapi.us/server/status?ip={ip}&port={puerto}')
                        #verificar que la peticion sea correcta
                        if peticion.status_code == 200:
                            estadopeticion = "si"
                            peticion = peticion.json()
                            if peticion["online"] == True:
                                #Asignar variables
                                version = peticion["server"]["name"]
                                online = "online"
                                maxplayers = peticion["players"]["max"]
                                onlineplayers = peticion["players"]["now"]
                            else:
                                online="offline"
                        else:
                            online="offline"
                    elif api == 3:
                        peticion = requests.get(f'https://mcstatus.snowdev.com.br/api/query/v3/{ip}:{puerto}')
                        #verificar que la peticion sea correcta
                        if peticion.status_code == 200:
                            estadopeticion = "si"
                            peticion = peticion.json()
                            if peticion["online"] == True:
                                #Asignar variables
                                version = peticion["version"]
                                online = "online"
                                maxplayers = peticion["max_players"]
                                onlineplayers = peticion["players_online"]
                            else:
                                online="offline"
                        else:
                            online="offline"
                elif edicion == "2":
                    if api >=1 or api <=2:
                        peticion = requests.get(f'https://api.mcsrvstat.us/bedrock/2/{ip}:{puerto}')
                        #verificar que la peticion sea correcta
                        if peticion.status_code == 200:
                            estadopeticion = "si"
                            peticion = peticion.json()
                            if peticion["online"] == True:
                                #Asignar variables
                                version = peticion["version"]
                                online = "online"
                                maxplayers = peticion["players"]["max"]
                                onlineplayers = peticion["players"]["online"]
                            else:
                                online="offline"
                    elif api == 3:
                        peticion = requests.get(f'https://api.minetools.eu/query/{ip}/{puerto}')
                        #verificar que la peticion sea correcta
                        if peticion.status_code == 200:
                            estadopeticion = "si"
                            peticion = peticion.json()
                            if peticion["online"] == True:
                                #Asignar variables
                                version = peticion["Version"]
                                online = "online"
                                maxplayers = peticion["MaxPlayers"]
                                onlineplayers = peticion["Players"]
                            else:
                                online="offline"
                else:
                    online="offline"
                
            if online == "online":
                return version,online,int(maxplayers),onlineplayers
            else:
                return "0.0.0.0",online,0,0
        #Funcion de evento
        async def actualizar(server,id):
            global servidord
            #leer servidores
            with open("srvmc.json","r") as f:
                servidord=json.load(f)
            #Leer variables
            edicion=servidord[f"{server}"]['servers'][f"{id}"]["edicion"]
            ip=servidord[f"{server}"]['servers'][f"{id}"]["ip"]
            puerto=servidord[f"{server}"]['servers'][f"{id}"]["puerto"]
            #ver si el evento esta inactivo
            if servidord[str(ctx.guild.id)]['servers'][f"{id}"]['activo']=="Inactivo":
                #eliminar id de servers
                servidord[str(ctx.guild.id)]['servers'].pop(f"{id}")
                with open("srvmc.json","w") as f:
                        json.dump(servidord,f)
                return
            #mientras el evento esta activo
            while servidord[str(ctx.guild.id)]['servers'][f"{id}"]['activo']=="En proceso":
                #leer servidores
                with open("srvmc.json","r") as f:
                    servidord=json.load(f)
                #realizar peticion
                version,online,maxplayers,onlineplayers = await realizarpeticion(edicion, ip, puerto)
                if maxplayers>1:
                    ahora = "En linea"
                else:
                    ahora = "Offline"
                #Ver si el servidor cambio de estado
                if ahora!=servidord[str(ctx.guild.id)]['servers'][f"{id}"]["anterior"]:
                    await ctx.send(f"El servidor {ip}:{puerto} esta {ahora}")
                    servidord[str(ctx.guild.id)]['servers'][f"{id}"]["anterior"] = ahora
                    with open("srvmc.json","w") as f:
                        json.dump(servidord,f)
                #activar cooldown
                i=0
                while i<30:
                    await asyncio.sleep((int(servidord[str(ctx.guild.id)]['servers'][f"{id}"]["cooldown"])/30))
                    with open("srvmc.json","r") as f:
                        servidord=json.load(f)
                    if servidord[str(ctx.guild.id)]['servers'][f"{id}"]['activo']=="Inactivo":
                        #quitar el servidor id del json
                        servidord[str(ctx.guild.id)]['servers'].pop(f"{id}")
                        with open("srvmc.json","w") as f:
                                json.dump(servidord,f)
                        await ctx.send(f"El servidor {ip}:{puerto} se ha eliminado correctamente")
                        return
                    if servidord['actualizando']=="si":
                        await ctx.send(f"El bot entrara en actualizacion, esto pausara la revision de los servidores, espere a que el bot vuelva a estar en linea")
                        return
                    i+=1
        
        #Modulo de ayuda
        if module==None or module=="help":
            #Se creara un embed para mostrar la funcion general del comando
            embed=discord.Embed(title="Minecraft", description=f"Version {versiones['versiones']['minecraft']}", color=0x00ff00)
            #embed.set_author(name="Minecraft", icon_url="https://i.imgur.com/XqQZQ.png")
            #embed.set_thumbnail(url="https://i.imgur.com/XqQZQ.png")
            embed.add_field(name="Forma de uso",value=f"Se usa de esta manera\n{prefix}minecraft [Modulo] <argumentos>\n [ ] -> Obligatorio\n< > -> opcional",inline=False)
            embed.add_field(name="Help", value="Muestra esta ayuda", inline=False)
            embed.add_field(name="Status", value=f"Muestra el estado del servidor\n{prefix}minecraft status <ip> <puerto>", inline=False)
            embed.add_field(name="autocheck", value=f"Manda un mensaje automatico al servidor cuando el servidor este online o offline\n{prefix}minecraft autocheck help ->Para mas información", inline=False)
            await ctx.send(embed=embed)
            return
        #Modulo de status
        if module=="status":
            #corroborar si estan bien las variables
            edicion, ip, puerto=await preguntar(edicion,ip,puerto)
            #Realizar peticion
            version,online,maxplayers,onlineplayers = await realizarpeticion(edicion, ip, puerto)
            #Enviar peticion si el servidor esta online
            if int(maxplayers)>1:
                embed=discord.Embed(title=f"Servidor de Minecraft status", description=f"Versión del comando: {versiones['versiones']['minecraft']}\nJugadores: {onlineplayers}/{maxplayers}", color=discord.Color.blue())
                embed.add_field(name="IP:", value= ip)
                embed.add_field(name="Puerto:", value= puerto)
                embed.add_field(name="Version:", value= version)
                embed.add_field(name="Encendido:", value= online)
                embed.add_field(name="Jugadores:", value= onlineplayers)
                embed.add_field(name="Jugadores maximo:", value= maxplayers)
                await ctx.send(embed=embed)
            #Enviar mensaje si el servidor esta offline
            else:
                await ctx.send(f'{ctx.author.mention} El servidor esta offline')
            return
        if module=="autocheck":
            #verificar si el usuario tiene permisos de gestor de mensajes
            if not ctx.author.guild_permissions.manage_messages:
                await ctx.send(f'{ctx.author.mention} No tienes permisos para usar este comando')
                return
            #Ver variable ip
            if ip==None or ip=="help":
                #crear embed de ayuda
                embed=discord.Embed(title="Minecraft autocheck", description=f"Version {versiones['versiones']['minecraft']}\nSolo con permiso \"Gestor de mensajes\"", color=0x00ff00)
                embed.add_field(name="Forma de uso",value=f"Se usa de esta manera\n{prefix}minecraft autocheck [modulo] <argumentos>\n [ ] -> Obligatorio\n< > -> opcional",inline=False)
                embed.add_field(name="help", value="Muestra esta ayuda", inline=False)
                embed.add_field(name="add", value=f"Crea un evento para iniciar el evento\n{prefix}minecraft autocheck add <ip> <puerto>", inline=False)
                embed.add_field(name="list", value=f"Muestra los eventos creados\n{prefix}minecraft autocheck list", inline=False)
                embed.add_field(name="check", value=f"Envia el estado actual del evento\n{prefix}minecraft autocheck check [id]", inline=False)
                embed.add_field(name="stop", value=f"Detiene un evento del autocheck\n{prefix}minecraft autocheck stop [id]", inline=False)
                embed.add_field(name="updater", value=f"Actualiza un evento\n{prefix}minecraft autocheck update [id]", inline=False)
                embed.add_field(name="info", value=f"Muestra informacion del evento\n{prefix}minecraft autocheck info [id]", inline=False)
                await ctx.send(embed=embed)
                return
            #Leer json de autocheck
            with open("srvmc.json","r") as f:
                servidord=json.load(f)
            #Verificar si el servidor esta registrado y si no, crear el registro y guardar el json
            if not str(ctx.guild.id) in servidord:
                servidord[str(ctx.guild.id)] ={
                    "tokens":1,
                    "tiempomin":5,
                    "servers":{}}
            with open("srvmc.json","w") as f:
                json.dump(servidord,f)
            
            #Modulo add
            if ip=="add":
                ip=puerto
                puerto = edicion
                #Verificar si aun tiene tokens
                if servidord[str(ctx.guild.id)]["tokens"]<=0:
                    await ctx.send("Has superado el limite de tokens")
                    return
                #corroborar si estan bien las variables
                edicion, ip, puerto=await preguntar(edicion,ip,puerto)
                #ver los servidores registrados
                id = 0
                for i in servidord[str(ctx.guild.id)]["servers"]:
                    #ver si el servidor ya esta registrado
                    if f"{ip}" == servidord[str(ctx.guild.id)]["servers"][str(i)]['ip'] and f"{puerto}" == servidord[str(ctx.guild.id)]["servers"][str(i)]['puerto']:
                        await ctx.send(f'El servidor ya esta registrado')
                        return
                    id+=int(servidord[str(ctx.guild.id)]["servers"][str(i)]['id'])+1
                
                #Crear registro
                servidord[str(ctx.guild.id)]['servers'][f"{id}"]={
                    "activo":"En proceso",
                    "id":id,
                    "ip":ip,
                    "puerto":puerto,
                    "edicion":edicion,
                    "cooldown": 800,
                    "canal": ctx.channel.id
                }
                #Restar tokens
                servidord[str(ctx.guild.id)]["tokens"]-=1
                #Realizar peticion
                version,online,maxplayers,onlineplayers = await realizarpeticion(edicion, ip, puerto)
                #Enviar peticion si el servidor esta online o enviar mensaje si el servidor esta offline
                if maxplayers>1:
                    ahora = "En linea"
                else:
                    ahora = "Offline"
                await ctx.send(f'El servidor {ip} esta {ahora}\n ya puedes borrar este y los mensajes anteriores')
                #guardar ahora en el json
                servidord[str(ctx.guild.id)]['servers'][f"{id}"]["anterior"] = ahora
                #Guardar json
                with open("srvmc.json","w") as f:
                    json.dump(servidord,f)
                #llamar a la funcion de crear evento
                await actualizar(str(ctx.guild.id),id)
                return
                
            #Modulo list
            if ip=="list":
                #enviar los servidores y su id
                embed=discord.Embed(title="Lista de servidores", description=f"Version {versiones['versiones']['minecraft']}", color=0x00ff00)
                for i in servidord[str(ctx.guild.id)]["servers"]:
                    embed.add_field(name=f"ID: {servidord[str(ctx.guild.id)]['servers'][i]['id']}", value=f"IP: {servidord[str(ctx.guild.id)]['servers'][i]['ip']}\nPuerto: {servidord[str(ctx.guild.id)]['servers'][i]['puerto']}", inline=False)
                await ctx.send(embed=embed)
                return
            #Modulo check
            if ip=="check":
                #verificar si existe el id del servidor
                if not str(puerto) in servidord[str(ctx.guild.id)]["servers"]:
                    await ctx.send(f'El servidor no existe')
                    return
                id=puerto
                #Leer variables
                edicion = servidord[str(ctx.guild.id)]["servers"][id]['edicion']
                ip = servidord[str(ctx.guild.id)]["servers"][id]['ip']
                puerto = servidord[str(ctx.guild.id)]["servers"][id]['puerto']

                #Realizar peticion
                version,online,maxplayers,onlineplayers = await realizarpeticion(edicion, ip, puerto)
                #Enviar peticion si el servidor esta online o enviar mensaje si el servidor esta offline
                if online==True and maxplayers>1:
                    ahora = "En linea"
                else:
                    ahora = "Offline"
                await ctx.send(f'El servidor {ip}:{puerto} esta {ahora}')
                return
            #Modulo stop
            if ip=="stop":
                #verificar si existe el id del servidor
                if not str(puerto) in servidord[str(ctx.guild.id)]["servers"]:
                    await ctx.send(f'El servidor no existe')
                    return
                id=puerto
                #actualizar ajuste activo y cooldown del json
                servidord[str(ctx.guild.id)]["servers"][id]["activo"]="Inactivo"
                servidord[str(ctx.guild.id)]["servers"][id]["cooldown"]=1
                #añadir tokens
                servidord[str(ctx.guild.id)]["tokens"]+=1
                #guardar json
                with open("srvmc.json","w") as f:
                    json.dump(servidord,f)
                #mandar menaje de que se ha desactivado el servidor
                await ctx.send(f'El servidor {ip}:{puerto} se ha desactivado, espere el mensaje cuando se haya eliminado correctamente, esto puede demorar un tiempo')
                return
            #modulo info
            if ip=="info":
                #verificar si existe el id del servidor
                if not str(puerto) in servidord[str(ctx.guild.id)]["servers"]:
                    await ctx.send(f'El servidor no existe')
                    return
                id=puerto
                #Leer variables
                edicion = servidord[str(ctx.guild.id)]["servers"][id]['edicion']
                ip = servidord[str(ctx.guild.id)]["servers"][id]['ip']
                puerto = servidord[str(ctx.guild.id)]["servers"][id]['puerto']
                cooldown=servidord[str(ctx.guild.id)]["servers"][id]['cooldown']
                canal=servidord[str(ctx.guild.id)]["servers"][id]['canal']
                activo=servidord[str(ctx.guild.id)]["servers"][id]['activo']
                anterior=servidord[str(ctx.guild.id)]["servers"][id]['anterior']
                #Enviar mensaje
                embed=discord.Embed(title="Informacion del servidor", description=f"Version {versiones['versiones']['minecraft']}", color=0x00ff00)
                embed.add_field(name="Estado del evento:", value=f"{activo}", inline=False)
                embed.add_field(name="ID:", value=f"{id}", inline=False)
                embed.add_field(name="IP:", value=f"{ip}", inline=False)
                embed.add_field(name="Puerto:", value=f"{puerto}", inline=False)
                embed.add_field(name="Edicion:", value=f"{edicion}", inline=False)
                embed.add_field(name="Canal:", value=f"{canal}", inline=False)
                embed.add_field(name="Estado:", value=f"{anterior}", inline=False)
                embed.add_field(name="Cooldown:", value="{cooldown} segundos", inline=False)
                await ctx.send(embed=embed)
                return
        #modulo reanudar
        if module=="reanudar":
            with open("srvmc.json","r") as f:
                servidord=json.load(f)
            #verificar si existe el id del servidor
            if not ip:
                return
            if not str(ip) in servidord[str(ctx.guild.id)]["servers"]:
                return
            if not "reanudar" in servidord[str(ctx.guild.id)]["servers"][ip]:
                return
            if servidord[str(ctx.guild.id)]["servers"][str(ip)]["reanudar"]=="si":
                #Leer variables
                servidord[str(ctx.guild.id)]["servers"][str(ip)]["reanudar"]="no"
                with open("srvmc.json","w") as f:
                    json.dump(servidord,f,indent=4)
                #llamar funcion actualizar
                await actualizar(str(ctx.guild.id), ip)
                return
    
    
    
    @commands.command()
    @commands.is_owner()
    async def minecraftdev(self,ctx,accion:str=None):
        #leer json
        with open("srvmc.json","r") as f:
            servidord=json.load(f)
        with open("prefixes.json","r") as f:
            prefixes=json.load(f)
        #Funcion actualizar
        #Mandar la accion de actualizar
        if accion=="actualizar":
            servidord["actualizando"]="si"
            with open("srvmc.json","w") as f:
                json.dump(servidord,f,indent=4)
            await ctx.send("Se completo la accion de actualizando...")
        
        #Mandar la accion de reanudar los servidores
        if accion=="reanudar":
            servidord["actualizando"]="no"
            with open("srvmc.json","w") as f:
                json.dump(servidord,f,indent=4)
            for i in servidord:
                if not i=="actualizando":
                    prefix=prefixes[str(i)]
                    for e in servidord[str(i)]["servers"]:
                        servidord[str(i)]["servers"][e]["reanudar"]="si"
                        canal = self.bot.get_channel(servidord[str(i)]["servers"][str(e)]["canal"])
                        await canal.send(f"El servidor {servidord[str(i)]['servers'][str(e)]['ip']}:{servidord[str(i)]['servers'][str(e)]['puerto']} esta listo para ser reactivado\n use el comando {prefix}minecraft reanudar {servidord[str(i)]['servers'][str(e)]['id']} para reactivarlo")
                        await ctx.send(f"Se notifico del servidor {e} al servidor {i}")
                        with open("srvmc.json","w") as f:
                            json.dump(servidord,f,indent=4)
                        await asyncio.sleep(0.5)
            await ctx.send("Se completo la accion de reanudar...")

async def setup(bot):
    await bot.add_cog(srvbeta(bot))