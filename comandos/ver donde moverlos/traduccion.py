import discord
import asyncio
from discord.ext import commands
from deep_translator import GoogleTranslator
from langdetect import detect


class traduccion1(commands.Cog):
    def __init__(self, bot):
        self.bot= bot

    @commands.command()
    async def t(self,ctx, *, texto):
        #Verificar si el texto es ingles o español
        #Si es ingles, traducir a español con depth_translator
        idioma=detect(texto)
        print(idioma)
        if idioma=='en':
            texto=GoogleTranslator(source='en',target='es').translate(texto)
            await ctx.reply(texto)
        #Si es español, traducir a ingles con depth_translator
        elif idioma=='es':
            texto=GoogleTranslator(source='es',target='en').translate(texto)
            await ctx.reply(texto)
        #Si no es ninguno de los dos, traducir al ingles y al español
        else:
            texto1=GoogleTranslator(source=idioma,target='en').translate(texto)
            texto=GoogleTranslator(source=idioma,target='es').translate(texto)
            await ctx.reply(f"> English: {texto1}\n> Spanish: {texto}")
        #await ctx.send("Comando en desarrollo")
        


async def setup(bot):
    await bot.add_cog(traduccion1(bot))