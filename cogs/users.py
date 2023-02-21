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

        embed = discord.Embed(title=f"{user_data['title'] if 'title' in user_data else ''} {user_data['username']}", color=constants.white_color,timestamp=datetime.utcnow(), description="Account created at")

        value = f"""
        Wins: {user_data["count"]["win"]}
        Draws: {user_data["count"]["draw"]}
        Losses: {user_data["count"]["loss"]}
        """

        embed.add_field(name=f"Games: {user_data['count']['all']}", value=value, inline=False)


# This is really confusing but all I'm doing here is making the ratings looks pleasing
# As well as only showing the ones that the api returns

        ratings = ""
        ratings_list = []

        if "ultraBullet" in user_data["perfs"]:
            s_ultraBullet = "\u001b[1;37mUltraBullet:\u001b[0;0m " + str(user_data['perfs']['ultraBullet']['rating'])
            if "prov" in user_data["perfs"]["ultraBullet"]:
                s_ultraBullet = s_ultraBullet + "?"
            
            if "prog" in user_data["perfs"]["ultraBullet"]:
                prog = str(user_data["perfs"]["ultraBullet"]["prog"])
                if "-" in prog:
                    s_ultraBullet = s_ultraBullet + f"\u001b[0;31m{prog}\u001b[0;0m"
                else:
                    s_ultraBullet = s_ultraBullet + f"\u001b[0;32m+{prog}\u001b[0;0m"

            ratings_list.append(s_ultraBullet)


        if "bullet" in user_data["perfs"]:
            s_bullet = "\u001b[1;37mBullet:\u001b[0;0m " + str(user_data['perfs']['bullet']['rating'])
            if "prov" in user_data["perfs"]["bullet"]:
                s_bullet = s_bullet + "?"
            
            if "prog" in user_data["perfs"]["bullet"]:
                prog = str(user_data["perfs"]["bullet"]["prog"])
                if "-" in prog:
                    s_bullet = s_bullet + f"\u001b[0;31m{prog}\u001b[0;0m"
                else:
                    s_bullet = s_bullet + f"\u001b[0;32m+{prog}\u001b[0;0m"

            ratings_list.append(s_bullet)


        if "blitz" in user_data["perfs"]:
            s_blitz = "\u001b[1;37mBlitz:\u001b[0;0m " + str(user_data['perfs']['blitz']['rating'])
            if "prov" in user_data["perfs"]["blitz"]:
                s_blitz = s_blitz + "?"

            if "prog" in user_data["perfs"]["blitz"]:
                prog = str(user_data["perfs"]["blitz"]["prog"])
                if "-" in prog:
                    s_blitz = s_blitz + f"\u001b[0;31m{prog}\u001b[0;0m"
                else:
                    s_blitz = s_blitz + f"\u001b[0;32m+{prog}\u001b[0;0m"

            ratings_list.append(s_blitz)


        if "rapid" in user_data["perfs"]:
            s_rapid = "\u001b[1;37mRapid:\u001b[0;0m " + str(user_data['perfs']['rapid']['rating'])
            if "prov" in user_data["perfs"]["rapid"]:
                s_rapid = s_rapid + "?"

            if "prog" in user_data["perfs"]["rapid"]:
                prog = str(user_data["perfs"]["rapid"]["prog"])
                if "-" in prog:
                    s_rapid = s_rapid + f"\u001b[0;31m{prog}\u001b[0;0m"
                else:
                    s_rapid = s_rapid + f"\u001b[0;32m+{prog}\u001b[0;0m"

            ratings_list.append(s_rapid)


        if "classical" in user_data["perfs"]:
            s_classical = "\u001b[1;37mClassical:\u001b[0;0m " + str(user_data['perfs']['classical']['rating'])
            if "prov" in user_data["perfs"]["classical"]:
                s_classical = s_classical + "?"
            
            if "prog" in user_data["perfs"]["classical"]:
                prog = str(user_data["perfs"]["classical"]["prog"])
                if "-" in prog:
                    s_classical = s_classical + f"\u001b[0;31m{prog}\u001b[0;0m"
                else:
                    s_classical = s_classical + f"\u001b[0;32m+{prog}\u001b[0;0m"

            ratings_list.append(s_classical)


        if "correspondence" in user_data["perfs"]:
            s_correspondence = "\u001b[1;37mCorrespondence:\u001b[0;0m " + str(user_data['perfs']['correspondence']['rating'])
            if "prov" in user_data["perfs"]["correspondence"]:
                s_correspondence = s_correspondence + "?"
            
            if "prog" in user_data["perfs"]["correspondence"]:
                prog = str(user_data["perfs"]["correspondence"]["prog"])
                if "-" in prog:
                    s_correspondence = s_correspondence + f"\u001b[0;31m{prog}\u001b[0;0m"
                else:
                    s_correspondence = s_correspondence + f"\u001b[0;32m+{prog}\u001b[0;0m"

            ratings_list.append(s_correspondence)
        

        if len(ratings_list) != 0:
            ratings = "```ansi\n" + "\n".join(ratings_list) + "```"

        else:
            ratings = "```No ratings registered```"
        

        other_ratings_list = []

        if "chess960" in user_data["perfs"]:
            s_chess960 = "\u001b[1;37mChess960:\u001b[0;0m " + str(user_data['perfs']['chess960']['rating'])
            if "prov" in user_data["perfs"]["chess960"]:
                s_chess960 = s_chess960 + "?"
            
            if "prog" in user_data["perfs"]["chess960"]:
                prog = str(user_data["perfs"]["chess960"]["prog"])
                if "-" in prog:
                    s_chess960 = s_chess960 + f"\u001b[0;31m{prog}\u001b[0;0m"
                else:
                    s_chess960 = s_chess960 + f"\u001b[0;32m+{prog}\u001b[0;0m"

            other_ratings_list.append(s_chess960)

        
        if "kingOfTheHill" in user_data["perfs"]:
            s_kingOfTheHill = "\u001b[1;37mKing Of The Hill:\u001b[0;0m " + str(user_data['perfs']['kingOfTheHill']['rating'])
            if "prov" in user_data["perfs"]["kingOfTheHill"]:
                s_kingOfTheHill = s_kingOfTheHill + "?"
            
            if "prog" in user_data["perfs"]["kingOfTheHill"]:
                prog = str(user_data["perfs"]["kingOfTheHill"]["prog"])
                if "-" in prog:
                    s_kingOfTheHill = s_kingOfTheHill + f"\u001b[0;31m{prog}\u001b[0;0m"
                else:
                    s_kingOfTheHill = s_kingOfTheHill + f"\u001b[0;32m+{prog}\u001b[0;0m"

            other_ratings_list.append(s_kingOfTheHill)
        
        if "atomic" in user_data["perfs"]:
            s_atomic = "\u001b[1;37mAtomic:\u001b[0;0m " + str(user_data['perfs']['atomic']['rating'])
            if "prov" in user_data["perfs"]["atomic"]:
                s_atomic = s_atomic + "?"
            
            if "prog" in user_data["perfs"]["atomic"]:
                prog = str(user_data["perfs"]["atomic"]["prog"])
                if "-" in prog:
                    s_atomic = s_atomic + f"\u001b[0;31m{prog}\u001b[0;0m"
                else:
                    s_atomic = s_atomic + f"\u001b[0;32m+{prog}\u001b[0;0m"

            other_ratings_list.append(s_atomic)

        if "racingKings" in user_data["perfs"]:
            s_racingKings = "\u001b[1;37mRacing Kings:\u001b[0;0m " + str(user_data['perfs']['racingKings']['rating'])
            if "prov" in user_data["perfs"]["racingKings"]:
                s_racingKings = s_racingKings + "?"
            
            if "prog" in user_data["perfs"]["racingKings"]:
                prog = str(user_data["perfs"]["racingKings"]["prog"])
                if "-" in prog:
                    s_racingKings = s_racingKings + f"\u001b[0;31m{prog}\u001b[0;0m"
                else:
                    s_racingKings = s_racingKings + f"\u001b[0;32m+{prog}\u001b[0;0m"

            other_ratings_list.append(s_racingKings)

        if "puzzle" in user_data["perfs"]:
            s_puzzle = "\u001b[1;37mPuzzles:\u001b[0;0m " + str(user_data['perfs']['puzzle']['rating'])
            if "prov" in user_data["perfs"]["puzzle"]:
                s_puzzle = s_puzzle + "?"
            
            if "prog" in user_data["perfs"]["puzzle"]:
                prog = str(user_data["perfs"]["puzzle"]["prog"])
                if "-" in prog:
                    s_puzzle = s_puzzle + f"\u001b[0;31m{prog}\u001b[0;0m"
                else:
                    s_puzzle = s_puzzle + f"\u001b[0;32m+{prog}\u001b[0;0m"

            other_ratings_list.append(s_puzzle)

        if "storm" in user_data["perfs"]:
            s_storm = "\u001b[1;37mPuzzles Storm:\u001b[0;0m " + str(user_data['perfs']['storm']['rating'])
            if "prov" in user_data["perfs"]["storm"]:
                s_storm = s_storm + "?"
            
            if "prog" in user_data["perfs"]["storm"]:
                prog = str(user_data["perfs"]["storm"]["prog"])
                if "-" in prog:
                    s_storm = s_storm + f"\u001b[0;31m{prog}\u001b[0;0m"
                else:
                    s_storm = s_storm + f"\u001b[0;32m+{prog}\u001b[0;0m"
            
            other_ratings_list.append(s_storm)

        if len(other_ratings_list) != 0:
            other_ratings = "```ansi\n" + "\n".join(other_ratings_list) + "```"

        else:
            other_ratings = "```No ratings registered```"

# Creating the embed

        
        embed.set_author(name="User Information",icon_url=constants.user_avatar, url=user_data["url"])
        embed.set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar.url)
        embed.add_field(name="Ratings",value=ratings)
        embed.add_field(name="Other Ratings", value=other_ratings)

        await ctx.reply(embed=embed)


    
async def setup(bot):
    await bot.add_cog(Users(bot))