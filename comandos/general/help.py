import discord
import asyncio
from discord.ext import commands
import datetime,json

class helpclass(commands.Cog):
    def __init__(self, bot):
        self.bot= bot

    @commands.command()
    async def help(self,ctx):
        #Leer jsons
        with open("config.json","r") as j:
            versiones=json.load(j)
        with open("prefixes.json","r") as f:
            prefixes=json.load(f)
        prefix=prefixes[str(ctx.guild.id)]
        #Iniciar embed
        embed=discord.Embed(title=f"Comados", description=f"Prefix: {prefix}\nVersión del bot: {versiones['versiones']['bot']}", timestamp=datetime.datetime.utcnow(), color=discord.Color.dark_blue())
        #Agregar comandos
        embed.add_field(name='dm',value='Envia un mensaje a un usuario (Comando unicamente de prueba)',inline=False)
        embed.add_field(name='info',value='Información del servidor',inline=False)
        embed.add_field(name='userinfo',value='Información de un usuario',inline=False)
        embed.add_field(name='avatar',value='Avatar de un usuario',inline=False)
        embed.add_field(name='pokedex',value=f'Consultas a una pokedex, funciona tanto con id o nombre de un pokemon\nUsos: {prefix}pokedex <id o nombre>',inline=False)
        embed.add_field(name='setprefix',value=f'Cambia el prefix del bot\nUsos: {prefix}setprefix <nuevo prefix> (Solo admins)',inline=False)
        embed.set_footer(text='Bot creado por: @KikeRex#6238')#Creditos
        #Enviar embed
        await ctx.send(embed=embed)
        


def setup(bot):
    bot.add_cog(helpclass(bot))