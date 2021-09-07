from __future__ import print_function
from typing import Literal
from datetime import date,datetime, timedelta

import discord
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.commands.commands import group
from redbot.core.config import Config
from redbot.core import config
from redbot.core.utils import chat_formatting as cf
from redbot.core.utils.menus import menu
from redbot.core.utils.menus import DEFAULT_CONTROLS

import pandas as pd
import os
from tabulate import tabulate
import os.path
from sys import path
import time
import requests
from bs4 import BeautifulSoup
import re

from . import res

'''
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]
'''


class navi(commands.Cog):
    """cog to maintain classroom things"""
    def __init__(self,bot):
        self.bot=bot
        
        self.config = Config.get_conf(
            self,
            identifier=12345,
            force_registration=False,
        )
        self.config.register_user(cls=None,batch=1,spam_dm=False)
        
        self.mapper={
            "cse3b": [res.cse3_b1, res.cse3_b2],
            "cse3c": [res.cse3_c1, res.cse3_c2],
            "cse2c": [res.cse2_c1, res.cse2_c2],
            "mtech2": [res.mtech2],
            "aids2": [res.aids2_b1, res.aids2_b2],
        }
        self.title_map = {
            "cse3b": "CSE III-B",
            "cse3c": "CSE III-C",
            "cse2c": "CSE II-C",
            "mtech2": "M.Tech II",
            "aids2": "AIDS II",
        }

        
        self.day_order=res.day_order
        
        self.cse3_b1tt=res.cse3_b1
        self.cse3_b2tt=res.cse3_b2
        self.today=date.today()
        self.li=res.links
        self.li2=res.linksmt
        self.li3=res.linkscse3b


        self.time=time.time()
        self.ttname="Unknown"
        self.t=self.today.ctime()
        self.timestamp=[9,10,13,14,15]
        self.tableheaders={4:["9:30","10:30", "1:30", "2:30"],5:["9:30","10:30", "1:30", "2:30","3:30"]}


        # rollnum things
        
        self.data=pd.read_csv("Dk-cogs/clsroom/resource/db.csv")
        self.ai_data=pd.read_csv("Dk-cogs/clsroom/resource/ai.csv")
        

    
    
    @commands.command()
    @commands.is_owner()
    async def gets(self,ctx,id:int):
        if (await self.config.user_from_id(id).cls())!=None:
            await ctx.send(await self.config.user_from_id(id).cls())
        else:
            await ctx.send("Noting registered under this user")

    @commands.is_owner()
    @commands.command()
    async def send_dm(self,ctx):
        usrs=await self.config.all_users()
        #for id,usr in usrs.items():
#            if usr['spam_dm']:
        id=497379893592719360
        await self.bot.get_user(id).send(self.link(ctx,id))

        await ctx.send(f"{ctx.message}")

        pass
        
        
    
    async def con(self,ctx,cls:str,usrid:int):
        """Connect usrid to cls
        """
        if cls not in ['aids2','cse3b','cse3c','cse2c','mtech2']:
            await ctx.send("Invalid class\navailable classes: > aids2,cse3b,cse3c,cse2c,mtech2")
        else:
            await self.config.user_from_id(usrid).cls.set(cls)
            await ctx.send("user registered with classid "+cls)


        #a=self.config()
        #a.user(ctx.author).nickname.set('bot boner')
        #pets = await self.config.user(ctx.author).pets()
        '''async with a.user_from_id(...).all() as u:
     u.name = ....
     u.nick   = ....'''
        
    
    @commands.command()
    async def connect(self,ctx,cls:str,batch:int):
        """Connect to your class and batch to get the link instantneously while using `[p]link` or `[p]timetable`
        Available departments:
        - aids2
        - cse2c
        - cse3b
        - cse3c
        - mtech2"""
        if cls not in self.mapper.keys():
            return await ctx.send_help()
        if len(self.mapper[cls])==1:
            batch=1;
        elif not batch or batch not in (1, 2):
            return await ctx.send("Kindly enter whether batch 1 or 2")
        
        async with self.config.user_from_id(ctx.author.id).all() as user_data:
            user_data["cls"] = cls
            user_data["batch"] = batch
        await ctx.send(f"user registered with class {cls} and batch {batch}")


    @commands.command()
    async def timetable(self,ctx):
        """`[p]timetable` displays the timetable registered under a discord user
Use `[p]connect` to register your class and batch"""

        self.today=date.today()

        async with self.config.user_from_id(ctx.author.id).all() as user_data:
            cls=user_data["cls"]
            batch=user_data["batch"]
            self.tt=self.mapper[cls][batch-1]
        
        if cls==None:
            return await ctx.send_help()

        
        table=[]
        size=len(list(self.mapper[cls][batch-1].values())[0])
        for i in self.mapper[cls][batch-1].keys():
            s=i+(' -> 'if i==self.day_order[str(self.today)] else '')
            table.append([s]+[*self.mapper[cls][batch-1][i]])
        

        return await menu(
            ctx,
            [
                cls+f"```{i} ```" + f"**Batch {batch}**" 
                for i in list([
                    
                        tabulate(
                            table,
                            headers=["", "9:30", "10:30", "1:30", "2:30", "3:30"],
                            tablefmt="presto",
                            colalign=("left",),
                        )]
                    
                )
            ],
            {"\N{CROSS MARK}": DEFAULT_CONTROLS["\N{CROSS MARK}"]},
            )
    
        if 8=='cse3b':#cse3b
            
            self.cse3_b1tt=res.cse3_b1
            self.cse3_b2tt=res.cse3_b2
            self.tableheaders=["9:30","10:30", "1:30", "2:30"]
            await self.cse(ctx)
        elif await self.config.user_from_id(ctx.author.id).cls()=='cse3c': #cse3c(sree)
            
            self.cse3_b1tt=res.cse3_c1
            self.cse3_b2tt=res.cse3_c2
            self.tableheaders=["9:30","10:30", "1:30", "2:30"]
            await self.cse(ctx)
        elif await self.config.user_from_id(ctx.author.id).cls()=='cse2c': #cse2c
            
            self.cse3_b1tt=res.cse2_c1
            self.cse3_b2tt=res.cse2_c2
            self.tableheaders=["9:30","10:30", "1:30", "2:30","3:30"]
            await self.cse(ctx)
        elif await self.config.user_from_id(ctx.author.id).cls()=='aids2':
            await self.aids2(ctx)
        elif await self.config.user_from_id(ctx.author.id).cls()=='mtech2':
            await self.mtech(ctx)

    #sdate = date(*[int(i)for i in sdate.split('-')])
    
    def cse(self,ctx):
        """Prints timetable of cse for registered users"""
        
        table1=[]
        table2=[]
        for i in self.cse3_b1tt.keys():
            if(i==self.day_order[str(self.today)]):
                s=i+' -> '
            else:
                s=i
            table1.append([s]+[self.cse3_b1tt[i][j]for j in range(len(self.tableheaders))])
        for i in self.cse3_b2tt.keys():
            if(i==self.day_order[str(self.today)]):
                s=i+' -> '
            else:
                s=i
            table2.append([s]+[self.cse3_b2tt[i][j]for j in range(len(self.tableheaders))])
        
        
        
        return menu(
            ctx,
            [
                self.ttname+f"```{i} ```" + f"**Batch {j+1}**" 
                for j,i in enumerate(list([
                    
                        tabulate(
                            table1,
                            headers=self.tableheaders,
                            tablefmt="presto",
                            colalign=("left",),
                        )
                        ,
                        tabulate(
                            table2,
                            headers=self.tableheaders,
                            tablefmt="presto",
                            colalign=("left",),
                        )]
                    
                ))
            ],
            DEFAULT_CONTROLS,
            )

    
    def mtech(self,ctx):
        
        table1=[]
        
        
        for i in self.mtechtt.keys():
            if(i==self.day_order[str(self.today)]):
                s=i+' -> '
            else:
                s=i
            table1.append([s]+[self.mtechtt[i][j]for j in range(4)])

        return menu(
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

    
    def aids2(self,ctx):
        """"""
        table1=[]
        table2=[]
        for i in self.tt1.keys():
            if(i==self.day_order[str(self.today)]):
                s=i+' -> '
            else:
                s=i
            table1.append([s]+[self.tt1[i][j]for j in range(5)])
        for i in self.tt2.keys():
            if(i==self.day_order[str(self.today)]):
                s=i+' -> '
            else:
                s=i
            table2.append([s]+[self.tt2[i][j]for j in range(5)])
        

        return menu(
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
    
    
    @commands.command(usage="")
    async def link(self,ctx,usr:int=None):
        """`[p]link` gives the clasroom meetlink of upcomming class
make sure to `[p]connect` before using this command
`[p]connect <department>` to connect to you class"""
        dm=True
        if not usr:
            usr=ctx.author.id
            dm=False

        self.today=date.today()
        self.time=datetime.now()#.strftime("%H:%M:%S")
        
        if await self.config.user_from_id(ctx.author).cls()=='cse3b':#cse3b
            self.ttname="CSE III B"
            self.li3=res.linkscse3b
            self.cse3_b1tt=res.cse3_b1
            self.cse3_b2tt=res.cse3_b2
            self.tableheaders=["9:30","10:30", "1:30", "2:30"]
            m=self.cs(ctx)
        #elif ctx.author.id.id in [497379893592719360]: #aids
        #    await ctx.send("check")
        elif await self.config.user_from_id(ctx.author.id).cls()=='cse3c': #cse3c(sree)
            self.ttname="CSE III C"
            self.li3=res.linkscse3c
            self.cse3_b1tt=res.cse3_c1
            self.cse3_b2tt=res.cse3_c2
            self.tableheaders=["9:30","10:30", "1:30", "2:30"]
            m=self.cs(ctx)
        elif await self.config.user_from_id(ctx.author.id).cls()=='cse2c': #cse2c
            self.ttname="CSE II C"
            self.li3=res.linkscse2c
            self.cse3_b1tt=res.cse2_c1
            self.cse3_b2tt=res.cse2_c2
            self.tableheaders=["9:30","10:30", "1:30", "2:30","3:30"]
            m=self.cs(ctx)
        elif await self.config.user_from_id(ctx.author.id).cls()=='mtech2': #
            m=self.mt(ctx)
        elif await self.config.user_from_id(ctx.author.id).cls()=='aids2': #
            m=self.ai(ctx)
        else:
            await ctx.send_help()
            return
        if dm:
            return m
        else:
            await m

        

        
    def ai(self,ctx,batch:int=None):
        """Displays the joining link of next class for AI-II year"""
        embs=[]
        
        d1=datetime.today()
        d=self.today
        j=-1
        while(self.day_order[str(d)]=="Day-0"):
            d+=timedelta(days=1)
            j+=1
        if(d!=self.today):
            emb=discord.Embed(title="Holiday",description=f"*Next class in* {j+(9+24-d1.hour)//24} days, {(9+24-d1.hour)%24} hours")
            emb.set_footer(text=self.day_order[str(d)])
            embs.append(emb)
            
        else:
            emb=discord.Embed(title="\tAIDS B1 "+f"{self.day_order[str(d)]}")
            
            index=0
            while(index<5 and self.time.replace(hour=self.timestamp[index],minute=30,second=0)<self.time):
                index+=1
            if self.time.replace(hour=self.timestamp[index-1]+1,minute=30,second=0)>self.time or index<5:
                
                    
                d1=datetime.today()
                if index!=0:
                    if(self.timestamp[index-1]+1<d1.hour or(self.timestamp[index-1]+1==d1.hour and d1.minute>=30)):
                        emb.add_field(name="Past class\t",value=f"**{self.tt1[self.day_order[str(d)]][index-1]}**\n *End time:* `{self.timestamp[index-1]+1}:30` \n [Google-Meet-link]({self.li[self.tt1[self.day_order[str(d)]][index-1]]})")
                    else:
                        emb.add_field(name="Ongoing class\t",value=f"**{self.tt1[self.day_order[str(d)]][index-1]}**\n *End time:* `{self.timestamp[index-1]+1}:30` \n [Google-Meet-link]({self.li[self.tt1[self.day_order[str(d)]][index-1]]})")
                if index !=5:
                    emb.add_field(name="Upcomming class",value=f"**{self.tt1[self.day_order[str(d)]][index]}**\n *Start time:* `{self.timestamp[index]}:30` \n [Google-Meet-link]({self.li[self.tt1[self.day_order[str(d)]][index]]})")
                    
                embs.append(emb)
                emb=discord.Embed(title="\tAIDS B2 "+f"{self.day_order[str(d)]}")
                
                if index!=0:
                    if(self.timestamp[index-1]+1<d1.hour or(self.timestamp[index-1]+1==d1.hour and d1.minute>=30)):
                        emb.add_field(name="Past class\t",value=f"**{self.tt2[self.day_order[str(d)]][index-1]}**\n *End time:* `{self.timestamp[index-1]+1}:30` \n [Google-Meet-link]({self.li[self.tt2[self.day_order[str(d)]][index-1]]})")
                    else:
                        emb.add_field(name="Ongoing class\t",value=f"**{self.tt2[self.day_order[str(d)]][index-1]}**\n *End time:* `{self.timestamp[index-1]+1}:30` \n [Google-Meet-Link]({self.li[self.tt2[self.day_order[str(d)]][index-1]]})")
                if index!=5:
                    emb.add_field(name="Upcomming class",value=f"**{self.tt2[self.day_order[str(d)]][index]}**\n *Start time:* `{self.timestamp[index]}:30` \n [Google-Meet-Link]({self.li[self.tt2[self.day_order[str(d)]][index]]})")

                embs.append(emb)

            else:
                d+=timedelta(days=1)
                i=0
                while(self.day_order[str(d)]=="Day-0"):
                    d+=timedelta(days=1)
                    i+=1
                

                embs.append(discord.Embed(title="End of "+self.day_order[str(d-timedelta(days=i+1))],description=f"*Next class in* {i} days, `{9+24-d1.hour}` hours"))
        
        if len(embs)>1:
            return menu(
                ctx,
                embs,
                DEFAULT_CONTROLS,
                )
        else:
            #await ctx.send(embed=embs[0])
            return menu(
                ctx,
                embs,
                {}
                )

    
    def cs(self,ctx):
        """Displays the joining link of next class for CSE"""
        #if(ctx.author.id):
        embs=[]
        
        d1=datetime.today()
        d=self.today
        j=-1
        while(self.day_order[str(d)]=="Day-0"):
            j+=1
            d+=timedelta(days=1)
        if(d!=self.today):
            emb=discord.Embed(title="Holiday",description=f"*Next class in* {j} days, `{(9+24-d1.hour)%24}` hours")
            emb.set_footer(text=self.day_order[str(d)])
            
            embs.append(emb)
            
        else:
            emb=discord.Embed(title=self.ttname+" batch-1\n"+f"{self.day_order[str(d)]}")
            
            index=0
            while(index<len(self.tableheaders) and self.time.replace(hour=self.timestamp[index],minute=30,second=0)<self.time):
                index+=1
            if self.time.replace(hour=self.timestamp[index-1]+1,minute=30,second=0)>self.time or index<len(self.tableheaders):
                
                d1=datetime.today()
                if index!=0:
                    if(self.timestamp[index-1]+1<d1.hour or(self.timestamp[index-1]+1==d1.hour and d1.minute>=30)):
                        emb.add_field(name="Past class\t",value=f"**{self.cse3_b1tt[self.day_order[str(d)]][index-1]}**\n *End time:* `{self.timestamp[index-1]+1}:30` \n [Google-Meet-link]({self.li3[self.cse3_b1tt[self.day_order[str(d)]][index-1]]})")
                    else:
                        emb.add_field(name="Ongoing class\t",value=f"**{self.cse3_b1tt[self.day_order[str(d)]][index-1]}**\n *End time:* `{self.timestamp[index-1]+1}:30` \n [Google-Meet-link]({self.li3[self.cse3_b1tt[self.day_order[str(d)]][index-1]]})")
                if(index!=len(self.tableheaders)):
                    emb.add_field(name="Upcomming class",value=f"**{self.cse3_b1tt[self.day_order[str(d)]][index]}**\n *Start time:* `{self.timestamp[index]}:30` \n [Google-Meet-link]({self.li3[self.cse3_b1tt[self.day_order[str(d)]][index]]})")
                embs.append(emb)
                
                emb=discord.Embed(title=self.ttname+" batch-2\n"+f"{self.day_order[str(d)]}")
                if index!=0:
                    if(self.timestamp[index-1]+1<d1.hour or(self.timestamp[index-1]+1==d1.hour and d1.minute>=30)):
                        emb.add_field(name="Past class\t",value=f"**{self.cse3_b2tt[self.day_order[str(d)]][index-1]}**\n *End time:* `{self.timestamp[index-1]+1}:30` \n [Google-Meet-link]({self.li3[self.cse3_b2tt[self.day_order[str(d)]][index-1]]})")
                    else:
                        emb.add_field(name="Ongoing class\t",value=f"**{self.cse3_b2tt[self.day_order[str(d)]][index-1]}**\n *End time:* `{self.timestamp[index-1]+1}:30` \n [Google-Meet-Link]({self.li3[self.cse3_b2tt[self.day_order[str(d)]][index-1]]})")
                if index!=len(self.tableheaders):
                    emb.add_field(name="Upcomming class",value=f"**{self.cse3_b2tt[self.day_order[str(d)]][index]}**\n *Start time:* `{self.timestamp[index]}:30` \n [Google-Meet-Link]({self.li3[self.cse3_b2tt[self.day_order[str(d)]][index]]})")
                embs.append(emb)

            else:
            
                d+=timedelta(days=1)
                i=0
                while(self.day_order[str(d)]=="Day-0"):
                    d+=timedelta(days=1)
                    i+=1
                
                embs.append(discord.Embed(title="End of "+self.day_order[str(d-timedelta(days=i+1))],description=f"*Next class in* {i} days, `{9+24-d1.hour}` hours"))
        
        if(len(embs)>1):
            return menu(
            ctx,
            embs,
            DEFAULT_CONTROLS,
            )
        else :
            #await ctx.send(embed=embs[0])
            return menu(
            ctx,
            embs,
            {}
            )
        

    def mt(self,ctx,batch:int=None):
        """Displays the joining link of next class for MtechCse-II year"""
        
        
        d1=datetime.today()
        d=self.today
        j=-1
        while(self.day_order[str(d)]=="Day-0"):
            j+=1
            d+=timedelta(days=1)
        if(d!=self.today):
            emb=discord.Embed(title="Holiday",description=f"*Next class in* {j} days, `{(9+24-d1.hour)%24}` hours")
            emb.set_footer(text=self.day_order[str(d)])
            
            
        else:
            
            
            index=0
            while(index<4 and self.time.replace(hour=self.timestamp[index],minute=30,second=0)<self.time):
                index+=1
            if self.time.replace(hour=self.timestamp[index-1]+1,minute=30,second=0)>self.time or index<4:
                emb=discord.Embed(title="\tMtech "+f"{self.day_order[str(d)]}")
                
                
                if index!=0:
                    if(self.timestamp[index-1]+1<d1.hour or(self.timestamp[index-1]+1==d1.hour and d1.minute>=30)):
                        emb.add_field(name="Past class\t",value=f"**{self.mtechtt[self.day_order[str(d)]][index-1]}**\n *End time:* `{self.timestamp[index-1]+1}:30` \n [Google-Meet-link]({self.li2[self.mtechtt[self.day_order[str(d)]][index-1]]})")
                    else:
                        emb.add_field(name="Ongoing class\t",value=f"**{self.mtechtt[self.day_order[str(d)]][index-1]}**\n *End time:* `{self.timestamp[index-1]+1}:30` \n [Google-Meet-Link]({self.li2[self.mtechtt[self.day_order[str(d)]][index-1]]})")
                if(index!=4):
                    emb.add_field(name="Upcomming class",
                        value=f"**{self.mtechtt[self.day_order[str(d)]][index]}**\n*Start time:* `{self.timestamp[index]}:30` \n[Google-Meet-Link]({self.li2[self.mtechtt[self.day_order[str(d)]][index]]})")

            else:
                
                d+=timedelta(days=1)
                i=0
                while(self.day_order[str(d)]=="Day-0"):
                    d+=timedelta(days=1)
                    i+=1
                emb=discord.Embed(title="End of "+self.day_order[str(d-timedelta(days=i+1))],description=f"*Next class in* {i} days, `{9+24-d1.hour}` hours")

        return menu(
            ctx,
            [emb],
            {}
            )       
        #return ctx.send(embed=emb)
        

    #rollnum cogs added here
    @commands.command()
    async def pnum(self,ctx,option):
        emb = discord.Embed(title="Details")
        emb.set_image(url=f"https://samwyc.codes/images/{option}.jpg")
        await menu(ctx,emb,{"\N{CROSS MARK}": DEFAULT_CONTROLS["\N{CROSS MARK}"]})

    @commands.command()
    async def rnum(self,ctx,option):
        """displays the details of roll number provided"""
        o=option.upper()
        #data.loc[data["r_no"]=='17EUCS001']
        #await ctx.send(self.data)
        d=self.data.loc[self.data["r_no"]==o]
        if len(d):
            emb = discord.Embed(title="Details")
            emb.add_field(name="Name",value=d.iloc[0]["name"]+' '+d.iloc[0]["s_name"])
            emb.add_field(name="Department",value=d.iloc[0]["dept"])
            emb.add_field(name="Roll No",value=d.iloc[0]["r_no"])
            emb.set_image(url=f"https://samwyc.codes/images/{option}.jpg")
            await menu(ctx,emb,{"\N{CROSS MARK}": DEFAULT_CONTROLS["\N{CROSS MARK}"]})
            """
            res='''`Name` {n} {n1}\n`Dept` {d1}\n`Roll` {r}'''.format(n=(d.iloc[0])["name"],n1=(d.iloc[0])["s_name"],d1=(d.iloc[0])["dept"],r=(d.iloc[0])["r_no"])
            await ctx.send(res)"""
        else:
            await ctx.send("Not found")

    @commands.command()
    async def sname(self,ctx,option):
        """search by name """
        a=option.upper()
        #d=self.data.loc[self.data["name"]==a]
        d=self.data[self.data["name"].str.contains(a,na=False)]
        i=1
        
        table=[]

        #search by first name
        for index,k in d.iterrows():
           table.append([i,str(k["name"])+' '+str(k["s_name"]),k["dept"],k["r_no"]])
           i+=1
        
        #search in second name
        d=self.data[self.data["s_name"].str.contains(a,na=False)]
        for index,k in d.iterrows():
           table.append([i,k["name"]+' '+k["s_name"],k["dept"],k["r_no"]])
           i+=1
        
        i=len(table)
        if i :
            li=list(
                    cf.pagify(
                        tabulate(
                            table,
                            headers=["Sno","Name", "Department", "Roll no"],
                            tablefmt="presto",
                            colalign=("left",),
                        ),page_length=1900
                    )
                )
            n=len(li)
            await menu(
            ctx,
            [
                f"```{i} ```" + f"**> Page {j+1} / {n}**"                 
                for j,i in enumerate(li)
            ],
            DEFAULT_CONTROLS,
            )
        else:
            await ctx.reply("No name matched with the data base")

    @commands.command()    
    async def aids(self,ctx,options:int):
        """get details of students of AIDS"""
        
        #data.loc[data["r_no"]=='17EUCS001']
        #await ctx.send(self.data)
        d=self.ai_data.loc[self.ai_data["S_No"]==options]
        try:
            emb = discord.Embed(title="Details")
            emb.add_field(name="Name",value=d.iloc[0]["Name"])
            emb.add_field(name="DOB",value=d.iloc[0]["DOB"])
            emb.add_field(name="Mobile",value=d.iloc[0]["Student_cell"])
            emb.add_field(name="Email",value=d.iloc[0]["Email_id"])
            emb.add_field(name="Address",value=d.iloc[0]["Per_Address"])
            
            #emb.set_image(url=f"https://samwyc.codes/images/20euai{options:03}.jpg")
            await menu(ctx,emb,{"\N{CROSS MARK}": DEFAULT_CONTROLS["\N{CROSS MARK}"]})
            
        except:
            await ctx.send("Not found")
    
    @commands.command()
    async def resai(self,ctx,serialnum:int):
        """display the result of semester happened in apr/mar"""
        month={'Jan':'01',
               'Feb':'02',
               'Mar':'03',
               'Apr':'04',
               'May':'05',
               'Jun':'06',
               'Jul':'07',
               'Aug':'08',
               'Sep':'09',
               'Oct':'10',
               'Nov':'11',
               'Dec':'12'
               }

        d=self.ai_data.loc[self.ai_data["S_No"]==serialnum]
        
        if len(d)==0:
            await ctx.reply("Wrong serial number")
            return
        dd=str(d.iloc[0]["DOB"]).split('-')
        dd[0],dd[1]=month[dd[1]],dd[0]
        dd='/'.join(dd)
        await self.result(ctx,f'20euai{serialnum:03}',dd)
        
        
        
        
    
    @commands.command()
    async def result(self,ctx,rollnum:str,dob:str):
        """display the result of semester happened in apr/mar"""
        async with ctx.typing():
            rollnum=rollnum.upper()
            
            dd=re.match('[0-9]{2}/[0-9]{2}/(1998|1999|2000|2001|2002|2003|2004)',dob)
            if(dd==None):
                await ctx.reply('Wrong dob Pattern')
                return
            
            r_form_data={
            "Srollno": rollnum,
            "Password": dob
            }
            
            r_headers={
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "Accept-Encoding": "gzip, deflate",
                    "Accept-Language": "en-US,en;q=0.5",
                    "Connection": "keep-alive",
                    "Content-Length": "41",
                    "Content-Type": "application/x-www-form-urlencoded",
                    #"Cookie": "ci_session=8geukb5t1h4t3nkqo82fa7l2l9ok49qi",
                    "Host": "results.skcet.ac.in:612",
                    "Origin":"http://results.skcet.ac.in:612",
                    "Referer": "http://results.skcet.ac.in:612/",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0"	
            }
            r=requests.post('http://results.skcet.ac.in:612/index.php/Welcome/Login',data=r_form_data,headers=r_headers)
            if(b"http://results.skcet.ac.in:612/assets/StudentImage/"+bytes(rollnum, encoding='utf8') not in r.content):
                await ctx.reply("Wrond dob or rollnum: "+rollnum+","+dob)
                return
            
            try:
                r.cookies.get_dict()['ci_session']
            except:
                await ctx.reply("There was a error loading the details")
                return
            
            r_headers1={
                'Host':'results.skcet.ac.in:612',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                #'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Referer': 'http://results.skcet.ac.in:612/index.php/Welcome/Login',
                #'Cookie': 'ci_session=mtq22fefrtr9l6l8djcjircu375h0mro',
                'Cookie': 'ci_session='+r.cookies.get_dict()['ci_session'],
                'Upgrade-Insecure-Requests': '1',
                }
            
            r1=requests.post('http://results.skcet.ac.in:612/index.php/Result',cookies=r.cookies,headers=r_headers1)
            soup=BeautifulSoup(r1.content,"html.parser")
            if soup.findAll('tr')==[]:
                """expection with cookies"""
                r_headers1={
                'Host':'results.skcet.ac.in:612',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                #'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Referer': 'http://results.skcet.ac.in:612/index.php/Welcome/Login',
                
                #'Cookie': 'ci_session='+r.cookies.get_dict()['ci_session'],
                'Cookie': 'ci_session=mtq22fefrtr9l6l8djcjircu375h0mro',
                'Upgrade-Insecure-Requests': '1',
                }
                r1=requests.post('http://results.skcet.ac.in:612/index.php/Result',cookies=r.cookies,headers=r_headers1)
                soup=BeautifulSoup(r1.content,"html.parser")
                if soup.findAll('tr')==[]:
                    await ctx.reply("Temporarry fix broken")
                    return
                #await ctx.send(str(soup.text)[:1999])
                #await ctx.send(str(soup.p.text))
                #await ctx.reply(f"bru Literally,... The site dont have the result of {rollnum}")
                
            b=[]
            for i in soup.findAll('tr'):
                a=i.findAll('td')
                s=[]
                for j in a:
                    if(len(j)==3):
                        j=j.find('span').contents
                    s.extend(j)
                b.append(s)
                


                
            try:
                await ctx.send('***'+str(soup.p.text)+'***'+'```'+tabulate(
                b[1:],
                headers=b[0],
                tablefmt="presto",
                colalign=("left",))+'```')
            except:
                await ctx.send(f"Somthing went wrong at the last moment")
                
    
    '''
    @commands.command()
    async def classes(self,ctx,options:int):
        """list down the classes available in classroom
        `[p]classes 10` prints the latest 10 classes created"""
        
        
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
        else:
            pass
            
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(self.creds.to_json())

        self.service = build('classroom', 'v1', credentials=self.creds)


        # Call the Classroom API
        results = self.service.courses().list(pageSize=options).execute()
        courses = results.get('courses', [])

        if not courses:
            await ctx.send('No courses found.')
        else:
            r="Courses: \n"
            await ctx.send(r+"\n".join([course['alternateLink']for course in courses]))

    
'''
