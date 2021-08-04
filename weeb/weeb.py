import contextlib
from random import choice

import discord
from discord import NotFound
from redbot.core import commands, data_manager

class Weeb(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
    @commands.command()
    async def uwu(self,ctx,option:str=None):
        await ctx.send("✧･ﾟ: *✧･ﾟb♡i*(t)*c♡h･ﾟ✧*:･ﾟ✧")