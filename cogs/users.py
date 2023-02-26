import discord
from discord.ext import commands

import flag
import pycountry
import requests
import json
import datetime

from utils import constants



class Users(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command()
    async def userinfo(self, ctx, *, username: str):
        r = requests.get(url=constants.user_public_data+username)
        user_data = json.loads(r.text)


## Creating the embed object

        embed = discord.Embed(
            color=constants.white_color,
            timestamp=datetime.datetime.utcnow(),
            description="",
            title=f"{user_data['title'] if 'title' in user_data else ''} {user_data['username']}",
            url=user_data['url']
            )


## Grabing all the data of the user
    # Profile info (bio, country, location, etc...)

        if 'profile' in user_data:
            profile_info = ""
            if 'firstName' in user_data['profile']:
                firstName = user_data['profile']['firstName']
                profile_info = profile_info + f"**{firstName}**"

            if 'lastName' in user_data['profile']:
                lastName = user_data['profile']['lastName']
                profile_info = profile_info + f" **{lastName}**"

            if 'bio' in user_data['profile']:
                bio = user_data['profile']['bio']
                profile_info = profile_info + f"\n*{bio}*"

            if 'fideRating' in user_data['profile']:
                fideRating = user_data['profile']['fideRating']
                profile_info = profile_info + f"\n\nFIDE Rating: **{fideRating}**"

            if 'uscfRating' in user_data['profile']:
                uscfRating = user_data['profile']['uscfRating']
                profile_info = profile_info + f"\n\nUSCF Rating: **{fideRating}**"

            if 'ecfRating' in user_data['profile']:
                ecfRating = user_data['profile']['ecfRating']
                profile_info = profile_info + f"\n\nECF Rating: **{fideRating}**"


            if 'country' in user_data['profile'] or 'location' in user_data['profile']:
                if 'country' in user_data['profile']:
                    country = user_data['profile']['country']
                    if len(country) == 2:
                        country_flag = flag.flag(country)
                        country_name = pycountry.countries.get(alpha_2=country).name

                    elif country == "_belarus-wrw":
                        country_flag = "🏴󠁲󠁵󠁡󠁤󠁿"
                        country_name = "Belarus White-red-white"
                    elif country == "_east-turkestan":
                        country_flag = "🏴󠁲󠁵󠁡󠁤󠁿"
                        country_name = "East Turkestan"
                    elif country == "_lichess":
                        country_flag = "<:lichesslogo:1079094668500938762>"
                        country_name = "Lichess"
                    elif country == "_priate":
                        country_flag = "🏴‍☠️"
                        country_name = "Pirate"
                    elif country == "_rainbow":
                        country_flag = "🏳️‍🌈"
                        country_name = "Rainbow"
                    elif country == "_russia-wbw":
                        country_flag = "🏴󠁲󠁵󠁡󠁤󠁿"
                        country_name = "Russia White-blue-white"
                    elif country == "_united-nations":
                        country_flag = "🇺🇳"
                        country_name = "United Nations"
                    elif country == "_earth":
                        country_flag = "🌍"
                        country_name = "Earth"
                    elif country == "_transgender":
                        country_flag = "🏳️‍⚧️"
                        country_name = "Transgender"
                    else:
                        country_flag = "🏴󠁲󠁵󠁡󠁤󠁿"
                        country_name = "Unknown"

                else:
                    country_name = ""
                    country_flag = ""

                if 'location' in user_data['profile']:
                    location = user_data['profile']['location']

                else:
                    location = ""
                
                profile_info = profile_info + f"\n\n{location} {country_flag} {country_name}"

            embed.description=profile_info


    # TOS Violation check

        if 'tosViolation' in user_data:
            if user_data['tosViolation']:
                tosViolation = "```ansi\n❗\u001b[1;31mThis account violated the Lichess Terms of Service```"
                embed.add_field(name='TOS Violation', value=tosViolation)
            else: 
                tosViolation = ""
        else: 
            tosViolation = ""

    # Games, Wins, Losses and Draws

        if 'count' in user_data:
            game_count = user_data['count']['all']

            value = f"""
            Wins: {user_data["count"]["win"]}
            Draws: {user_data["count"]["draw"]}
            Losses: {user_data["count"]["loss"]}
            """

            embed.add_field(name=f"Games: {game_count}", value=value, inline=False)

    # Account creation date
        
        if 'createdAt' in user_data:
            createdAt = user_data['createdAt'] / 1000
            embed.add_field(name='Member since', value=datetime.datetime.fromtimestamp(createdAt).strftime('%b %d, %Y'))

    # Time Spent Playing

        if 'playTime' in user_data:
            playTime = user_data['playTime']['total']
            hour_value = playTime // 3600
            sec_value = playTime % 3600
            min = sec_value // 60
            sec_value %= 60
            embed.add_field(name='Time spent playing', value=f"{hour_value} hours and {min} minutes")
        else:
            embed.add_field(name='\u2800', value='\u2800')

    # Time spent on TV

        if 'playTime' in user_data:
            tvTime = user_data['playTime']['tv']
            hour_value = tvTime // 3600
            sec_value = tvTime % 3600
            min = sec_value // 60
            sec_value %= 60
            embed.add_field(name='Time on TV', value=f"{hour_value} hours and {min} minutes")
        else:
            embed.add_field(name='\u2800', value='\u2800')


    # Writting down the ratings

        ratings = ""
        ratings_list = []

        if 'perfs' in user_data:
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
            
        # Writting down the other ratings


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
                s_storm = "\u001b[1;37mPuzzles Storm:\u001b[0;0m " + str(user_data['perfs']['storm']['score'])
                if "runs" in user_data["perfs"]["storm"]:
                    s_storm = s_storm + f" out of {str(user_data['perfs']['storm']['runs'])} runs"
                
                other_ratings_list.append(s_storm)

            if len(other_ratings_list) != 0:
                other_ratings = "```ansi\n" + "\n".join(other_ratings_list) + "```"

            else:
                other_ratings = "```No ratings registered```"


    # Check if user is a Lichess patron

        if 'patron' in user_data:
            if user_data['patron']:

                embed.title = '<:crown_lichess:1079129114168004678> ' + embed.title
        else:
            pass

## Finishing the embed
        
        embed.set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar.url)
        embed.add_field(name="Ratings",value=ratings, inline=True)
        embed.add_field(name="Other Ratings", value=other_ratings, inline=True)

    # Check if the user is playing

        if 'playing' in user_data:
            playing_link = user_data['playing']
            side = playing_link[-5:]

            embed.add_field(name=f'Currently playing as {side}', value=f"[Link to game]({playing_link})", inline=False)

        await ctx.reply(embed=embed)


    
async def setup(bot):
    await bot.add_cog(Users(bot))