import discord
from discord.ext import commands

import json
import os


with open("config.json", "r") as config:
    data = json.load(config)


intents = discord.Intents.all()


class Bot(commands.Bot):
    async def setup_hook(self):

        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"{filename} loaded!")

            else:
                print(f"{filename} is not a cog.")
        
        print('Bot is setup.')


bot = Bot(command_prefix=data["prefix"], activity=discord.Activity(type = discord.ActivityType.playing, name="In development"), intents=intents)



@bot.event
async def on_ready():
    print('Bot is ready.')

@bot.event
async def on_connect():
    print('Bot is connected to Discord.')



@commands.is_owner()
@bot.command(name='reload', help='Reloads a cog')
async def reload(ctx, extension):
    await bot.reload_extension(f'cogs.{extension}')
    embed = discord.Embed(
        description=f'```🔄 Reloaded cogs.{extension} ```',
        color=0xf2f2f2
    )
    await ctx.reply(embed=embed)



@reload.error
async def handler(ctx, error):
    if isinstance(error, commands.NotOwner):
        pass



bot.run(data["token"])