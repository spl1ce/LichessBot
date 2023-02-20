import discord
from discord.ext import commands

import requests
import json
from datetime import datetime

from utils import constants



class Users(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def userinfo(self, ctx, *, username: str):
        r = requests.get(url=constants.user_public_data+username)
        user_data = json.loads(r.text)

        print(user_data)

        description = f"""
        Games: {user_data["count"]["all"]}
        Wins: {user_data["count"]["win"]}
        Draws: {user_data["count"]["draw"]}
        Losses: {user_data["count"]["loss"]}
        """


# This is really confusing but all I'm doing here is making the ratings looks pleasing
# As well as only showing the ones that the api returns

        ratings = ""
        ratings_list = []

        if "ultraBullet" in user_data["perfs"]:
            s_ultraBullet = "\u001b[1;37mUltraBullet:\u001b[0;0m " + str(user_data['perfs']['ultraBullet']['rating'])
            if "prov" in user_data["perfs"]["ultraBullet"]:
                s_ultraBullet = s_ultraBullet + "?"
            
            if "prog" in user_data["perfs"]["ultraBullet"]:
                s_ultraBullet = s_ultraBullet + str(user_data["perfs"]["ultraBullet"]["prog"])

            s_ultraBullet = s_ultraBullet
            ratings_list.append(s_ultraBullet)


        if "bullet" in user_data["perfs"]:
            s_bullet = "\u001b[1;37mBullet:\u001b[0;0m " + str(user_data['perfs']['bullet']['rating'])
            if "prov" in user_data["perfs"]["bullet"]:
                s_bullet = s_bullet + "?"
            
            if "prog" in user_data["perfs"]["bullet"]:
                s_bullet = s_bullet + str(user_data["perfs"]["bullet"]["prog"])

            s_bullet = s_bullet
            ratings_list.append(s_bullet)


        if "blitz" in user_data["perfs"]:
            s_blitz = "\u001b[1;37mBlitz:\u001b[0;0m " + str(user_data['perfs']['blitz']['rating'])
            if "prov" in user_data["perfs"]["blitz"]:
                s_blitz = s_blitz + "?"

            if "prog" in user_data["perfs"]["blitz"]:
                s_blitz = s_blitz + str(user_data["perfs"]["blitz"]["prog"])

            s_blitz = s_blitz
            ratings_list.append(s_blitz)


        if "rapid" in user_data["perfs"]:
            s_rapid = "\u001b[1;37mRapid:\u001b[0;0m " + str(user_data['perfs']['rapid']['rating'])
            if "prov" in user_data["perfs"]["rapid"]:
                s_rapid = s_rapid + "?"

            if "prog" in user_data["perfs"]["rapid"]:
                s_rapid = s_rapid + str(user_data["perfs"]["rapid"]["prog"])

            s_rapid = s_rapid
            ratings_list.append(s_rapid)


        if "classical" in user_data["perfs"]:
            s_classical = "\u001b[1;37mClassical:\u001b[0;0m " + str(user_data['perfs']['classical']['rating'])
            if "prov" in user_data["perfs"]["classical"]:
                s_classical = s_classical + "?"
            
            if "prog" in user_data["perfs"]["classical"]:
                s_classical = s_classical + str(user_data["perfs"]["classical"]["prog"])

            s_classical = s_classical
            ratings_list.append(s_classical)


        if "correspondence" in user_data["perfs"]:
            s_correspondence = "\u001b[1;37mCorrespondence:\u001b[0;0m " + str(user_data['perfs']['correspondence']['rating'])
            if "prov" in user_data["perfs"]["correspondence"]:
                s_correspondence = s_correspondence + "?"
            
            if "prog" in user_data["perfs"]["correspondence"]:
                s_correspondence = s_correspondence + str(user_data["perfs"]["correspondence"]["prog"])

            s_correspondence = s_correspondence
            ratings_list.append(s_correspondence)
        
            
        ratings = "```ansi\n" + "\n".join(ratings_list) + "```"
        




        other_ratings = f"""```ansi
{f'Chess960: {user_data["perfs"]["chess960"]["rating"]}{"?" if "prov" in user_data["perfs"]["chess960"] else ""}' if 'chess960' in user_data["perfs"] else ''}
{f'King of the Hill: {user_data["perfs"]["kingOfTheHill"]["rating"]}{"?" if "prov" in user_data["perfs"]["kingOfTheHill"] else ""}' if 'kingOfTheHill' in user_data["perfs"] else ''}
{f'Atomic: {user_data["perfs"]["atomic"]["rating"]}{"?" if "prov" in user_data["perfs"]["atomic"] else ""}' if 'atomic' in user_data["perfs"] else ''}
{f'Racing Kings: {user_data["perfs"]["racingKings"]["rating"]}{"?" if "prov" in user_data["perfs"]["racingKings"] else ""}' if 'racingKings' in user_data["perfs"] else ''}
{f'Puzzles: {user_data["perfs"]["puzzle"]["rating"]}{"?" if "prov" in user_data["perfs"]["puzzle"] else ""}' if 'puzzle' in user_data["perfs"] else ''}
{f'Puzzles Storm: {user_data["perfs"]["storm"]["rating"]}{"?" if "prov" in user_data["perfs"]["storm"] else ""}' if 'storm' in user_data["perfs"] else ''} 
```"""


# Creating the embed

        embed = discord.Embed(title=user_data["username"], color=constants.white_color,timestamp=datetime.utcnow(), description=description)
        embed.set_author(name="User Information",icon_url=constants.user_avatar, url=user_data["url"])
        embed.set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar.url)
        embed.add_field(name="Ratings",value=ratings)
        embed.add_field(name="Other Ratings", value=other_ratings)

        await ctx.reply(embed=embed)


    
async def setup(bot):
    await bot.add_cog(Users(bot))