from __future__ import print_function

import os
import os.path
from typing import Literal

import discord
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from redbot.core import commands
from redbot.core.bot import Red
from redbot.core.config import Config
from redbot.core.utils import chat_formatting as cf
from redbot.core.utils.menus import DEFAULT_CONTROLS, menu
from tabulate import tabulate

RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]


class rollnum(commands.Cog):
    """
    cog to display college member details
    """

    def __init__(self, bot: Red) -> None:
        self.bot = bot

        self.data = pd.read_csv("Dk-cogs/rollnum/resource/db.csv")
        self.ai_data = pd.read_csv("Dk-cogs/rollnum/resource/ai.csv")
        self.config = Config.get_conf(
            self,
            identifier=12345,
            force_registration=True,
        )

        self.SCOPES = ["https://www.googleapis.com/auth/classroom.courses.readonly"]
        self.creds = None
        if os.path.exists("token.json"):
            self.creds = Credentials.from_authorized_user_file("token.json", self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(self.creds.to_json())

        self.service = build("classroom", "v1", credentials=self.creds)
        results = self.service.courses().list(pageSize=10).execute()
        courses = results.get("courses", [])

    async def red_delete_data_for_user(self, *, requester: RequestType, user_id: int) -> None:
        # TODO: Replace this with the proper end user data removal handling.
        super().red_delete_data_for_user(requester=requester, user_id=user_id)

    @commands.command()
    async def rnum(self, ctx, option):
        """displays the details of roll number provided"""
        o = option.upper()
        # data.loc[data["r_no"]=='17EUCS001']
        # await ctx.send(self.data)
        d = self.data.loc[self.data["r_no"] == o]
        if len(d):
            emb = discord.Embed(title="Details")
            emb.add_field(name="Name", value=d.iloc[0]["name"] + " " + d.iloc[0]["s_name"])
            emb.add_field(name="Department", value=d.iloc[0]["dept"])
            emb.add_field(name="Roll No", value=d.iloc[0]["r_no"])
            emb.set_image(url=f"https://samwyc.codes/images/{option}.jpg")
            await ctx.send(embed=emb)
            """
            res='''`Name` {n} {n1}\n`Dept` {d1}\n`Roll` {r}'''.format(n=(d.iloc[0])["name"],n1=(d.iloc[0])["s_name"],d1=(d.iloc[0])["dept"],r=(d.iloc[0])["r_no"])
            await ctx.send(res)"""
        else:
            await ctx.send("Not found")

    @commands.command()
    async def sname(self, ctx, option):
        """search by name"""
        a = option.upper()
        # d=self.data.loc[self.data["name"]==a]
        d = self.data[self.data["name"].str.contains(a, na=False)]
        i = 1

        table = []

        # search by first name
        for index, k in d.iterrows():
            table.append([i, str(k["name"]) + " " + str(k["s_name"]), k["dept"], k["r_no"]])
            i += 1

        # search in second name
        d = self.data[self.data["s_name"].str.contains(a, na=False)]
        for index, k in d.iterrows():
            table.append([i, k["name"] + " " + k["s_name"], k["dept"], k["r_no"]])
            i += 1

        i = len(table)
        if i:
            n = len(
                list(
                    cf.pagify(
                        tabulate(
                            table,
                            headers=["Sno", "Name", "Department", "Roll no"],
                            tablefmt="presto",
                            colalign=("left",),
                        )
                    )
                )
            )
            await menu(
                ctx,
                [
                    f"```{i} ```" + f"** > Page {j+1} / {n}**"
                    for j, i in enumerate(
                        list(
                            cf.pagify(
                                tabulate(
                                    table,
                                    headers=["Sno", "Name", "Department", "Roll no"],
                                    tablefmt="presto",
                                    colalign=("left",),
                                )
                            )
                        )
                    )
                ],
                DEFAULT_CONTROLS,
            )
        else:
            await ctx.reply("No name matched with the data base")
            # await ctx.send_interactive(cf.pagify(cf.box(tabulate(table,headers=["Name","Department","Roll no"],tablefmt="pretty"))))

    """
    @commands.is_owner()
    @commands.group()
    async def pls():
     #blah blah

    @pls.command()
    async def p(...):
    # auisfhslef"""
    '''
    @commands.group()
    async def aids(self,ctx):
        """get details of students of AIDS"""
        #data.loc[data["r_no"]=='17EUCS001']
        #await ctx.send(self.data)
    @aids.command()    
    async def p(self,ctx,options:int,op:str=None):
        """get details of students of AIDS"""
        
        #data.loc[data["r_no"]=='17EUCS001']
        #await ctx.send(self.data)
        d=self.ai_data.loc[self.ai_data["S_No"]==options]
        if 1:
            emb = discord.Embed(title="Details")
            emb.add_field(name="Name",value=d.iloc[0]["Name"])
            emb.add_field(name="DOB",value="hidden")
            
            emb.set_thumbnail(url=f" https://samwyc.codes/images/20euai{options:03}.jpg")
            await ctx.send(embed=emb)
            
        else:
            await ctx.send("Not found")'''

    @commands.command()
    async def aids(self, ctx, options: int):
        """get details of students of AIDS"""

        # data.loc[data["r_no"]=='17EUCS001']
        # await ctx.send(self.data)
        d = self.ai_data.loc[self.ai_data["S_No"] == options]
        try:
            emb = discord.Embed(title="Details")
            emb.add_field(name="Name", value=d.iloc[0]["Name"])
            emb.add_field(name="DOB", value=d.iloc[0]["DOB"])

            emb.set_image(url=f"https://samwyc.codes/images/20euai{options:03}.jpg")
            await ctx.send(embed=emb)

        except:
            await ctx.send("Not found")

    @commands.command()
    async def classes(self, ctx, options: int):
        """list down the classes available in classroom
        `[p]classes 10` prints the latest 10 classes created"""

        if os.path.exists("token.json"):
            self.creds = Credentials.from_authorized_user_file("token.json", self.SCOPES)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
        else:
            pass
            """flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', self.SCOPES)
            self.creds = flow.run_local_server(port=0)"""
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(self.creds.to_json())

        self.service = build("classroom", "v1", credentials=self.creds)

        # Call the Classroom API
        results = self.service.courses().list(pageSize=options).execute()
        courses = results.get("courses", [])

        if not courses:
            await ctx.send("No courses found.")
        else:
            r = "Courses: \n"
            await ctx.send(r + "\n".join([course["alternateLink"] for course in courses]))
