from typing import Dict, List, Literal
import datetime as dt

import discord
from discord import user
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


"""
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
"""
RequestType = Literal["discord_deleted_user", "owner", "user", "user_strict"]


class navi(commands.Cog):
    """cog to maintain classroom things"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=12345,
            force_registration=True,
        )
        self.config.register_user(dept=None, batch=None)

        self.ref_time = [9, 10, 13, 14, 15]
        self.mapper = {
            "cse3b": [res.cse3_b1, res.cse3_b2],
            "mtech": [res.mtech],
            "aids": [res.aids_b1, res.aids_b2],
        }

        # rollnum things
        self.data = pd.read_csv(
            os.path.abspath(__file__ + "/../../") + "\\rollnum\\resource\\db.csv"
        )
        self.ai_data = pd.read_csv(
            os.path.abspath(__file__ + "/../../") + "\\rollnum\\resource\\ai.csv"
        )
        self.config = Config.get_conf(
            self,
            identifier=12345,
            force_registration=True,
        )

    """
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
    """

    @commands.command()
    async def connect(self, ctx, dept, batch):
        if dept not in ["cse3b", "mtech", "aids"]:
            return await ctx.send(
                "Invalid department. Please choose from `cse3b`, `mtech` or `aids`"
            )
        # TODO remove hardcode
        if dept == "mtech":
            batch = 1
        elif not batch:
            return await ctx.send("Kindly enter whether batch 1 or 2")

        async with self.config.user_from_id(ctx.author.id).all() as user_data:
            user_data["dept"] = dept
            user_data["batch"] = batch

        await ctx.send(
            f"Sucessfully registered as department {dept}"
            + (f"and batch {batch}" if batch else "")
        )

    @commands.command(aliases=["tt"])
    async def timetable(self, ctx, dept: str = None, batch: int = None):
        """`[p]timetable department` displays the timetable of the department

        Available departments:
        - `cse3b`
        - `mtech`
        - `aids`"""

        user_data = await self.config.user_from_id(ctx.author.id).all()
        if not dept:
            if user_data["dept"] and user_data["batch"]:
                dept = user_data["dept"]
                batch = int(user_data["batch"])
            else:
                return await ctx.send_help()
        else:
            if dept not in ["cse3b", "mtech", "aids"]:
                return await ctx.send(
                    "Invalid department. Please choose from `cse3b`, `mtech` or `aids`"
                )
            # TODO remove hardcode
            if dept == "mtech":
                batch = 1
            elif not batch:
                return await ctx.send("Kindly enter whether batch 1 or 2")

        if dept not in self.mapper:
            return await ctx.send_help()

        table = tabulate(
            [[k] + [period for period in v] for k, v in self.get_sub_obj(dept, batch).items()],
            headers=["9:30", "10:30", "1:30", "2:30"],
            tablefmt="presto",
            colalign=("left",),
        )

        await menu(
            ctx,
            [f"{dept.upper()}  **Batch {batch}** TimeTable ```{table} ``"],
            {"\N{CROSS MARK}": DEFAULT_CONTROLS["\N{CROSS MARK}"]},
        )

    @commands.group(aliases=["links"])
    async def link(self, ctx, dept=None, batch: int = None):
        """Setup up link using `[p]connect` else give your department and batch number

        Available departments:
        - `cse3b`
        - `aids`
        - `mtech`"""
        user_data = await self.config.user_from_id(ctx.author.id).all()
        if not dept:
            if user_data["dept"] and user_data["batch"]:
                dept = user_data["dept"]
                batch = int(user_data["batch"])
            else:
                return await ctx.send_help()
        else:
            if dept not in ["cse3b", "mtech", "aids"]:
                return await ctx.send(
                    "Invalid department. Please choose from `cse3b`, `mtech` or `aids`"
                )
            # TODO remove hardcode
            if dept == "mtech":
                batch = 1
            elif not batch:
                return await ctx.send("Kindly enter whether batch 1 or 2")

        # Prep stuff
        embs = []

        # Getting correct time things
        time_now = dt.datetime.now()
        time_now.replace(hour=time_now.hour + 1)
        day_order = res.day_order[time_now.strftime("%Y-%m-%d")]

        # Get next working day
        tmrw = time_now + dt.timedelta(days=1)
        while res.day_order[tmrw.strftime("%Y-%m-%d")][-1] == "0":
            tmrw += dt.timedelta(days=1)
        next_class_day = tmrw.replace(hour=9, minute=30) - time_now

        # Holiday
        if day_order[-1] == "0":
            # Hardcoded timedelta
            emb = discord.Embed(
                title="Holiday",
                description=f"*Next class in* {cf.humanize_timedelta(timedelta=next_class_day)}",
            )
            emb.set_footer(text=day_order)
            embs.append(emb)
        # Working day :(
        else:
            emb = discord.Embed(title=f"{dept.upper()} {batch or ''} - {day_order}")
            dept_links = getattr(res, dept + "_links")
            # Getting period hour
            if time_now.hour < self.ref_time[0]:
                subject = self.get_sub_obj(dept, batch)[day_order][0]
                emb.add_field(
                    name="Upcomming class",
                    value=f"**{subject}**\n *Start time:* {self.ref_time[0]}:30 \n [Google-Meet-link]({dept_links[subject]})",
                )
            else:
                for hr_index in range(len(self.ref_time) - 1):
                    if self.ref_time[hr_index] <= time_now.hour < self.ref_time[hr_index + 1]:

                        # TODO Check this out later, time inbetweens are not working
                        hr_index -= 1

                        # If it's greater than 30mins then it's the next hour
                        if time_now.minute > 30 and time_now.hour + 1 in self.ref_time:
                            hr_index += 1

                        subject = self.get_sub_obj(dept, batch)[day_order][hr_index]
                        emb.add_field(
                            name="Ongoing class",
                            value=f"**{subject}**\n *End time:* {self.ref_time[hr_index+1]}:30 \n [Google-Meet-link]({dept_links[subject]})",
                        )
                        # There exists the next class
                        if hr_index < len(self.get_sub_obj(dept, batch)[day_order]) - 1:
                            subject = self.get_sub_obj(dept, batch)[day_order][hr_index + 1]
                            emb.add_field(
                                name="Upcoming class",
                                value=f"**{subject}**\n *Start time:* {self.ref_time[hr_index+1]}:30 \n [Google-Meet-link]({dept_links[subject]})",
                            )
                        break
                else:
                    # Likely Last hour TODO hardcoded
                    if not (time_now.hour >= 15 and time_now.minute > 30):
                        subject = self.get_sub_obj(dept, batch)[day_order][-1]
                        emb.add_field(
                            name="Ongoing class",
                            value=f"**{subject}**\n *End time:* {self.ref_time[-1]}:30 \n [Google-Meet-link]({dept_links[subject]})",
                        )

                # We are in the last hour
                if len(emb.fields) <= 1:
                    emb.add_field(
                        name="End",
                        value=f"Next class in {cf.humanize_timedelta(timedelta=next_class_day)}",
                    )
            embs.append(emb)

            # For now there is only one page, let's add more later
            await menu(
                ctx,
                embs,
                DEFAULT_CONTROLS
                if len(embs) > 1
                else {"\N{CROSS MARK}": DEFAULT_CONTROLS["\N{CROSS MARK}"]},
            )

    # rollnum cogs added here
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
        """search by name """
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
                        ),
                        page_length=1900,
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
                                ),
                                page_length=1900,
                            )
                        )
                    )
                ],
                DEFAULT_CONTROLS,
            )
        else:
            await ctx.reply("No name matched with the data base")

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

    def get_sub_obj(self, dept, batch=None):
        mini = self.mapper[dept]
        if not batch:
            batch = 1
        return mini[batch - 1]

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
