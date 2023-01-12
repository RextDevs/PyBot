import discord
from discord.ext import commands
from discord.utils import get
from datetime import datetime
from random import randint
from discord import app_commands
class Users(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @app_commands.command(name="userinfo", description="Informacion de un usuario")
    @commands.bot_has_permissions(embed_links=True)
    async def userinfo(self, interaction:discord.Interaction, member:discord.Member=None):
        roles = []
        if not member:
            member = interaction.user
        for role in member.roles:
            roles.append(str(role.mention))
        roles.reverse()
        embed = discord.Embed(title=f"{member}'s User Info")
        embed.add_field(name="Username", value=str(member.name))
        embed.add_field(name="Discriminator", value=str(member.discriminator))
        embed.add_field(name="ID", value=str(member.id))
        embed.add_field(name="Creado el", value=str(member.created_at))
        embed.add_field(name="Unido el", value=str(member.joined_at))
        if len(str(" | ".join([x.mention for x in member.roles]))) > 1024:
            embed.add_field(name=f"Roles [{len(member.roles)}]", value="Too many to display.")
        else:
            embed.add_field(name=f"Roles [{len(member.roles)}]", value=" | ".join(roles))
        embed.add_field(name="Color", value=str(member.color))
        embed.set_thumbnail(url=member.avatar)
        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="avatar", description="Avatar de un usuario")
    @commands.bot_has_permissions(embed_links=True)
    async def avatar(self, interaction:discord.Interaction, member:discord.Member=None):
        roles = []
        if not member:
            member = interaction.user
        embed = discord.Embed(title=f"Avatar de {member}")
        embed.set_image(url=member.avatar)
        await interaction.response.send_message(embed=embed)
		
async def setup(bot):
	await bot.add_cog(Users(bot))