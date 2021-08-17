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

'''
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
'''
RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]

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
        self.tableheaders=["9:30","10:30", "1:30", "2:30"]


        # rollnum things
        
        self.data=pd.read_csv("Dk-cogs/clsroom/resource/db.csv")
        self.ai_data=pd.read_csv("Dk-cogs/clsroom/resource/ai.csv")
        self.config = Config.get_conf(
            self,
            identifier=12345,
            force_registration=True,
        )

    '''
        self.SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly']
        self.creds=None
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())

        self.service = build('classroom', 'v1', credentials=self.creds)
    '''



    @commands.group()
    async def timetable(self,ctx):
        """`[p]timetable department` displays the timetable of the department"""
        self.today=date.today()
        if ctx.author.id in [453158855904591872]:#cse3b
            self.ttname="CSE III B TIMETABLE"
            self.cse3_b1tt=res.cse3_b1
            self.cse3_b2tt=res.cse3_b2
            self.tableheaders=["9:30","10:30", "1:30", "2:30"]
            

        #elif ctx.author.id in [497379893592719360]: #aids
        #    await ctx.send("check")
        elif ctx.author.id in [650735047569047552]: #cse3c(sree)
            self.ttname="CSE III C TIMETABLE"
            self.li3=res.linkscse3b
            self.cse3_b1tt=res.cse3_c1
            self.cse3_b2tt=res.cse3_c2
            self.tableheaders=["9:30","10:30", "1:30", "2:30"]
        elif ctx.author.id in [778438128527867915,497379893592719360]: #cse2b
            self.ttname="CSE II C TIMETABLE"
            self.cse3_b1tt=res.cse2_c1
            self.cse3_b2tt=res.cse2_c2
            self.tableheaders=["9:30","10:30", "1:30", "2:30","3:30"]

            


        
        
        #sdate = date(*[int(i)for i in sdate.split('-')])
        
    @timetable.command()
    async def cse(self,ctx):
        """Prints timetable of cse for registered users"""
        table1=[]
        table2=[]
        for i in self.cse3_b1tt.keys():
            table1.append([i]+[self.cse3_b1tt[i][j]for j in range(len(self.tableheaders))])
        for i in self.cse3_b2tt.keys():
            table2.append([i]+[self.cse3_b2tt[i][j]for j in range(len(self.tableheaders))])

        await menu(
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
    async def aids2(self,ctx):
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
        
        if ctx.author.id in [453158855904591872]:#cse3b
            self.li3=res.linkscse3b
            self.cse3_b1tt=res.cse3_b1
            self.cse3_b2tt=res.cse3_b2
            self.tableheaders=["9:30","10:30", "1:30", "2:30"]
            

        #elif ctx.author.id in [497379893592719360]: #aids
        #    await ctx.send("check")
        elif ctx.author.id in [650735047569047552]: #cse3c(sree)
            self.li3=res.linkscse3c
            self.cse3_b1tt=res.cse3_c1
            self.cse3_b2tt=res.cse3_c2
            self.tableheaders=["9:30","10:30", "1:30", "2:30"]
        elif ctx.author.id in [778438128527867915]: #cse2b
            self.li3=res.linkscse2c
            self.cse3_b1tt=res.cse2_c1
            self.cse3_b2tt=res.cse2_c2
            self.tableheaders=["9:30","10:30", "1:30", "2:30","3:30"]

        
        
        
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
            if self.time.replace(hour=self.timestamp[index-1]+1,minute=30,second=0)>self.time or index<5:
                
                    
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
            while(index<len(self.tableheaders) and self.time.replace(hour=self.timestamp[index],minute=30,second=0)<self.time):
                index+=1
            if self.time.replace(hour=self.timestamp[index-1]+1,minute=30,second=0)>self.time or index<len(self.tableheaders):
                
                d1=datetime.today()
                if index!=0:
                    if(self.timestamp[index-1]+1<d1.hour or(self.timestamp[index-1]+1==d1.hour and d1.minute>=30)):
                        emb.add_field(name="Past class\t",value=f"**{self.cse3_b1tt[self.day_order[str(d)]][index-1]}**\n *End time:* {self.timestamp[index-1]+1}:30 \n [Google-Meet-link]({self.li3[self.cse3_b1tt[self.day_order[str(d)]][index-1]]})")
                    else:
                        emb.add_field(name="Ongoing class\t",value=f"**{self.cse3_b1tt[self.day_order[str(d)]][index-1]}**\n *End time:* {self.timestamp[index-1]+1}:30 \n [Google-Meet-link]({self.li3[self.cse3_b1tt[self.day_order[str(d)]][index-1]]})")
                if(index!=len(self.tableheaders)):
                    emb.add_field(name="Upcomming class",value=f"**{self.cse3_b1tt[self.day_order[str(d)]][index]}**\n *Start time:* {self.timestamp[index]}:30 \n [Google-Meet-link]({self.li3[self.cse3_b1tt[self.day_order[str(d)]][index]]})")
                embs.append(emb)
                
                emb=discord.Embed(title="\tCSE-B B2 "+f"{self.day_order[str(d)]}")
                if index!=0:
                    if(self.timestamp[index-1]+1<d1.hour or(self.timestamp[index-1]+1==d1.hour and d1.minute>=30)):
                        emb.add_field(name="Past class\t",value=f"**{self.cse3_b2tt[self.day_order[str(d)]][index-1]}**\n *End time:* {self.timestamp[index-1]+1}:30 \n [Google-Meet-link]({self.li3[self.cse3_b2tt[self.day_order[str(d)]][index-1]]})")
                    else:
                        emb.add_field(name="Ongoing class\t",value=f"**{self.cse3_b2tt[self.day_order[str(d)]][index-1]}**\n *End time:* {self.timestamp[index-1]+1}:30 \n [Google-Meet-Link]({self.li3[self.cse3_b2tt[self.day_order[str(d)]][index-1]]})")
                if index!=len(self.tableheaders):
                    emb.add_field(name="Upcomming class",value=f"**{self.cse3_b2tt[self.day_order[str(d)]][index]}**\n *Start time:* {self.timestamp[index]}:30 \n [Google-Meet-Link]({self.li3[self.cse3_b2tt[self.day_order[str(d)]][index]]})")
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
            if self.time.replace(hour=self.timestamp[index-1]+1,minute=30,second=0)>self.time or index<4:
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
        

    #rollnum cogs added here
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
            await ctx.send(embed=emb)
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
            #emb.add_field(name="Mobile",value=d.iloc[0]["Student_cell"])
            #emb.add_field(name="Email",value=d.iloc[0]["Email_id"])
            #emb.add_field(name="Address",value=d.iloc[0]["Per_Address"])
            
            emb.set_image(url=f"https://samwyc.codes/images/20euai{options:03}.jpg")
            await ctx.send(embed=emb,)
            
        except:
            await ctx.send("Not found")
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
