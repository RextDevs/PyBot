import discord
import asyncio
from discord.ext import commands

class recordatoriosclass(commands.Cog):
    def __init__(self, bot):
        self.bot= bot

    #crear comando recordatorios con alias r, record, reminder
    @commands.command(aliases=['r','record','reminder'])
    async def recordatorio(self,ctx,*,texto:str=None):
        await ctx.send("Comando deshabilitado por el momento, vuelve mas tarde")
        return
        await ctx.send("COMANDO EN DESARROLLO")
        #Funciones
        def check(m):
            return m.author.id == ctx.author.id
        #Verificar variables
        if texto is None:
            await ctx.send("No has puesto ningun texto")
            texto = await self.bot.wait_for('message',check=check)
            texto = texto.content
        await ctx.send(f"Ingrese la cantidad a minutos que desea que se le recorde")
        tiempo= await self.bot.wait_for('message',check=check)
        tiempo = int(tiempo.content)
        while True:
            await ctx.send(f'{texto}, {ctx.author.mention}')
            await asyncio.sleep(tiempo*60)

        


async def setup(bot):
    await bot.add_cog(recordatoriosclass(bot))