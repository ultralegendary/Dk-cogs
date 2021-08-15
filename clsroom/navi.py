from __future__ import print_function
from typing import Literal
from datetime import date,datetime, timedelta

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
from . import res

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
        self.cse3_b1tt=res.cse3_b1
        self.cse3_b2tt=res.cse3_b2
        self.today=date.today()
        self.li=res.links
        self.li2=res.linksmt
        self.li3=res.linkscse3b


        self.time=time.time()
        self.t=self.today.ctime()
        self.timestamp=[9,10,13,14,15]



    @commands.group()
    async def timetable(self,ctx):
        """`[p]timetable department` displays the timetable of the department"""
        
        #sdate = date(*[int(i)for i in sdate.split('-')])
        
    @timetable.command()
    async def cse3b(self,ctx):
        """Prints timetable of cse3b"""
        table1=[]
        table2=[]
        for i in self.cse3_b1tt.keys():
            table1.append([i]+[self.cse3_b1tt[i][j]for j in range(4)])
        for i in self.cse3_b2tt.keys():
            table2.append([i]+[self.cse3_b2tt[i][j]for j in range(4)])

        await menu(
            ctx,
            [
                "*CSE III TimeTable*"+f"```{i} ```" + f"**Batch {j+1}**" 
                for j,i in enumerate(list([
                    
                        tabulate(
                            table1,
                            headers=["9:30","10:30", "1:30", "2:30"],
                            tablefmt="presto",
                            colalign=("left",),
                        )
                        ,
                        tabulate(
                            table2,
                            headers=["9:30","10:30", "1:30", "2:30"],
                            tablefmt="presto",
                            colalign=("left",),
                        )]
                    
                ))
            ],
            DEFAULT_CONTROLS,
            )
    @timetable.command()
    async def mtech(self,ctx):
        
        table1=[]
        
        for i in self.mtechtt.keys():
            table1.append([i]+[self.mtechtt[i][j]for j in range(4)])

        await menu(
            ctx,
            [
                "*Mtech TimeTable*" + f"```{i} ```"
                for i in list([
                        tabulate(
                            table1,
                            headers=["9:30","10:30", "1:30", "2:30"],
                            tablefmt="presto",
                            colalign=("left",),
                        )
                        ]   
                )
            ],
            {}
            
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
                "*AIDS TimeTable*"+f"```{i} ```" + f"**Batch {j+1}**" 
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
        self.today=date.today()
        self.time=datetime.now()#.strftime("%H:%M:%S")
        
        
        
    @link.command()
    async def ai(self,ctx,batch:int=None):
        """Displays the joining link of next class for AI-II year"""
        
        embs=[]
        
        d1=datetime.today()
        d=self.today
        j=-1
        while(self.day_order[str(d)]=="Day-0"):
            d+=timedelta(days=1)
            j+=1
        if(d!=self.today):
            emb=discord.Embed(title="Holiday",description=f"*Next class in* {j} days, {(9+24-d1.hour)%24} hours")
            emb.set_footer(text=self.day_order[str(d)])
            embs.append(emb)
            
        else:
            emb=discord.Embed(title="\tAIDS B1 "+f"{self.day_order[str(d)]}")
            
            index=0
            while(index<5 and self.time.replace(hour=self.timestamp[index],minute=30,second=0)<self.time):
                index+=1
            if self.time.replace(hour=self.timestamp[index-1]+1,minute=30,second=0)>self.time:
                
                    
                d1=datetime.today()
                if index!=0:
                    if(self.timestamp[index-1]+1<d1.hour or(self.timestamp[index-1]+1==d1.hour and d1.minute>=30)):
                        emb.add_field(name="Past class\t",value=f"**{self.tt1[self.day_order[str(d)]][index-1]}**\n *End time:* {self.timestamp[index-1]+1}:30 \n [Google-Meet-link]({self.li[self.tt1[self.day_order[str(d)]][index-1]]})")
                    else:
                        emb.add_field(name="Ongoing class\t",value=f"**{self.tt1[self.day_order[str(d)]][index-1]}**\n *End time:* {self.timestamp[index-1]+1}:30 \n [Google-Meet-link]({self.li[self.tt1[self.day_order[str(d)]][index-1]]})")
                    if index !=5:
                        emb.add_field(name="Upcomming class",value=f"**{self.tt1[self.day_order[str(d)]][index]}**\n *Start time:* {self.timestamp[index]}:30 \n [Google-Meet-link]({self.li[self.tt1[self.day_order[str(d)]][index]]})")
                    
                    embs.append(emb)
                emb=discord.Embed(title="\tAIDS B2 "+f"{self.day_order[str(d)]}")
                
                if index!=0:
                    if(self.timestamp[index-1]+1<d1.hour or(self.timestamp[index-1]+1==d1.hour and d1.minute>=30)):
                        emb.add_field(name="Past class\t",value=f"**{self.tt2[self.day_order[str(d)]][index-1]}**\n *End time:* {self.timestamp[index-1]+1}:30 \n [Google-Meet-link]({self.li[self.tt2[self.day_order[str(d)]][index-1]]})")
                    else:
                        emb.add_field(name="Ongoing class\t",value=f"**{self.tt2[self.day_order[str(d)]][index-1]}**\n *End time:* {self.timestamp[index-1]+1}:30 \n [Google-Meet-Link]({self.li[self.tt2[self.day_order[str(d)]][index-1]]})")
                if index!=5:
                    emb.add_field(name="Upcomming class",value=f"**{self.tt2[self.day_order[str(d)]][index]}**\n *Start time:* {self.timestamp[index]}:30 \n [Google-Meet-Link]({self.li[self.tt2[self.day_order[str(d)]][index]]})")

                embs.append(emb)

            else:
                d+=timedelta(days=1)
                i=0
                while(self.day_order[str(d)]=="Day-0"):
                    d+=timedelta(days=1)
                    i+=1
                

                embs.append(discord.Embed(title="End of "+self.day_order[str(d-timedelta(days=i+1))],description=f"*Next class in* {i} days, {9+24-d1.hour} hours"))
        
        if len(embs)>1:
            await menu(
                ctx,
                embs,
                DEFAULT_CONTROLS,
                )
        else:
            await ctx.send(embed=embs[0])

    @link.command()
    async def cs(self,ctx):
        """Displays the joining link of next class for Cse-B-III year"""
        #if(ctx.author.id):
        embs=[]
        
        d1=datetime.today()
        d=self.today
        j=-1
        while(self.day_order[str(d)]=="Day-0"):
            j+=1
            d+=timedelta(days=1)
        if(d!=self.today):
            emb=discord.Embed(title="Holiday",description=f"*Next class in* {j} days, {(9+24-d1.hour)%24} hours")
            emb.set_footer(text=self.day_order[str(d)])
            
            embs.append(emb)
            
        else:
            emb=discord.Embed(title="\tCSE-B B1 "+f"{self.day_order[str(d)]}")
            
            index=0
            while(index<4 and self.time.replace(hour=self.timestamp[index],minute=30,second=0)<self.time):
                index+=1
            if self.time.replace(hour=self.timestamp[index-1]+1,minute=30,second=0)>self.time:
                
                    
                d1=datetime.today()
                if index!=0:
                    if(self.timestamp[index-1]+1<d1.hour or(self.timestamp[index-1]+1==d1.hour and d1.minute>=30)):
                        emb.add_field(name="Past class\t",value=f"**{self.cse3_b1tt[self.day_order[str(d)]][index-1]}**\n *End time:* {self.timestamp[index-1]+1}:30 \n [Google-Meet-link]({self.li3[self.cse3_b1tt[self.day_order[str(d)]][index-1]]})")
                    else:
                        emb.add_field(name="Ongoing class\t",value=f"**{self.cse3_b1tt[self.day_order[str(d)]][index-1]}**\n *End time:* {self.timestamp[index-1]+1}:30 \n [Google-Meet-link]({self.li3[self.cse3_b1tt[self.day_order[str(d)]][index-1]]})")
                if(index!=4):
                    emb.add_field(name="Upcomming class",value=f"**{self.cse3_b1tt[self.day_order[str(d)]][index]}**\n *Start time:* {self.timestamp[index]}:30 \n [Google-Meet-link]({self.li3[self.cse3_b1tt[self.day_order[str(d)]][index]]})")
                embs.append(emb)
                
                emb=discord.Embed(title="\tCSE-B B2 "+f"{self.day_order[str(d)]}")
                if index!=0:
                    if(self.timestamp[index-1]+1<d1.hour or(self.timestamp[index-1]+1==d1.hour and d1.minute>=30)):
                        emb.add_field(name="Past class\t",value=f"**{self.tt2[self.day_order[str(d)]][index-1]}**\n *End time:* {self.timestamp[index-1]+1}:30 \n [Google-Meet-link]({self.li[self.tt2[self.day_order[str(d)]][index-1]]})")
                    else:
                        emb.add_field(name="Ongoing class\t",value=f"**{self.tt2[self.day_order[str(d)]][index-1]}**\n *End time:* {self.timestamp[index-1]+1}:30 \n [Google-Meet-Link]({self.li[self.tt2[self.day_order[str(d)]][index-1]]})")
                if index!=4:
                    emb.add_field(name="Upcomming class",value=f"**{self.tt2[self.day_order[str(d)]][index]}**\n *Start time:* {self.timestamp[index]}:30 \n [Google-Meet-Link]({self.li[self.tt2[self.day_order[str(d)]][index]]})")
                embs.append(emb)

            else:
            
                d+=timedelta(days=1)
                i=0
                while(self.day_order[str(d)]=="Day-0"):
                    d+=timedelta(days=1)
                    i+=1
                
                embs.append(discord.Embed(title="End of "+self.day_order[str(d-timedelta(days=i+1))],description=f"*Next class in* {i} days, {9+24-d1.hour} hours"))
        
        if(len(embs)>1):
            await menu(
            ctx,
            embs,
            DEFAULT_CONTROLS,
            )
        else :
            await ctx.send(embed=embs[0])
        


    
    @link.command()
    async def mt(self,ctx,batch:int=None):
        """Displays the joining link of next class for MtechCse-II year"""
        
        
        d1=datetime.today()
        d=self.today
        j=-1
        while(self.day_order[str(d)]=="Day-0"):
            j+=1
            d+=timedelta(days=1)
        if(d!=self.today):
            emb=discord.Embed(title="Holiday",description=f"*Next class in* {j} days, {(9+24-d1.hour)%24} hours")
            emb.set_footer(text=self.day_order[str(d)])
            
            
        else:
            
            
            index=0
            while(index<4 and self.time.replace(hour=self.timestamp[index],minute=30,second=0)<self.time):
                index+=1
            if self.time.replace(hour=self.timestamp[index-1]+1,minute=30,second=0)>self.time:
                emb=discord.Embed(title="\tMtech "+f"{self.day_order[str(d)]}")
                
                
                if index!=0:
                    if(self.timestamp[index-1]+1<d1.hour or(self.timestamp[index-1]+1==d1.hour and d1.minute>=30)):
                        emb.add_field(name="Past class\t",value=f"**{self.mtechtt[self.day_order[str(d)]][index-1]}**\n *End time:* {self.timestamp[index-1]+1}:30 \n [Google-Meet-link]({self.li2[self.mtechtt[self.day_order[str(d)]][index-1]]})")
                    else:
                        emb.add_field(name="Ongoing class\t",value=f"**{self.mtechtt[self.day_order[str(d)]][index-1]}**\n *End time:* {self.timestamp[index-1]+1}:30 \n [Google-Meet-Link]({self.li2[self.mtechtt[self.day_order[str(d)]][index-1]]})")
                if(index!=4):
                    emb.add_field(name="Upcomming class",
                        value=f"**{self.mtechtt[self.day_order[str(d)]][index]}**\n*Start time:* {self.timestamp[index]}:30 \n[Google-Meet-Link]({self.li2[self.mtechtt[self.day_order[str(d)]][index]]})")

            else:
                
                d+=timedelta(days=1)
                i=0
                while(self.day_order[str(d)]=="Day-0"):
                    d+=timedelta(days=1)
                    i+=1
                emb=discord.Embed(title="End of "+self.day_order[str(d-timedelta(days=i+1))],description=f"*Next class in* {i} days, {9+24-d1.hour} hours")
                
        await ctx.send(embed=emb)
        

        #await ctx.send(msg)
    

        


