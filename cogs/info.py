import discord
from discord.ext import commands


from utils import constants


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx):
        owner = await self.bot.fetch_user(constants.owner_id)

        embed = constants.InfoEmbed
        embed.set_footer(text=f"{ctx.author.name}#{ctx.author.discriminator}", icon_url=ctx.author.avatar.url)
        embed.add_field(name="Developed by", value=f"{owner.mention} ({owner.name}#{owner.discriminator})")
        await ctx.reply(embed=embed)

    @commands.command()
    async def invite(self, ctx):
        embed = constants.InviteEmbed

        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Info(bot))