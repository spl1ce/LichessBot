import discord
from discord.ext import commands

import chess
import chess.pgn
import chess.svg

import requests
import json
import datetime
import io
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM


from utils import constants



class Puzzles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group()
    async def puzzle(self, ctx):
        pass

    @puzzle.command(description="Solve todays puzzle!")
    async def daily(self, ctx):
        r = requests.get(url=constants.dailypuzzle_url)
        pzl_data = json.loads(r.text)
        if "pgn" in pzl_data["game"]:
            pgn = pzl_data["game"]["pgn"]
            game = chess.pgn.read_game(io.StringIO(pgn))
            board = game.end().board()
            boardsvg = chess.svg.board(coordinates=True, board = board, size=350)
            f = open("utils/media/dailypuzzle.svg", "w")
            f.write(boardsvg)
            f.close()
            drawing = svg2rlg('utils/media/dailypuzzle.svg')
            renderPM.drawToFile(drawing, 'utils/media/dailypuzzle.png', fmt='PNG')

            file = discord.File('utils/media/dailypuzzle.png', filename="dailypuzzle.png")

        embed = discord.Embed(
            title="Daily Puzzle",
            colour=constants.white_color,
            timestamp=datetime.datetime.utcnow()
            )
        
        embed.set_image(url="attachment://dailypuzzle.png")
        await ctx.reply(file=file, embed=embed)


async def setup(bot):
    await bot.add_cog(Puzzles(bot))
