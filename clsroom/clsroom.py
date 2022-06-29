import datetime as dt
import os
import os.path
import re
import time
from sys import path
from typing import Literal

import aiohttp
import discord
import pandas as pd
import requests
from bs4 import BeautifulSoup
from dateutil.tz import gettz
from discord.ext import tasks
from pytz import timezone
from redbot.core import commands, config
from redbot.core.config import Config
from redbot.core.utils import chat_formatting as cf
from redbot.core.utils.menus import DEFAULT_CONTROLS, menu
from tabulate import tabulate

from . import res

class ClsRoom(commands.Cog):
    """cog to maintain classroom things"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(
            self,
            identifier=12345,
            force_registration=False,
        )
        self.config.register_user(dept=None, batch=None, dm=False, ctx=None)
        

        self.config1 = Config.get_conf(
            self,
            identifier=12334,
            force_registration=False,
        )

        self.config1.register_user(Name=[], dob=[],last_activity="")


        self.ref_time = [dt.time(hr, (30 if hr>10 else 15)) for hr in [9, 10, 11, 12]]
        self.mapper = {
            "cse3b": [res.cse3b_b1, res.cse3b_b2],
            "cse3c": [res.cse3c_b1, res.cse3c_b2],
            "cse2c": [res.cse2c_b1, res.cse2c_b2],
            "mtech2": [res.mtech2],
            "aids2": [res.aids_b1, res.aids_b2],
        }

        self.title_map = {
            "cse3b": "CSE III-B",
            "cse3c": "CSE III-C",
            "cse2c": "CSE II-C",
            "mtech2": "M.Tech CSE II",
            "aids2": "AIDS II",
        }

        # rollnum things
    
        self.stud_data=pd.read_csv(
            os.path.join(os.path.abspath(__file__ + "/../../"), "clsroom/resource/sk_data_v4.csv")
        )

        self.data=self.stud_data.copy().drop(columns=['Unnamed: 0'])
        self.data['Name']=self.data.Name.str.upper()
        self.data['Fathername']=self.data.Fathername.str.upper()


        self.ai_data = pd.read_csv(
            os.path.join(os.path.abspath(__file__ + "/../../"), "clsroom/resource/ai.csv")
        )
        
        self.spam_dob.start()
        # self.spam_link.start()

    def cog_unload(self):
        self.spam_dob.cancel()
        pass
        # self.spam_link.cancel()
    @tasks.loop(hours=24)
    async def spam_dob(self):
        """send remainder to dob remainder on date mentioned"""
        now = dt.datetime.now(tz=gettz("Asia/Kolkata")).strftime("%d%m")
        v = await self.config1.all_users()
        # print(v)
        for user in v:
            if v[user]["last_activity"]==now:
                return
            await self.config1.user_from_id(user).last_activity.set(now)
            v[user]["last_activity"]=now
            dobs=v[user]["dob"]
            
            for i,date in enumerate(dobs):
                if date[:4]==now:
                    emb=discord.Embed(title="See who's birthday it is!", description="One of your friend seems to celebrate birthday today!", color=0x9732a8)
                    emb.add_field(name="Name", value=v[user]["Name"][i])
                    emb.add_field(name="DOB", value=v[user]["dob"][i][:2]+"-"+v[user]["dob"][i][2:4]+"-"+v[user]["dob"][i][4:])
                    await self.bot.get_user(user).send(embed=emb)
        #update config1

    @spam_dob.before_loop
    async def before_spam_dob(self):
        await self.bot.wait_until_ready()
        


    @tasks.loop(seconds=300)
    async def spam_link(self):
        """dm class link to registered users before 5 mins class starts"""
        now = dt.datetime.now(tz=gettz("Asia/Kolkata"))

        t = now.replace(minute=(30 if now.hour>10 else 15)) - now

        if now.hour in [9, 10, 11, 12] and t.seconds <= 300 and t.seconds > 0:

            v = await self.config.all_users()
            for user in v:
                if v[user]["dm"]:
                    a = await self.link(user)
                    if a and self.bot.get_user(user):
                        await self.bot.get_user(user).send(embed=a)

    @commands.command(aliases=["sal"])
    @commands.is_owner()
    async def sendalllinks(self, ctx):
        """send all class link to registered users"""
        now = dt.datetime.now(tz=gettz("Asia/Kolkata"))
        v = await self.config.all_users()

        for user in v:
            if v[user]["dm"]:
                await self.bot.get_user(user).send("Due to bot down today, links are sent now")
                for i in [9, 10, 11, 12]:
                    n = now.replace(hour=i, minute=25)

                    a = await self.link(user, None, None, n)
                    if a:
                        await self.bot.get_user(user).send(embed=a)

    @spam_link.before_loop
    async def before_printer(self):
        await self.bot.wait_until_ready()

    @commands.command()
    async def dmlinks(self, ctx, toggle: bool):
        """Set toggle to Send link of the class to join in dm before 5 mins\nuse `[p] dmlinks false` to not spam in your dm"""
        await ctx.tick()
        if toggle:
            usr_msg = await ctx.author.send(
                f"{ctx.author.mention} You have registered to dm links before 5 mins of class starts.\n To stop this service, use `$dmlinks false`"
            )

        async with self.config.user_from_id(ctx.author.id).all() as user_data:
            user_data["dm"] = toggle

    @commands.command(aliases=["con"])
    async def connect(self, ctx, dept, batch: int = None):
        """Connect to your class and batch to get the link instantneously while using [p]link or [p]timetable

        Available departments:
        - aids2
        - cse2c
        - cse3b
        - cse3c
        - mtech2
        """
        if dept not in self.mapper.keys():
            return await ctx.send(
                "Invalid department. Please choose from:\n"
                + ", ".join(f"`{i}`" for i in self.mapper.keys())
            )
        if len(self.mapper[dept]) == 1:
            batch = 1
        elif not batch or batch not in (1, 2):
            return await ctx.send("Kindly enter whether batch 1 or 2")

        async with self.config.user_from_id(ctx.author.id).all() as user_data:
            user_data["dept"] = dept
            user_data["batch"] = batch

        await ctx.send(
            f"Sucessfully registered as department {dept}"
            + (f" and batch {batch}" if batch else "")
        )

    # Util function to get subject_object
    def get_sub_obj(self, dept, batch=None):
        mini = self.mapper[dept]
        if not batch:
            batch = 1
        return mini[batch - 1]

    @commands.command()
    async def leaves(self, ctx, verbose: bool = False):
        """Get the list of holidays for fun"""
        holidays = ""
        time_now = dt.datetime.now(tz=gettz("Asia/Kolkata"))
        tmrw = time_now + dt.timedelta(days=1)
        while True:
            try:
                if res.day_order[tmrw.strftime("%Y-%m-%d")][-1] == "0":
                    if verbose or not tmrw.weekday() in (5, 6):
                        holidays += f"{tmrw.strftime('`%d/%m/%y` : **%A**')}\n"
                tmrw += dt.timedelta(days=1)
            except KeyError:
                break

        embs = []
        pages = list(cf.pagify(holidays, page_length=1000, shorten_by=0))
        no_of_pages = len(pages)
        for pgno, page in enumerate(pages, 1):
            embs.append(
                discord.Embed(title="Holiday Calender", description=page).set_footer(
                    text=f"Page {pgno}/{no_of_pages}"
                )
            )

        await menu(
            ctx,
            pages=embs,
            controls=DEFAULT_CONTROLS
            if len(embs) > 1
            else {"\N{CROSS MARK}": DEFAULT_CONTROLS["\N{CROSS MARK}"]},
        )

    @commands.command(aliases=["tt"])
    async def timetable(self, ctx, dept: str = None, batch: int = None):
        """`[p]timetable department` displays the timetable of the department

        Available departments:
        - aids2
        - cse2c
        - cse3b
        - cse3c
        - mtech2
        """
        try:
            user_data = await self.config.user_from_id(ctx.author.id).all()
            time_now = dt.datetime.now(tz=gettz("Asia/Kolkata"))
            day_order = res.day_order[time_now.strftime("%Y-%m-%d")]
        except KeyError:
            e=discord.Embed(title="No Day-order found")
            e.add_field(name="no timetable exist", value="will update soon")
            return await ctx.send(embed=e)

        if not dept:
            if user_data["dept"] and user_data["batch"]:
                dept = user_data["dept"]
                batch = int(user_data["batch"])
            else:
                return await ctx.send_help()
        else:
            if dept not in self.mapper.keys():
                return await ctx.send(
                    "Invalid department. Please choose from:\n"
                    + ", ".join(f"`{i}`" for i in self.mapper.keys())
                )
            if len(self.mapper[dept]) == 1:
                batch = 1
            elif not batch or batch not in (1, 2):
                return await ctx.send(
                    f"Kindly enter whether batch 1 or 2\n Example: {ctx.message.content.split(' ')[0]} aids2 1"
                )

        if dept not in self.mapper:
            return await ctx.send_help()
        if not self.get_sub_obj(dept, batch) :
            return await ctx.send("No timetable found for this department")
        table = tabulate(
            [
                [k + " -->" if day_order == k else k] + [period for period in v]
                for k, v in self.get_sub_obj(dept, batch).items()
            ],
            headers=["", "9:15", "10:15", "11:30", "12:30", "1:30"],
            tablefmt="presto",
            colalign=("left",),
        )

        return await menu(
            ctx,
            [f"{self.title_map[dept]}  **Batch {batch}** TimeTable```{table}```"],
            {"\N{CROSS MARK}": DEFAULT_CONTROLS["\N{CROSS MARK}"]},
        )

    @commands.command(aliases=["links"], usage="[dept] [batch]")
    async def link(self, ctx, dept=None, batch: int = None, ext=None):
        """Get the link to the gmeet of your department

        Connect your class using `[p]connect` or else give your department and batch number

        Available departments:
        - aids2
        - cse2c
        - cse3b
        - cse3c
        - mtech2
        """
        is_dm = type(ctx) is int
        user_data = await self.config.user_from_id(ctx if is_dm else ctx.author.id).all()
        if not dept:
            if user_data["dept"] and user_data["batch"]:
                dept = user_data["dept"]
                batch = int(user_data["batch"])
            else:
                return await ctx.send_help()
        else:
            if dept not in self.mapper.keys():
                return await ctx.send(
                    "Invalid department. Please choose from:\n"
                    + ", ".join(f"`{i}`" for i in self.mapper.keys())
                )
            if len(self.mapper[dept]) == 1:
                batch = 1
            elif not batch or batch not in (1, 2):
                return await ctx.send("Kindly enter whether batch 1 or 2")

        # Prep stuff
        embs = []

        # Getting correct time things
        time_now = ext if ext else dt.datetime.now(tz=gettz("Asia/Kolkata"))
        try:
            day_order = res.day_order[time_now.strftime("%Y-%m-%d")]

            # Get next working day
            tmrw = time_now + dt.timedelta(days=1)
            while res.day_order[tmrw.strftime("%Y-%m-%d")][-1] == "0":
                tmrw += dt.timedelta(days=1)
        except KeyError:
            #no timetable
            e=discord.Embed(title="Cant find day-order")
            e.add_field(name="no timetable exist", value="will update soon")
            return await ctx.send(embed=e)

        # Hardcoded timedelta
        next_class_day = tmrw.replace(hour=9, minute=30) - time_now

        # Holiday
        if day_order[-1] == "0":
            if is_dm:
                return None
            emb = discord.Embed(
                title="Holiday",
                description=f"Next class in {cf.humanize_timedelta(timedelta=next_class_day)}",
                color=discord.Color.orange(),
            )

            emb.set_footer(
                text=f"Next day order {res.day_order[(time_now + next_class_day).strftime('%Y-%m-%d')]}"
            )

            # emb.add_field(name="Your first class on the next working day", value=sub[0])
            embs.append(emb)

        # Working day :(
        else:
            emb = discord.Embed(color=discord.Color.green())
            emb.set_footer(text=f"{day_order}  |  Batch-{batch}")
            emb.set_author(name=self.title_map[dept])
            if dept in ["cse2c","cse3b"]:
                dept_links=getattr(res, dept+str(batch) + "_links")
            else:
                dept_links = getattr(res, dept + "_links")
            try:
                sub_obj = self.get_sub_obj(dept, batch)[day_order]
            except KeyError:
                e=discord.Embed(title="Your time table is not with us!")
                
                if is_dm:
                    if dt.datetime.now().hour ==9:
                        e.add_field(name="No timetable exist for your class and you have registered for dm links", value="Classes are back online!, send your time table to me {dhiva}#1852")
                        return e
                    return None
                else:
                    e.add_field(name="No timetable exist for your class and you are asking for links?", value="Classes are back online!, send your time table to me {dhiva}#1852")
                    return await ctx.send(embed=e)

                
            time_obj = time_now.time()
            # time_obj = dt.time(16, 28) #debug

            # Before First class
            if time_obj < self.ref_time[0]:
                subject = sub_obj[0]
                emb.add_field(
                    name="Upcomming class",
                    value=f"**{subject}**\n Start time: `{self.ref_time[0].strftime('%I:%M %p')}`\n [Google-Meet-link]({dept_links[subject]})",
                )

            else:
                for hr_index in range(len(self.ref_time) - 1):
                    if self.ref_time[hr_index] <= time_obj < self.ref_time[hr_index + 1]:
                        subject = sub_obj[hr_index]
                        end_time = (
                            dt.datetime.combine(dt.date.today(), self.ref_time[hr_index])
                            + dt.timedelta(hours=1)
                        ).time()
                        emb.add_field(
                            name=(
                                "Ongoing"
                                if end_time > time_obj or end_time == self.ref_time[hr_index + 1]
                                else "Past"
                            )
                            + " class",
                            value=f"**{subject}**\n End time: `{end_time.strftime('%I:%M %p')}`\n [Google-Meet-link]({dept_links[subject]})",
                        )

                        # There exists a next class
                        if hr_index < len(sub_obj) - 1:
                            subject = sub_obj[hr_index + 1]
                            if subject != "NILL":
                                emb.add_field(
                                    name="Upcoming class",
                                    value=f"**{subject}**\n Start time: `{self.ref_time[hr_index+1].strftime('%I:%M %p')}`\n [Google-Meet-link]({dept_links[subject]})",
                                )
                            elif is_dm and subject == "NILL":
                                return None
                        break
                else:
                    subject = sub_obj[-1]
                    # We are in the last hour
                    if (
                        time_obj
                        < dt.time(hour=self.ref_time[-1].hour + 1, minute=self.ref_time[-1].minute)
                        and subject != "NILL"
                    ):
                        if is_dm:
                            return None
                        emb.add_field(
                            name="Ongoing class",
                            value=f"**{subject}**\n *End time:* {self.ref_time[-1].strftime('%I:%M %p')} \n [Google-Meet-link]({dept_links[subject]})",
                        )

                if len(emb.fields) <= 1 and is_dm:
                    return None

                if len(emb.fields) <= 1:
                    emb.add_field(
                        name="End",
                        value=f"Next class in {cf.humanize_timedelta(timedelta=next_class_day)}",
                    )
            embs.append(emb)

        # For now there is only one page, let's add more later
        if not is_dm:
            await menu(
                ctx,
                embs,
                DEFAULT_CONTROLS
                if len(embs) > 1
                else {"\N{CROSS MARK}": DEFAULT_CONTROLS["\N{CROSS MARK}"]},
            )
        else:
            return embs[0]

    # rollnum cogs added here
    @commands.command()
    async def pnum(self, ctx, option):
        """displayes photos of given roll number"""
        rollnumber = option.upper()
        
        n='s.skcet.ac.in:611'
        if rollnumber[2:3]=='B':
            n='.skasc.ac.in:810'
        if rollnumber[-3:].isdigit():
            r=int(rollnumber[-3:])
        else:
            return await ctx.send("Invalid roll number")            
        rollnumber=rollnumber[:-3]
        l=[]
        for i in range(r,r+100):
            url=f"http://result{n}/assets/StudentImage/{rollnumber}{i:03}.jpg"
            emb = discord.Embed(title=f"{rollnumber}{i:03}")
            emb.set_image(url=url)
            l.append(emb)
        
        await menu(ctx, l, DEFAULT_CONTROLS)

    @commands.command()
    async def rn(self, ctx, option):
        """displays the details of roll number provided"""
        o = option.upper()
        # data.loc[data["r_no"]=='17EUCS001']
        # await ctx.send(self.data)
        d = self.data.loc[self.data["r_no"] == o]
        if len(d):
            emb = discord.Embed(title="Details")
            emb.add_field(
                name="Name",
                value=str(d.iloc[0]["name"]) + " " + str(d.iloc[0]["s_name"]),
            )
            emb.add_field(name="Department", value=d.iloc[0]["dept"])
            emb.add_field(name="Roll No", value=d.iloc[0]["r_no"])
            emb.set_image(url=f"http://results.skcet.ac.in:611/assets/StudentImage/{option}.jpg")
            await menu(ctx, [emb], {"\N{CROSS MARK}": DEFAULT_CONTROLS["\N{CROSS MARK}"]})
            """
            res='''`Name` {n} {n1}\n`Dept` {d1}\n`Roll` {r}'''.format(n=(d.iloc[0])["name"],n1=(d.iloc[0])["s_name"],d1=(d.iloc[0])["dept"],r=(d.iloc[0])["r_no"])
            await ctx.send(res)"""
        else:
            await ctx.send("Not found")

    @commands.command()
    async def rnum(self, ctx, rollnumber: str):
        """Fetch information about the given rollnumber of a person
`API` calls moved to [p]rrnum"""
        rollnumber = rollnumber.upper()
        d=self.stud_data[self.stud_data.Rno==rollnumber]
        emb = discord.Embed(
            title="Given roll number not found, try using `rrnum` instead",
            color=await ctx.embed_color(),
        )
        if len(d):
            d=self.stud_data[self.stud_data.Rno==rollnumber].iloc[0]
            emb.title=d['Name'].split()[0].capitalize()+ "'s Details"
            for i in dict(d):
                if 'Unnamed' in i:
                    continue
                emb.add_field(
                    name=i,
                    value=d[i],
                )
            emb.set_thumbnail(url=f"http://results.skcet.ac.in:611/assets/StudentImage/{rollnumber}.jpg")
            
        return await ctx.send(embed=emb)

    @commands.command()
    async def rrnum(self, ctx, rollnumber: str):
        """Fetch information about the given rollnumber of a person"""
        rollnumber = rollnumber.upper()
        KEY='tyut54yh56thtgh'
        url=f"http://results.skcet.ac.in:611/assets/StudentImage/{rollnumber}.jpg"
        if rollnumber[2:3]=='B':
            KEY='d564fe54f231d65f4'
            url=f"http://result.skasc.ac.in:810/assets/StudentImage/{rollnumber}.jpg"

        head1 = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"
        }
        head2 = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://pgw.srikrishna.ac.in",
            "Connection": "keep-alive",
            "Referer": "https://pgw.srikrishna.ac.in/index.php/?key=%s" % KEY,
            
            "Upgrade-Insecure-Requests": "1",
        }
        async with ctx.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "https://pgw.srikrishna.ac.in/index.php/?key=%s" % KEY,
                    headers=head1,
                ) as resp:
                    if resp.status != 200:
                        return await ctx.send("Server down, try again later")
                async with session.post(
                    "https://pgw.srikrishna.ac.in/index.php/Welcome/Dashboard",
                    headers=head2,
                    data={"RollNo": rollnumber},
                ) as resp:
                    if resp.status != 200:
                        return await ctx.send("Server down, try again later")
                    soup = BeautifulSoup(await resp.text(), "html.parser")
                emb = discord.Embed(
                    title="Something went wrong, User not found",
                    color=await ctx.embed_color(),
                )
                for thing in soup.findAll(id=lambda L: L and L.startswith("student_")):
                    emb.add_field(
                        name=thing["id"].replace("student_", "").capitalize(),
                        value=thing.text.title()if thing.text.title() else "​",
                    )
                    if thing["id"] == "student_name":
                        emb.title = thing.text.split()[0].capitalize() + "'s Details"
                emb.set_thumbnail(url=url)
                
                await ctx.send(embed=emb)

    @commands.command()
    async def sname(self, ctx, name):
        """search by name"""
        name = name.upper()
        # d=self.data.loc[self.data["name"]==a]
        d = self.data[self.data["Name"].str.contains(name, na=False)]
        i = 1

        table = []

        # search by first name
        for index, k in d.iterrows():
            table.append([i, str(k["Name"]) , str(k["Fathername"]), k["Stream"], k["Rno"]])
            i += 1

        # search in second name
        d = self.data[self.data["Fathername"].str.contains(name, na=False)]
        for index, k in d.iterrows():
            table.append([i, str(k["Name"]) , str(k["Fathername"]), k["Stream"], k["Rno"]])
            i += 1

        i = len(table)
        if i:
            li = list(
                cf.pagify(
                    tabulate(
                        table,
                        headers=["Sno","Name", "Father name", "Department", "Roll no"],
                        tablefmt="presto",
                        colalign=("left",),
                    ),
                    page_length=1900,
                )
            )
            n = len(li)
            await menu(
                ctx,
                [f"```{i} ```" + f"**> Page {j+1} / {n}**" for j, i in enumerate(li)],
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
        if len(d):
            emb = discord.Embed(title="Details", color=discord.Color.dark_green())
            emb.add_field(name="Name", value=d.iloc[0]["Name"])
            emb.add_field(name="DOB", value=d.iloc[0]["DOB"])
            emb.add_field(name="Mobile", value=d.iloc[0]["Student_cell"])
            emb.add_field(name="Email", value=d.iloc[0]["Email_id"])
            emb.add_field(name="Address", value=d.iloc[0]["Per_Address"])

            # emb.set_image(url=f"https://samwyc.codes/images/20euai{options:03}.jpg")
            await menu(ctx, [emb], {"\N{CROSS MARK}": DEFAULT_CONTROLS["\N{CROSS MARK}"]})

        else:
            await ctx.send("Not found")

    @commands.command()
    async def resai(self, ctx, serialnum: int):
        """display the result of semester happened in apr/mar"""
        month = {
            "Jan": "01",
            "Feb": "02",
            "Mar": "03",
            "Apr": "04",
            "May": "05",
            "Jun": "06",
            "Jul": "07",
            "Aug": "08",
            "Sep": "09",
            "Oct": "10",
            "Nov": "11",
            "Dec": "12",
        }

        d = self.ai_data.loc[self.ai_data["S_No"] == serialnum]

        if len(d) == 0:
            return await ctx.reply("Wrong serial number")

        dd = str(d.iloc[0]["DOB"]).split("-")
        dd[0], dd[1] = month[dd[1]], dd[0]
        dd = "/".join(dd)
        await self.result(ctx, f"20euai{serialnum:03}", dd)

    @commands.command()
    async def result(self, ctx, rollnum: str, dob: str):
        """display the result of semester happened in apr/mar"""
        async with ctx.typing():
            rollnum = rollnum.upper()

            dd = re.match("[0-9]{2}/[0-9]{2}/(1998|1999|2000|2001|2002|2003|2004)", dob)
            if dd == None:
                await ctx.reply("Wrong dob Pattern")
                return

            r_form_data = {"Srollno": rollnum, "Password": dob}

            r_headers = {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "en-US,en;q=0.5",
                "Connection": "keep-alive",
                "Content-Length": "41",
                "Content-Type": "application/x-www-form-urlencoded",
                # "Cookie": "ci_session=8geukb5t1h4t3nkqo82fa7l2l9ok49qi",
                "Host": "results.skcet.ac.in:611",
                "Origin": "http://results.skcet.ac.in:611",
                "Referer": "http://results.skcet.ac.in:611/",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
            }
            r = requests.post(
                "http://results.skcet.ac.in:611/index.php/Welcome/Login",
                data=r_form_data,
                headers=r_headers,
            )
            if (
                b"http://results.skcet.ac.in:611/assets/StudentImage/"
                + bytes(rollnum, encoding="utf8")
                not in r.content
            ):
                await ctx.reply("Wrond dob or rollnum: " + rollnum + "," + dob)
                return

            try:
                r.cookies.get_dict()["ci_session"]
            except:
                await ctx.reply("There was a error loading the details")
                return

            r_headers1 = {
                "Host": "results.skcet.ac.in:611",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
                #'Accept-Encoding': 'gzip, deflate',
                "Connection": "keep-alive",
                "Referer": "http://results.skcet.ac.in:611/index.php/Welcome/Login",
                #'Cookie': 'ci_session=mtq22fefrtr9l6l8djcjircu375h0mro',
                "Cookie": "ci_session=" + r.cookies.get_dict()["ci_session"],
                "Upgrade-Insecure-Requests": "1",
            }

            r1 = requests.post(
                "http://results.skcet.ac.in:611/index.php/Result",
                cookies=r.cookies,
                headers=r_headers1,
            )
            soup = BeautifulSoup(r1.content, "html.parser")
            if soup.findAll("tr") == []:
                """expection with cookies"""
                r_headers1 = {
                    "Host": "results.skcet.ac.in:611",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.5",
                    #'Accept-Encoding': 'gzip, deflate',
                    "Connection": "keep-alive",
                    "Referer": "http://results.skcet.ac.in:611/index.php/Welcome/Login",
                    #'Cookie': 'ci_session='+r.cookies.get_dict()['ci_session'],
                    "Cookie": "ci_session=mtq22fefrtr9l6l8djcjircu375h0mro",
                    "Upgrade-Insecure-Requests": "1",
                }
                r1 = requests.post(
                    "http://results.skcet.ac.in:611/index.php/Result",
                    cookies=r.cookies,
                    headers=r_headers1,
                )
                soup = BeautifulSoup(r1.content, "html.parser")
                if soup.findAll("tr") == []:
                    await ctx.reply("Temporarry fix broken")
                    return
                # await ctx.send(str(soup.text)[:1999])
                # await ctx.send(str(soup.p.text))
                # await ctx.reply(f"bru Literally,... The site dont have the result of {rollnum}")

            b = []
            for i in soup.findAll("tr"):
                a = i.findAll("td")
                s = []
                for j in a:
                    if len(j) == 3:
                        j = j.find("span").contents
                    s.extend(j)
                b.append(s)

            try:
                await ctx.send(
                    "***"
                    + soup.p.text
                    + "***"
                    + "```"
                    + tabulate(b[1:], headers=b[0], tablefmt="presto", colalign=("left",))
                    + "```"
                )
            except:
                await ctx.send(f"Somthing went wrong at the last moment")


    @commands.group(pass_context=True)
    async def bday(self, ctx):
        '''remainds of a person birthday'''

    @bday.command()
    async def add(self, ctx,name:str,dob:str):
        '''add birth date to reminder
        date pattern: `ddmmyyyy`'''
        if len(dob) != 8:
            await ctx.send_help()
            return
        try:
            dt.datetime.strptime(dob, "%d%m%Y")
        except:
            await ctx.send_help()
            return
        await ctx.reply("Added dob successfully, you will be reminded on the birth date if i am alive")
        async with self.config1.user_from_id(ctx.author.id).all() as user_data:
            user_data['dob'].append( dob)
            user_data['Name'].append( name)
    
    @bday.command(name="list")
    async def blist(self, ctx):
        '''list all your birth dates for a user'''
        async with self.config1.user_from_id(ctx.author.id).all() as user_data:
            if len(user_data['dob']) ==0:
                await ctx.reply("You have not set any birthdays")
                return
            string="```py\n"
            for name,dob in zip(user_data['Name'],user_data['dob']):
                dob=dob[:2]+"-"+dob[2:4]+"-"+dob[4:]
                string+="1. "+name+": "+dob+"\n"
            string+="```"
            await ctx.reply(string)
    @bday.command(name="remove")
    async def bremove(self, ctx,index:int):
        '''remove a birthday reminder from list
        `index`: index of the tuple to remove'''
        async with self.config1.user_from_id(ctx.author.id).all() as user_data:
            if index>len(user_data['dob']):
                await ctx.reply("Index out of range")
                return
            user_data['dob'].pop(index-1)
            user_data['Name'].pop(index-1)
            await ctx.reply("Removed successfully")
