import discord
from discord.ext import commands
from discord.utils import get
from random import randint

class mensajes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def dm(self,ctx):
        #,member:discord.Member
        await ctx.send("El comando esta desactivado por el momento, vuelve mas tarde")
        return
        await ctx.send("Que le desea decir?")
        def check(m):
            return m.author.id == ctx.author.id
        message = await self.bot.wait_for('message',check=check)
        #await ctx.send(f'{ctx.author.name} envio un mensaje a {member}')
        await member.send(f'{ctx.author.mention} Tiene un mensaje para ti:\n{message.content}')
async def setup(bot):
    await bot.add_cog(mensajes(bot))
