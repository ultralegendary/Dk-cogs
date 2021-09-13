from __future__ import print_function

import os
import os.path
from datetime import date, datetime, timedelta, tzinfo
from typing import Literal

import discord
from discord.ext import tasks
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from pytz import timezone
from redbot.core import commands, config
from redbot.core.bot import Red
from redbot.core.commands.commands import group
from redbot.core.config import Config
from redbot.core.utils import chat_formatting as cf
from redbot.core.utils.menus import DEFAULT_CONTROLS, menu


class Updts(commands.Cog):
    def __init__(self, bot):
        self.config = Config.get_conf(
            self,
            identifier=12344,
            force_registration=False,
        )
        default_guild = {
            "courses": [],
            "teachers": [],
            "coursematerials": [],
            "coursework": [],
        }
        self.config.init_custom("CustomGuildGroup", 1)
        self.config.register_custom("CustomGuildGroup", **default_guild)

        self.config.register_guild(
            channel_id=None,
            guild_id=None,
        )

        SCOPES = [
            "https://www.googleapis.com/auth/classroom.courses.readonly",
            "https://www.googleapis.com/auth/classroom.coursework.me",
            "https://www.googleapis.com/auth/classroom.announcements.readonly",
            "https://www.googleapis.com/auth/classroom.push-notifications",
            "https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly",
            "https://www.googleapis.com/auth/classroom.rosters.readonly",
        ]
        os.environ["OAUTHLIB_RELAX_TOKEN_SCOPE"] = "1"
        creds = None
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        self.service = build("classroom", "v1", credentials=creds)
        self.bot = bot
        self.cscode = [
            "MS",
            "AI",
            "OOP",
            "MC",
            "OOP-LAB",
            "DBMS",
            "DBMS-LAB",
            "DAA",
            "FOS-LAB",
            "FOS",
            "A",
        ]
        self.update_courses.start()

    @commands.is_owner()
    @commands.command(name="update")
    async def update(self, ctx):
        """Update basic course details"""
        async with ctx.typing():
            reply = await ctx.send("Updating...")
            courses = self.service.courses().list().execute().get("courses", [])
            await self.config.custom("CustomGuildGroup", ctx.guild.id).courses.set(courses)
            teachers = []
            for c in courses[:11]:
                tech = (
                    self.service.courses()
                    .teachers()
                    .get(courseId=c["id"], userId=c["ownerId"])
                    .execute()
                )
                teachers.append(tech)

            await self.config.custom("CustomGuildGroup", ctx.guild.id).teachers.set(teachers)

        await ctx.tick()

    @commands.command()
    async def courses(self, ctx, count: int = 11):
        """Lists the latest courses"""
        async with ctx.typing():
            courses = await self.config.custom("CustomGuildGroup", ctx.guild.id).courses()
            await ctx.send("\n".join([f"{c['name']} , {c['section']}" for c in courses]))

    @commands.command()
    async def course(self, ctx, coursecode: str):
        """Display the details of a course"""

        if coursecode in self.cscode:
            async with ctx.typing():
                emb = discord.Embed(title="Course details")
                courses = await self.config.custom("CustomGuildGroup", ctx.guild.id).courses()
                teachers = await self.config.custom("CustomGuildGroup", ctx.guild.id).teachers()
                i = self.cscode.index(coursecode)
                course = courses[i]
                tech = teachers[i]

                """
            await ctx.send("Added sucessfully");"""

                emb.add_field(name="Section", value=course["section"])
                emb.add_field(name="Year", value=course["name"])

                emb.add_field(name="link", value=f"[link to class]({course['alternateLink']})")
                emb.add_field(name="Tutor name", value=f"{tech['profile']['name']['fullName']}")

                await ctx.send(embed=emb)

        else:
            await ctx.send("Invalid course code")

    @commands.is_owner()
    @commands.command()
    async def updatemat(self, ctx):
        """Update course materials and assingments"""

        async with ctx.typing():
            cm = []
            cw = []
            courses = await self.config.custom("CustomGuildGroup", ctx.guild.id).courses()
            for c in courses:
                cw.append(self.service.courses().courseWork().list(courseId=c["id"]).execute())
                cm.append(
                    self.service.courses().courseWorkMaterials().list(courseId=c["id"]).execute()
                )

            await self.config.custom("CustomGuildGroup", ctx.guild.id).coursematerials.set(cm)
            await self.config.custom("CustomGuildGroup", ctx.guild.id).coursework.set(cw)

        await ctx.tick()

    @tasks.loop(seconds=600)
    async def update_courses(self):
        """updates and posts unposted materials into mentioned channel"""
        print("YES")
        channel = await self.config.guild_from_id(781133714306105394).channel_id()
        v = await self.config.custom("CustomGuildGroup", 781133714306105394).coursematerials()
        c = await self.config.custom("CustomGuildGroup", 781133714306105394).courses()
        t = await self.config.custom("CustomGuildGroup", 781133714306105394).teachers()
        w = await self.config.custom("CustomGuildGroup", 781133714306105394).coursework()

        for v1, c1, w1, t1, i in zip(v[:11], c[:11], w[:11], t[:11], range(11)):
            p = 0

            new = (
                self.service.courses()
                .courseWorkMaterials()
                .list(courseId=c1["id"], pageSize=5)
                .execute()
            )
            # await ctx.send(f"```{t1}``` {c1['id']}")
            if "courseWorkMaterial" in new.keys():

                for i in new["courseWorkMaterial"]:
                    vv1 = v1["courseWorkMaterial"][p]
                    p += 1

                    if i["id"] != vv1["id"]:
                        emb = discord.Embed(
                            title=f"{t1['profile']['name']['fullName']} : Posted New material"
                        )
                    elif i["id"] == vv1["id"] and i["updateTime"] != vv1["updateTime"]:
                        emb = discord.Embed(
                            title=f"{t1['profile']['name']['fullName']} : Updated a material"
                        )
                    else:
                        break
                    # emp.add_field(name="Course",value=f"{c1['name']}  {c1['section']}")
                    emb.add_field(name="Course", value=f"{c1['name']}  {c1['section']}")
                    emb.add_field(
                        name="Link to the original post",
                        value=f"[Original post link]({vv1['alternateLink']})",
                    )
                    emb.add_field(
                        name="Description",
                        value=(
                            vv1["description"] if "description" in vv1.keys() else "No description"
                        ),
                    )
                    if "title" in vv1.keys():
                        emb.add_field(name="Title", value=f"{i['title']}")
                    d1 = (
                        datetime.strptime(
                            vv1["creationTime"].split(".")[0],
                            "%Y-%m-%dT%H:%M:%S",
                        )
                        + timedelta(hours=5, minutes=30)
                    )
                    d1 = d1.strftime("%d-%m-%Y  %a %H:%M")

                    d2 = (
                        datetime.strptime(
                            vv1["updateTime"].split(".")[0],
                            "%Y-%m-%dT%H:%M:%S",
                        )
                        + timedelta(hours=5, minutes=30)
                    )
                    d2 = d2.strftime("%d-%m-%Y  %a %H:%M")

                    color = discord.Color.random()
                    # await ctx.send(str(vv1.keys())[:1000])
                    if "materials" in vv1.keys():

                        for j in vv1["materials"]:
                            emb1 = emb
                            # emp.add_field(name="Course",value=f"{c1['name']}  {c1['section']}")

                            l = list(j.keys())
                            # await ctx.send(f"{j}")
                            if l[0] == "link":
                                emb1.add_field(
                                    name="LINK",
                                    value=f"[{j['link']['title']}]({j['link']['url']})",
                                )

                            elif l[0] == "driveFile":
                                emb1.add_field(
                                    name="DRIVEFILE",
                                    value=f"[{j['driveFile']['driveFile']['title']}]({j['driveFile']['driveFile']['alternateLink']})",
                                )

                            elif l[0] == "youtubeVideo":
                                emb1.add_field(
                                    name=f"YOUTUBEVEDIO",
                                    value=f"[{j['youtubeVideo']['title']}]({j['youtubeVideo']['alternateLink']})",
                                )

                            elif l[0] == "form":
                                emb1.add_field(
                                    name="FORM",
                                    value=f"[j['form']['title']]({j['form']['formUrl']})",
                                )

                        if "updateTime" in l:
                            emb1.add_field(name="Last updated", value=f"{j['updateTime']}")
                        emb1.set_footer(text=f"{c1['section']}")

                        emb1.add_field(name="Creation time: ", value=d1)
                        emb1.add_field(name="Last updated: ", value=d2)
                        # await self.bot.get_channel(channel).send(embed=emb1)

                    else:
                        # emb=discord.Embed(title=f"{t1['profile']['name']['fullName']} Posted New material")
                        # emp.add_field(name="Course",value=f"{c1['name']}  {c1['section']}")
                        emb1 = emb

                        emb1.add_field(name="Creation time: ", value=d1)
                        emb1.add_field(name="Last updated: ", value=d2)
                        # await ctx.send(channel)
                        # await self.bot.get_channel(channel).send(embed=emb1)

            q = 0
            new = self.service.courses().courseWork().list(courseId=c1["id"], pageSize=5).execute()
            # await ctx.send(f"```{t1}``` {c1['id']}")

            if "courseWork" in new.keys():

                for i in new["courseWork"]:
                    vv1 = w1["courseWork"][q]
                    q += 1

                    if i["id"] != vv1["id"]:
                        emb = discord.Embed(
                            title=f"{t1['profile']['name']['fullName']} : Posted new Assignment",
                            color=discord.Color.random(),
                        )
                    elif i["id"] == vv1["id"] and i["updateTime"] != vv1["updateTime"]:
                        emb = discord.Embed(
                            title=f"{t1['profile']['name']['fullName']} : Updated a Assignment",
                            color=discord.Color.random(),
                        )
                    else:
                        break
                    # emp.add_field(name="Course",value=f"{c1['name']}  {c1['section']}")
                    emb.add_field(name="Course", value=f"{c1['name']}  {c1['section']}")
                    emb.add_field(
                        name="Link to the original post",
                        value=f"[Original post link]({vv1['alternateLink']})",
                    )
                    emb.add_field(
                        name="Description",
                        value=(
                            vv1["description"] if "description" in vv1.keys() else "No description"
                        ),
                    )
                    if "dueDate" in vv1.keys():
                        d1 = (
                            datetime(
                                year=vv1["dueDate"]["year"],
                                month=vv1["dueDate"]["month"],
                                day=vv1["dueDate"]["day"],
                                hour=vv1["dueTime"]["hours"],
                                minute=vv1["dueTime"]["minutes"],
                            )
                            + timedelta(hours=5, minutes=30)
                        )
                        d1 = d1.strftime("%d-%m-%Y  %a %H:%M")
                    else:
                        d1 = "No due date"
                    d2 = datetime.strptime(
                        vv1["updateTime"].split(".")[0], "%Y-%m-%dT%H:%M:%S"
                    ) + timedelta(hours=5, minutes=30)
                    d2 = d2.strftime("%d-%m-%Y  %a %H:%M")

                    # await ctx.send(str(vv1.keys())[:1000])

                    if "materials" in vv1.keys():

                        for j in vv1["materials"]:
                            emb1 = emb

                            # emp.add_field(name="Course",value=f"{c1['name']}  {c1['section']}")

                            l = list(j.keys())
                            # await ctx.send(f"{j}")
                            if l[0] == "link":
                                emb1.add_field(
                                    name="LINK",
                                    value=f"[{j['link']['title']}]({j['link']['url']})",
                                )
                            elif l[0] == "driveFile":
                                emb1.add_field(
                                    name="DRIVEFILE",
                                    value=f"[{j['driveFile']['driveFile']['title']}]({j['driveFile']['driveFile']['alternateLink']})",
                                )

                            elif l[0] == "youtubeVideo":
                                emb1.add_field(
                                    name=f"YOUTUBEVEDIO",
                                    value=f"[{j['youtubeVideo']['title']}]({j['youtubeVideo']['alternateLink']})",
                                )

                            elif l[0] == "form":
                                emb1.add_field(
                                    name="FORM",
                                    value=f"[j['form']['title']]({j['form']['formUrl']})",
                                )

                        if "updateTime" in l:
                            emb1.add_field(
                                name="Last updated", value=f"{j['updateTime']}"
                            )  # waste code ig

                        emb1.set_footer(text=f"{c1['section']}")

                        emb1.add_field(name="DUE: ", value=d1)
                        emb1.add_field(name="Last updated: ", value=d2)
                        await self.bot.get_channel(channel).send(embed=emb1)

                    else:
                        # emb=discord.Embed(title=f"{t1['profile']['name']['fullName']} Posted New material")
                        # emp.add_field(name="Course",value=f"{c1['name']}  {c1['section']}")
                        emb1 = emb

                        emb1.add_field(name="Creation time: ", value=d1)
                        emb1.add_field(name="Last updated: ", value=d2)
                        # await ctx.send(channel)
                        await self.bot.get_channel(channel).send(embed=emb1)

        # await ctx.tick()

    @update_courses.before_loop
    async def before_update_courses(self):
        await self.bot.wait_until_ready()

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def chmat(self, ctx, toogle: bool):
        """Toogle course material for a channel"""
        async with self.config.guild(ctx.guild).all() as ch:
            if toogle:
                ch["channel_id"] = ctx.channel.id
            else:
                ch["channel_id"] = None
        await ctx.tick()

    @commands.command()
    async def materials(self, ctx, coursecode: str):
        """Display the materials for the course"""
        if coursecode in self.cscode:
            async with ctx.typing():
                courses = await self.config.custom("CustomGuildGroup", ctx.guild.id).courses()
                i = self.cscode.index(coursecode)
                course = courses[i]
                materials = await self.config.custom(
                    "CustomGuildGroup", ctx.guild.id
                ).coursematerials()
                courseworks = await self.config.custom(
                    "CustomGuildGroup", ctx.guild.id
                ).coursework()
                material = materials[i]
                a = 1
                for c in material["courseWorkMaterial"]:
                    color = discord.Color.random()
                    if "materials" in c.keys():
                        d1 = (
                            datetime.strptime(c["creationTime"].split(".")[0], "%Y-%m-%dT%H:%M:%S")
                            .replace(tzinfo=timezone("Asia/Kolkata"))
                            .strftime("%d-%m-%Y  %a %H:%M")
                        )
                        d2 = (
                            datetime.strptime(c["updateTime"].split(".")[0], "%Y-%m-%dT%H:%M:%S")
                            .replace(tzinfo=timezone("Asia/Kolkata"))
                            .strftime("%d-%m-%Y  %a %H:%M")
                        )

                        for j in c["materials"]:
                            emb = discord.Embed(title=f"{c['title']}", color=color)
                            emb.add_field(
                                name="Link to the original post",
                                value=f"[Original post link]({c['alternateLink']})",
                            )
                            emb.add_field(
                                name="Description",
                                value=(
                                    c["description"]
                                    if "description" in c.keys()
                                    else "No description"
                                ),
                            )

                            l = list(j.keys())
                            # await ctx.send(f"{j}")
                            if l[0] == "link":
                                emb.add_field(
                                    name=j["link"]["title"],
                                    value=f"[link to Website]({j['link']['url']})",
                                )

                            elif l[0] == "driveFile":
                                emb.add_field(
                                    name=j["driveFile"]["driveFile"]["title"],
                                    value=f"[link to driveFile]({j['driveFile']['driveFile']['alternateLink']})",
                                )

                            elif l[0] == "youtubeVedio":
                                emb.add_field(
                                    name=f"Youtube vedio: {j['youtubeVedio']['title']}",
                                    value=f"[link]({j['youtubeVedio']['alternateLink']})",
                                )

                            if "updateTime" in l:
                                emb.add_field(name="Last updated", value=f"{j['updateTime']}")
                            emb.set_footer(text=f"{coursecode}-{course['section']}")
                            a += 1
                            emb.add_field(name="Creation time: ", value=d1)
                            emb.add_field(name="Last updated: ", value=d2)

                            await ctx.send(embed=emb)
                            # emb.add_field(name=j['title'],value=)
                    else:
                        emb = discord.Embed(title=f"{c['title']}", color=color)
                        emb.add_field(
                            name="Link to the original post",
                            value=f"[Original post link]({c['alternateLink']})",
                        )
                        emb.add_field(
                            name="Description",
                            value=(
                                c["description"] if "description" in c.keys() else "No description"
                            ),
                        )
                        emb.add_field(name="Creation time: ", value=d1)
                        emb.add_field(name="Last updated: ", value=d2)
                        emb.set_footer(text=f"{coursecode}-{course['section']}")
                        await ctx.send(embed=emb)
