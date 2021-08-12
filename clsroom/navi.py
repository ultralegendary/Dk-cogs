from __future__ import print_function
from typing import Literal
from datetime import date, datetime, timedelta

import discord
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config
from redbot.core.utils import chat_formatting as cf
from redbot.core.utils.menus import menu
from redbot.core.utils.menus import DEFAULT_CONTROLS
import pandas as pd
import os
from tabulate import tabulate
import os.path
from sys import path
import time
path.insert(0,r"Dk-cogs\clsroom")
import res
class navi(commands.Cog):
    """cog to maintain classroom things"""
    def __init__(self,bot):
        self.bot=bot
        self.config = Config.get_conf(
            self,
            identifier=12345,
            force_registration=True,
        )
        
        
        self.day_order=res.day_order
        res.AIBatch1
        self.tt1=res.AIBatch1
        self.tt2=res.AIBatch2
        self.mtechtt=res.Mtechcs
        self.today=date.today()
        self.li=res.links

        self.time=time.time()
        self.t=self.today.ctime()
        self.timestamp=[9,10,13,14,15]



    @commands.group()
    async def timetable(self,ctx):
        """`[p]timetable department` displays the timetable of the department"""
        
        #sdate = date(*[int(i)for i in sdate.split('-')])
        

    @timetable.command()
    async def mtech(self,ctx):
        
        table1=[]
        
        for i in self.mtechtt.keys():
            
            table1.append([i]+[self.mtechtt[i][j]for j in range(5)])
        

        await menu(
            ctx,
            [
                f"```{i} ```" + f"**Batch {j+1}**" 
                for j,i in enumerate(list([
                    
                        tabulate(
                            table1,
                            headers=["9:30","10:30", "1:30", "2:30","3:30"],
                            tablefmt="presto",
                            colalign=("left",),
                        )
                        ]
                    
                ))
            ],
            DEFAULT_CONTROLS,
            )

    @timetable.command()
    async def aids(self,ctx):
        
        table1=[]
        table2=[]
        for i in self.tt1.keys():
            table1.append([i]+[self.tt1[i][j]for j in range(5)])
        for i in self.tt2.keys():
            table2.append([i]+[self.tt2[i][j]for j in range(5)])
        

        await menu(
            ctx,
            [
                f"```{i} ```" + f"**Batch {j+1}**" 
                for j,i in enumerate(list([
                    
                        tabulate(
                            table1,
                            headers=["9:30","10:30", "1:30", "2:30","3:30"],
                            tablefmt="presto",
                            colalign=("left",),
                        )
                        ,
                        tabulate(
                            table2,
                            headers=["9:30","10:30", "1:30", "2:30","3:30"],
                            tablefmt="presto",
                            colalign=("left",),
                        )]
                    
                ))
            ],
            DEFAULT_CONTROLS,
            )
    
    @commands.group()
    async def link(self,ctx):
        """`[p]link department` gives the clasroom meetlink of upcomming class"""
        
        
    @link.command()
    async def ai(self,ctx,batch:int=None):
        """Displays the joining link of next class"""
        self.time=datetime.now()#.strftime("%H:%M:%S")
        msg=[]
        embs=[]
        
        st,s='',''
        d=self.today
        while(self.day_order[str(d)]=="Day-0"):
            d+=timedelta(days=1)
        if(d!=self.today):
            emb=discord.Embed(title="Holiday",description=f"Holiday\n{self.today-d} day(s) untill next working day")
            embs.append(emb)
            st+=f"Holiday\n{self.today-d} day(s) untill next working day"
        else:
            emb=discord.Embed(title=f"{self.day_order[str(d)]}")
            st+=f"{self.day_order[str(d)]}"
            index=0
            while(index<5 and self.time.replace(hour=self.timestamp[index],minute=30,second=0)<self.time):
                index+=1
            if(index<5):
                if batch!=2:
                    emb.add_field(name="Batch-1 Upcomming class",value=f"{self.tt1[self.day_order[str(d)]][index]}\n **STart time:** {self.timestamp[index]}:30 \n [Google-Meet-link]({self.li[self.tt1[self.day_order[str(d)]][index]]})")
                    
                    s+=f"\n`Upcomming class :`  {self.tt1[self.day_order[str(d)]][index]} \t{self.timestamp[index]}:30\
                    \n`Link:`  <{self.li[self.tt1[self.day_order[str(d)]][index]]}>"
                    if index!=0:
                        emb.add_field(name="Batch-1 Ongoing class",value=f"{self.tt1[self.day_order[str(d)]][index-1]}\n **End time:** {self.timestamp[index]+1}:30 \n [Google-Meet-link]({self.li[self.tt1[self.day_order[str(d)]][index-1]]})")
                    
                        s+=f"\n`Ongoing class :`  {self.tt1[self.day_order[str(d)]][index-1]}\
                        \n`Link:`  <{self.li[self.tt1[self.day_order[str(d)]][index-1]]}>"
                    msg.append(s)
                    embs.append(emb)
                emb=discord.Embed(title=f"{self.day_order[str(d)]}")
                s=''
                emb.add_field(name="Batch-2 Upcomming class",value=f"{self.tt2[self.day_order[str(d)]][index]}\n **Start time:** {self.timestamp[index]}:30 \n [Google-Meet-Link]({self.li[self.tt2[self.day_order[str(d)]][index]]})")
                s+=f"\n`Upcomming class :`  {self.tt2[self.day_order[str(d)]][index]}\
                    \n`Link:`   <{self.li[self.tt2[self.day_order[str(d)]][index]]}>"

                if index!=0:
                    emb.add_field(name="Batch-2 Ongoing class",value=f"{self.tt2[self.day_order[str(d)]][index-1]}\n **End time:** {self.timestamp[index]+1}:30 \n {self.li[self.tt2[self.day_order[str(d)]][index-1]]}")
                    s+=f"\n`Ongoing class :`  {self.tt2[self.day_order[str(d)]][index-1]}\
                    \n`Link:`  <{self.li[self.tt2[self.day_order[str(d)]][index-1]]}>"
                msg.append(s)
                embs.append(emb)

            else:
                embs.append(discord.Embed(title="End of day",description="class tommrow"))
                s="No classes for today"
        
        
        
        await menu(
            ctx,
            embs,
            DEFAULT_CONTROLS,
            )
        return
        await menu(
            ctx,
            [
                st+f"{i} " + f"\n**Batch {j+1}**" 
                for j,i in enumerate(list(
                        msg           
                ))
            ],
            DEFAULT_CONTROLS,
            )

        #await ctx.send(msg)
        


        


