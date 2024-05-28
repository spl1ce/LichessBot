import discord
from discord.ext import commands

import typing
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
    bot.get_command("user status").update(enabled=False)
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

@commands.is_owner()
@commands.guild_only()
@bot.command(name='sync', help='Syncs the bots commands with Discord API.')
async def sync(
  ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: typing.Optional[typing.Literal["~", "*", "^"]] = None) -> None:
    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")



@reload.error
async def handler(ctx, error):
    if isinstance(error, commands.NotOwner):
        pass



bot.run(data["token"])