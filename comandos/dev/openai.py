import discord
import asyncio
from discord.ext import commands
import openai,json,time
from concurrent.futures import ThreadPoolExecutor
def vipcheck(id):
    with open("servidores.json","r") as f:
        vip=json.load(f)
    print(vip[str(id)]['vip'])
    return str(vip[str(id)]['vip'])



class Openai(commands.Cog):
    def __init__(self, bot):
        self.bot= bot
    def createpython(message):
        global response
        response = openai.Completion.create(
        model="code-davinci-002",
        prompt=f"\"\"\"\n{message.content}\n\"\"\"",
        temperature=0,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )
        
    @commands.command()
    async def codigo(self,ctx):
        global response
        vip=vipcheck(ctx.guild.id)
        if vip=="False":
            await ctx.send('El servidor no tiene permiso a usar este comando')
            return
        await ctx.send("Ingrese las instrucciones, siendo asi \n> 1. instruccion 1\n> 2. Instruccion 2\n y asi sucesivamente en el mismo mensaje")
        openai.api_key = 'YOURAPIKEY'
        def check(m):
            return m.author.id == ctx.author.id
        message = await self.bot.wait_for('message',check=check)
        excecutor = ThreadPoolExecutor(max_workers=4)
        excecutor.submit(Openai.createpython, message)
        await asyncio.sleep(10)
        await ctx.send("```python\n"+str(response['choices'][0]['text'])+"\n```")
        


def setup(bot):
    bot.add_cog(Openai(bot))