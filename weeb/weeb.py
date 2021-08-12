import contextlib
from random import choice

import discord
from discord import NotFound
from redbot.core import commands, data_manager

class Weeb(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
    @commands.command()
    async def uwu(self,ctx):
        """UwU some randome decorated UwU
        `[p]uwu c`- to delete the original messege
        """
        
        await ctx.send("✧･ﾟ: *✧･Bﾟ♡I*(t)*C♡H･ﾟ✧*:･ﾟ✧")
    
    @commands.command()
    async def owo(self,ctx):
        if ctx.channel.permissions_for(ctx.me).manage_messages:
                await ctx.message.delete()
        else:
            raise commands.BotMissingPermissions(discord.Permissions(manage_messages=True))

        await ctx.send("https://cdn.discordapp.com/emojis/742951429211291758.png")
    @commands.command()
    async def baka(self,ctx):
        pass
    @commands.command()
    async def massping(self,ctx,option:str =None):
        for i in "1"*5:
            if option==None:
                pass
                

            if option.isdigit():
                if option == 497379893592719360:
                    await ctx.send("Dont be smart pinging owner")
                else:
                    await ctx.send("<@!{a}>".format(a=option))
            elif(option[0]=='<'and option[-1]=='>'):
                if option[3:-1]== 497379893592719360:
                    await ctx.reply("Dont be smart pinging owner")
                else:
                    await ctx.send(option)




