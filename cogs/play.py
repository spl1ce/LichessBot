import discord
from discord.ext import commands

from utils import constants

from cairosvg import svg2png

import requests
import json
import io
import traceback


import chess
from chess import pgn
from chess import svg
from svglib.svglib import svg2rlg


class Guess(discord.ui.Modal, title='Guess'):
    def __init__(self, solution):
        super().__init__()
        self.count = 0
        self.solution = solution
    # Our modal classes MUST subclass `discord.ui.Modal`,
    # but the title can be whatever you want.

    # This will be a short input, where the user can enter their name
    # It will also have a placeholder, as denoted by the `placeholder` kwarg.
    # By default, it is required and is a short-style input which is exactly
    # what we want.
    name = discord.ui.TextInput(
        label='Move',
        placeholder='Type the move in Algebraic Chess Notation...',
    )


    async def on_submit(self, interaction: discord.Interaction):
        if self.name.value == self.solution[0]:
            print("ok1")
            self.count += 2
            board_file = discord.File("/home/spl1ce/Projects/Github/LichessBot/utils/media/board.png", filename="board.png")
            puzzles_file = discord.File("/home/spl1ce/Projects/Github/LichessBot/utils/media/puzzles.png", filename="puzzles.png")
            print("ok2")

            embed = discord.Embed(title="Daily Puzzle", description=f"""
            **Best Move!**
            Keep going...
            
            *Type the next move in Algebraic Chess Notation. *`/notation`""")
            embed.set_image(url="attachment://board.png")
            embed.set_thumbnail(url="attachment://puzzles.png")
            await interaction.response.edit_message(attachments=[board_file, puzzles_file], embed=embed, view=Solving(solution=self.solution))

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Oops! Something went wrong.', ephemeral=True)

        # Make sure we know what the error actually is
        traceback.print_exception(type(error), error, error.__traceback__)



class Solving(discord.ui.View):
    def __init__(self, solution):
        super().__init__()
        self.solution = solution

    @discord.ui.button(label='Guess', style=discord.ButtonStyle.blurple)
    async def guess(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(Guess(solution=self.solution))


class SolveIt(discord.ui.View):
    def __init__(self, board, solution):
        super().__init__()
        self.value = None
        self.board = board
        self.solution = solution

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.

    @discord.ui.button(label='Solve it', style=discord.ButtonStyle.green)
    async def solveit(self, interaction: discord.Interaction, button: discord.ui.Button):
        board_file = discord.File("/home/spl1ce/Projects/Github/LichessBot/utils/media/board.png", filename="board.png")
        puzzles_file = discord.File("/home/spl1ce/Projects/Github/LichessBot/utils/media/puzzles.png", filename="puzzles.png")

        turn = "Black"
        if self.board.turn is True:
            turn = "White"

        embed = discord.Embed(title="Daily Puzzle", description=f"""
        **Your turn**
        Find the best move for {turn}
        
        *Type the move in Algebraic Chess Notation. *`/notation`""")
        embed.set_image(url="attachment://board.png")
        embed.set_thumbnail(url="attachment://puzzles.png")
        await interaction.response.send_message(files=[board_file, puzzles_file], embed=embed, view=Solving(solution=self.solution), ephemeral=True)
        
        self.value = True
        self.stop()





class Play(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.hybrid_command(aliases=["dp"])
    async def daily_puzzle(self, ctx):
        r = requests.get(url=constants.daily_puzzle_data)
        puzzle_data = json.loads(r.text)

        puzzle_id = puzzle_data["puzzle"]["id"]
        puzzle_rating = puzzle_data["puzzle"]["rating"]
        puzzle_plays = puzzle_data["puzzle"]["plays"]
        puzzle_clock = puzzle_data["game"]["clock"]
        puzzle_perfname = puzzle_data["game"]["perf"]["name"]
        players = puzzle_data["game"]["players"]
        white_name = players[0]["name"]
        black_name = players[1]["name"]

        solution = puzzle_data["puzzle"]["solution"]

        pgn = io.StringIO(puzzle_data["game"]["pgn"])
        game = chess.pgn.read_game(pgn)
        board = chess.Board()


        for move in game.mainline_moves():
            board.push(move) 
        boardsvg = chess.svg.board(board, lastmove=move)

        svg2png(bytestring=boardsvg, write_to='board.png')

        outputfile = open('D:/Users/Utilizador/Documents/GitHub/LichessBot/utils/media/board.svg', "w")
        outputfile.write(boardsvg)
        outputfile.close()

        svg2png(bytestring=boardsvg, write_to='D:/Users/Utilizador/Documents/GitHub/LichessBot/utils/media/board.png')

        board_file = discord.File("D:/Users/Utilizador/Documents/GitHub/LichessBot/utils/media/board.png", filename="board.png")
        puzzles_file = discord.File("D:/Users/Utilizador/Documents/GitHub/LichessBot/utils/media/puzzles.png", filename="puzzles.png")

        description = f"""
        Puzzle: [#{puzzle_id}](https://lichess.org/training/{puzzle_id})
        Rating: {puzzle_rating}
        Played **{puzzle_plays}** times

        From game {puzzle_clock} • {puzzle_perfname}
        <:whiteicon:1125454428942630983> {white_name} 
        <:blackicon:1125454922138255500> {black_name}
        """

        embed = discord.Embed(title=f"Daily Puzzle", description=description, colour=constants.white_color)
        embed.set_image(url="attachment://board.png")
        embed.set_thumbnail(url="attachment://puzzles.png")
        view = SolveIt(board=board, solution=solution)

        await ctx.reply(files=[board_file, puzzles_file], embed=embed, view=view)



# Show daily puzzle
# ask if user wants to play it.
# if yes user inputs first move
# if correct, congrats now whats the next move?
# if incorrect, oops you didn't get it right, try again!
# at the end of the puzzle, congrats you got it right!


async def setup(bot):
    await bot.add_cog(Play(bot))



# Make board flip if black is to move
# handle wrong answers
# make the solution continuation
# congratulating message
# make notation command