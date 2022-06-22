import time
import os
import discord
from discord.ext import commands
from discord.utils import get
from datetime import datetime
import requests, json
from random import randint
class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(aliases=["whois", "ui"])
    async def userinfo(self, ctx, member:discord.Member=None):
        roles = []
        if not member:
            member = ctx.author
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
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def avatar(self, ctx, member:discord.Member=None):
        roles = []
        if not member:
            member = ctx.author
        for role in member.roles:
            roles.append(str(role.mention))
        
        roles.reverse()

        embed = discord.Embed(title=f"Avatar de {member}")
        embed.set_image(url=member.avatar_url)
        await ctx.send(embed=embed)
		
def setup(bot):
	bot.add_cog(UserInfo(bot))