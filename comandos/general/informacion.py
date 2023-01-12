import discord
from discord import app_commands
from discord.ext import commands
from discord.utils import get
import datetime
from random import randint


class informacion(commands.Cog):
    def __init__(self, bot):
        self.bot= bot

    @app_commands.command(name="info", description="Muestra la información del servidor")
    @commands.bot_has_permissions(embed_links=True)
    async def info(self, interaction: discord.Interaction) -> None:
        embed = discord.Embed(title=f"{interaction.guild.name}", description="Información del servidor", timestamp=datetime.datetime.utcnow(), color=discord.Color.dark_blue())
        embed.add_field(name="Servidor creado el:", value=f"{interaction.guild.created_at}")
        embed.add_field(name="Owner: ", value=f"{interaction.guild.owner}")
        #embed.add_field(name="Region", value=f"{interaction.guild.}")
        embed.add_field(name="ID", value=f"{interaction.guild.id}")
        embed.add_field(name="Miembros", value=f"{interaction.guild.member_count}")
        embed.add_field(name="Roles", value=f"{len(interaction.guild.roles)}")
        embed.add_field(name="Canales", value=f"{len(interaction.guild.channels)}")
        embed.set_thumbnail(url=interaction.guild.icon)
        await interaction.response.send_message(embed=embed)
        
async def setup(bot):
    await bot.add_cog(informacion(bot))