import discord
from discord.ext import commands

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd

import typing
import flag
import pycountry
import requests
import json
import datetime

from utils import constants


def graph(data, xmin):


    fig = plt.figure()
    ax = fig.add_subplot()

    grey_color = '#646873'

    fig.set_facecolor('#2f3136')
    ax.set_facecolor('#2f3136')
    ax.spines['bottom'].set_color(grey_color)
    ax.spines['right'].set_color(grey_color)
    ax.tick_params(axis='x', colors=grey_color)
    ax.tick_params(axis='y', colors=grey_color,direction='out',pad=-1)
    ax.yaxis.tick_right()
    ax.spines[['left','top','right']].set_visible(False)
    ax.grid(color=grey_color,axis='y')
    fig.set_figwidth(10)

    formatter = mdates.AutoDateFormatter(mdates.AutoDateLocator())
    formatter.scaled[365] = "%h, %y"
    formatter.scaled[30] = "%h, %Y"
    formatter.scaled[1] = "%d %h, %y"

    ax.xaxis.set_major_formatter(formatter)
    ax.xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=10))

    for variant in data:
        

        points = variant['points']
        name = variant['name']

        
        # Arranging the data 

        dates = []
        ratings = []

        for entry in points:
            date = datetime.datetime(year=entry[0], month=entry[1]+1, day=entry[2])
            dates.append(date)

        ratings = [entry[3] for entry in points]
        

        # Make lines go straight when there is not data

        for date in dates:
            index = dates.index(date) 
            day_before = date - datetime.timedelta(days=1)
            if day_before not in dates and index !=0:
                dates.insert(index, day_before)
                ratings.insert(index, ratings[index-1])

        # Creating the graph and costumizing it

        plt.plot(dates, ratings, color = constants.graph_variants[name]['colour'], dashes=(4,4) if constants.graph_variants[name]['dash'] else (None, None))


    ## FINISHING THE GRAPH


    # Find ymax and ymin for the graph


    if xmin != None:
            
        for i in range(len(dates)):
            if dates[i] >= xmin:
                xmin_i = i-1 if i!= 0 else i
                break
        
        
        plt.xlim(xmin, datetime.datetime.today())
        ymin, ymax = ax.get_ylim()
        if len(points) == 1:
            ymax = max(ratings[xmin_i:])
        plt.ylim(ymin-100,ymax+100)

        
    else:
        ymin, ymax = ax.get_ylim()
        plt.ylim(ymin-100,ymax+100)

    ax.set_yticklabels(ax.get_yticklabels(), ha="right", va="bottom")

    labels = []
    for label in ax.get_xticklabels():
        label = label.get_text().title()
        labels.append(label)

    ax.set_xticklabels(labels)



    return plt.savefig('utils/media/image.png',bbox_inches='tight')


class RHDropdown(discord.ui.Select):
    def __init__(self, data, xmin):
        self.data = data
        self.xmin = xmin

        options = [
            discord.SelectOption(label='All variants', description='Display all variants.', value='All', emoji='<:rainbowcircle:1085206360691576942>')
        ]
        super().__init__(placeholder='Choose the variants you want to see...', min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):

        name = self.values[0]
        data = self.data
        new_data = []

        if name == 'All':
            new_data = data
        else:
            for variant in self.data:
                if variant['name'] == name:
                    new_data.append(variant)

        embed = interaction.message.embeds[0]
        graph(data=new_data, xmin=self.xmin)
        file = [discord.File('utils/media/image.png', filename="image.png")]
        embed.set_image(url="attachment://image.png")
        await interaction.response.edit_message(attachments=file, embed=embed)


class RHView(discord.ui.View):
    def __init__(self):
        super().__init__()

        # Adds the dropdown to our view object.

class Users(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(aliases = ['ui'])
    async def userinfo(self, ctx, *, username: str):
        r = requests.get(url=constants.user_public_data+username)
        user_data = json.loads(r.text)

        print(user_data)


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

                embed.title = constants.lichess_crown + " " + embed.title

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

    @commands.hybrid_command()
    async def status(self, ctx, *, usernames: str):
        
        r = requests.get(url="https://lichess.org/api/users/status", params={'ids': usernames.replace(" ",",")})
        user_data = json.loads(r.text)[0]
        print(user_data)

        

        embed = discord.Embed(title=f"{user_data['title'] if 'title' in user_data else ''} {user_data['username']}",
                              description="test",
                              colour=colour,
                              timestamp=datetime.datetime.utcnow()
                              )
        
        embed.set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar.url)
        
        # Check if user is: online, Lichess patron, streaming and playing

        if 'online' in user_data:
            if user_data['online']:
                colour = discord.Colour.green
                online = True

            else:
                colour = discord.Colour.light_grey
                online = False

        if 'patron' in user_data:
            if user_data['patron']:

                embed.title = constants.lichess_crown + " " + embed.title
        else:
            pass

        if 'streaming' in user_data:
            streaming = user_data['streaming']


        if 'playing' in user_data:
            if user_data['playing']:
                playing = "Is Playing"


        # Finishing the embed

        value="""```

        ```"""

        embed.add_field(name='Status', value=value)
        await ctx.reply(embed=embed)


    @commands.hybrid_command(aliases=['rh'])
    async def rating_history(self, ctx, username: str, lim = '3m'):
        
        ## CREATING THE GRAPH

        # Getting the date range of the graph 

        limits = {
            '1w':{'days': 7, 'label': '1 week'},
            '1m':{'days': 30, 'label': '1 month'},
            '3m':{'days': 3*30, 'label': '3 months'},
            '6m':{'days': 6*30, 'label': '6 months'},
            '1y':{'days': 12*30, 'label': '1 year'},
            '2y':{'days': 24*30, 'label': '2 years'}
        }

        try:
            days = limits[lim]['days']
            xmin = (datetime.datetime.today() - datetime.timedelta(days=days))
            desc_start = f"Rating history in the past __{limits[lim]['label']}__."

        except KeyError:
            if lim.lower() == 'all':
                desc_start = f"__All time__ rating history."
                xmin = None
            elif lim.lower() == 'ytd':
                desc_start = f"Rating history __since the start of this year__."
                xmin = datetime.datetime(year=datetime.datetime.today().year,month=1,day=1)
            else:
                embed = constants.LimitErrorEmbed
                await ctx.reply(embed=embed)
                return


        ## REQUESTING DATA FROM LICHESS
        rh_r = requests.get(url=f"https://lichess.org/api/user/{username}/rating-history")
        data = rh_r.content
        print(data)
        rh_data = json.loads(rh_r.text)

        upd_r = requests.get(url=constants.user_public_data+username)
        data = upd_r.content
        upd_data = json.loads(upd_r.text)
        

        # Just writing it to a file for testing purposes
        with open('data.json', 'wb') as f:
            f.write(data)

        view = RHView()
        selectmenu = RHDropdown(rh_data, xmin)

        for variant in rh_data:
            name = variant['name']
            selectmenu.add_option(label=name, value=name, emoji=constants.graph_variants[name]['emoji'])

        graph(rh_data, xmin)

        # Get the variants
        
        plt.savefig('utils/media/image.png',bbox_inches='tight')
        file = discord.File('utils/media/image.png', filename="image.png")


        ## Creating the embed

        embed = discord.Embed(
            title=f"{upd_data['title'] if 'title' in upd_data else ''} {upd_data['username']}",
            color=constants.white_color,
            description=f'{desc_start}\n\nChange the time range by specifying it in the command like this:\n`=rh username [1w, 1m, 3m, 6m, 1y, 2y, ytd or all]`\n',
            timestamp=datetime.datetime.utcnow(),
            url=upd_data['url']
        )
        embed.set_image(url="attachment://image.png")
        embed.set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar.url)

        if 'patron' in upd_data:
            if upd_data['patron']:

                embed.title = constants.lichess_crown + " " + embed.title


        view.add_item(selectmenu)
        await ctx.reply(file=file, view=view, embed=embed)


async def setup(bot):
    await bot.add_cog(Users(bot))