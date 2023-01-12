import discord
import asyncio
from discord.ext import commands

class bugs(commands.Cog):
    def __init__(self, bot):
        self.bot= bot

    @commands.command(aliases=['bug'])
    async def reportbug(self,ctx,*,bug:str=None):
        await ctx.send("Comando en desarrollo",delete_after=5)
        #Verificar argumentos
        if bug==None:
            #solicitar el texto
            await ctx.send("Escriba el bug que desea reportar")
            def check(m):
                return m.author.id == ctx.author.id
            message = await self.bot.wait_for('message',check=check)
            bug=message.content
        #Enviar mensaje al dueño y al canal correspondiente del bot
        owner=await self.bot.fetch_user(612786159306670112)
        await owner.send(f"Bug reportado por: {ctx.author.name}#{ctx.author.discriminator}\nen el servidor: {ctx.guild.name}\nBug: {bug}")
        canal=await self.bot.fetch_channel(1002377944129351770)
        await canal.send(f"Bug reportado por: {ctx.author.name}#{ctx.author.discriminator}\nen el servidor: {ctx.guild.name}\nBug: {bug}")
        #Enviar mensaje de confirmación
        await ctx.send("Bug reportado con exito, muchas gracias por su ayuda, trataremos de solucionarlo lo mas rapido posible")



async def setup(bot):
    await bot.add_cog(bugs(bot))