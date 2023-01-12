import discord
from discord import app_commands
from discord.ext import commands
import datetime,json

class Ayuda(commands.Cog):
    def __init__(self, bot):
        self.bot= bot

    #@commands(name="help", description="Muestra los comandos del bot")
    @app_commands.command(name="help", description="Muestra los comandos del bot")
    @commands.bot_has_permissions(embed_links=True)
    async def help(self, interaction: discord.Interaction) -> None:
        #Leer jsons
        with open("config.json","r") as j:
            versiones=json.load(j)
        with open("prefixes.json","r") as f:
            prefixes=json.load(f)
        prefix=prefixes[str(interaction.guild.id)]
        #Iniciar embed
        embed=discord.Embed(title=f"Comandos", description=f"Prefix: {prefix}\nVersión del bot: {versiones['versiones']['bot']}", timestamp=datetime.datetime.utcnow(), color=discord.Color.dark_blue())
        #Agregar comandos
        embed.add_field(name='dog',value='Una imagen aleatoria de perros\nUso: dog <module>, use dog help para mas información',inline=False)
        embed.add_field(name='cat',value='Una imagen aleatoria de gatos',inline=False)
        embed.add_field(name='capy', value='Una imagen aleatoria de capybaras',inline=False)
        embed.add_field(name='info',value='Información del servidor',inline=False)
        embed.add_field(name='userinfo',value='Información de un usuario',inline=False)
        embed.add_field(name='avatar',value='Avatar de un usuario',inline=False)
        embed.add_field(name='traducir*****',value='Traduce un texto (En desarrollo)',inline=False)
        embed.add_field(name='~~recordatorio~~*****',value='~~Crea un recordatorio~~',inline=False)
        embed.add_field(name='pokedex',value=f'Consultas a una pokedex, funciona tanto con id o nombre de un pokemon\nUso: {prefix}pokedex <id o nombre>',inline=False)
        embed.add_field(name='setprefix*****',value=f'Cambia el prefix del bot\nUso: {prefix}setprefix <nuevo prefix> **(Solo admins)**',inline=False)
        embed.add_field(name='minecraft',value=f'Información de un servidor de minecraft\nUso: {prefix}minecraft help\n*Puede experimentar problema, estamos actualmente trabajando para resolver los errores presentes*',inline=False)
        embed.add_field(name='reportbug',value=f'Reporta un error en el bot',inline=False)
        embed.add_field(name='beta*****', value=f'Le otorga información de los comandos en estado de prueba, **Solo para servidores registrados**', inline=False)
        embed.add_field(name="*****", value="Comandos deshabilidados, en desarrollo o en proceso de eliminación")
        embed.set_footer(text='Bot creado por: Rext\nGitHub: Rextpro/PyBot\n')
        #Enviar embed
        await interaction.response.send_message(embed=embed, ephemeral=True)
        


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Ayuda(bot))