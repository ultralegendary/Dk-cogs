import discord
from redbot.core import commands
import pandas as pd
import os



class roll_n(commands.Cog):
    def __init__(self,bot):
        self.data=pd.read_csv("roll_n/resource/db.csv").set_index("r_no")
        self.bot=bot
    def prin(self):
        print(self.data)
    @commands.command()
    async def roll(self,ctx,option :str =None):
        """displays the details of roll number provided"""
        await ctx.send(str)
        
        


    
