import discord
import asyncio
from discord.ext import commands
import tqdm

class Developer(commands.Cog):
    def __init__(self, bot):
        self.bot= bot

    @commands.command()
    async def tqdm(self, ctx):
        message = await ctx.send("Progreso")
        # Inicia la barra de progreso
        bar = tqdm.tqdm(total=10)
        for i in range(11):
            await asyncio.sleep(0.5) # simula una tarea
            bar.update(1) # actualiza la barra
            # Actualiza el mensaje con el progreso actual
            await message.edit(content=f'Progreso: {bar}')
        bar.close()
        await ctx.send("Completado")


async def setup(bot):
    await bot.add_cog(Developer(bot))