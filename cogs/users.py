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

        ratings = f"""
        {f'UltraBullet: {user_data["perfs"]["ultraBullet"]["rating"]}{"?" if "prov" in user_data["perfs"]["ultraBullet"] else ""}' if 'ultraBullet' in user_data["perfs"] else ''}
        {f'Bullet: {user_data["perfs"]["bullet"]["rating"]}{"?" if "prov" in user_data["perfs"]["bullet"] else ""}' if 'bullet' in user_data["perfs"] else ''}
        {f'Blitz: {user_data["perfs"]["blitz"]["rating"]}{"?" if "prov" in user_data["perfs"]["blitz"] else ""}' if 'blitz' in user_data["perfs"] else ''}
        {f'Rapid: {user_data["perfs"]["rapid"]["rating"]}{"?" if "prov" in user_data["perfs"]["rapid"] else ""}' if 'rapid' in user_data["perfs"] else ''}
        {f'Classical: {user_data["perfs"]["classical"]["rating"]}{"?" if "prov" in user_data["perfs"]["classical"] else ""}' if 'classical' in user_data["perfs"] else ''}
        {f'Correspondence: {user_data["perfs"]["correspondence"]["rating"]}{"?" if "prov" in user_data["perfs"]["correspondence"] else ""}' if 'correspondence' in user_data["perfs"] else ''}
        """

        other_ratings = f"""
        {f'Chess960: {user_data["perfs"]["chess960"]["rating"]}{"?" if "prov" in user_data["perfs"]["chess960"] else ""}' if 'chess960' in user_data["perfs"] else ''}
        {f'King of the Hill: {user_data["perfs"]["kingOfTheHill"]["rating"]}{"?" if "prov" in user_data["perfs"]["kingOfTheHill"] else ""}' if 'kingOfTheHill' in user_data["perfs"] else ''}
        {f'Atomic: {user_data["perfs"]["atomic"]["rating"]}{"?" if "prov" in user_data["perfs"]["atomic"] else ""}' if 'atomic' in user_data["perfs"] else ''}
        {f'Racing Kings: {user_data["perfs"]["racingKings"]["rating"]}{"?" if "prov" in user_data["perfs"]["racingKings"] else ""}' if 'racingKings' in user_data["perfs"] else ''}
        {f'Puzzles: {user_data["perfs"]["puzzle"]["rating"]}{"?" if "prov" in user_data["perfs"]["puzzle"] else ""}' if 'puzzle' in user_data["perfs"] else ''}
        {f'Puzzles Storm: {user_data["perfs"]["storm"]["rating"]}{"?" if "prov" in user_data["perfs"]["storm"] else ""}' if 'storm' in user_data["perfs"] else ''}
        """


        embed = discord.Embed(title="User Information", color=constants.white_color,timestamp=datetime.utcnow())
        embed.set_author(name=user_data["username"],icon_url=constants.user_avatar, url=user_data["url"])
        embed.set_footer(text=f"Requested by {ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar.url)
        embed.add_field(name="Ratings",value=ratings)
        embed.add_field(name="Other Ratings", value=other_ratings)


        await ctx.reply(embed=embed)


    
async def setup(bot):
    await bot.add_cog(Users(bot))