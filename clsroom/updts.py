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
        SCOPES = [
            "https://www.googleapis.com/auth/classroom.courses.readonly",
            "https://www.googleapis.com/auth/classroom.coursework.me",
            "https://www.googleapis.com/auth/classroom.announcements.readonly",
            "https://www.googleapis.com/auth/classroom.push-notifications",
            "https://www.googleapis.com/auth/classroom.courseworkmaterials.readonly",
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

    @commands.command()
    async def courses(self, ctx, count: int = 11):
        """Lists the top 10 courses"""
        courses = self.service.courses().list(pageSize=count).execute().get("courses", [])
        for c in courses:
            await ctx.send(f"{c['name']} - {c['id']}")
