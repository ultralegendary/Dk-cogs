from __future__ import print_function

import os
import os.path
from datetime import date, datetime, timedelta
from typing import Literal

import discord
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
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
        }
        # self.config.init_custom("CustomGuildGroup", 1)
        # self.config.register_custom("CustomGuildGroup", **default_guild)

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

    @commands.is_owner()
    @commands.command(name="update")
    async def update_cls(self, ctx):
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

            await ctx.send("Done!")

    @commands.command()
    async def courses(self, ctx, count: int = 11):
        """Lists the latest courses"""
        async with ctx.typing():
            courses = await self.config.custom("CustomGuildGroup", ctx.guild.id).courses()
            await ctx.send("\n".join([f"{c['name']} , {c['id']}" for c in courses]))

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
