import discord

from datetime import datetime

 # IDs

owner_id = 345928604057731073
white_color = 0xffffff

# Colours

graph_variants = {
    'Bullet': {'colour': '#56B4E9', 'dash': False, 'emoji': '<:56B4E9:1085200735710498836>'},
    'Blitz': {'colour': '#0072B2', 'dash': False, 'emoji': '<:0072B2:1085200798830579875>'},
    'Rapid': {'colour': '#009E73', 'dash': False, 'emoji': '<:009E73:1085200846087782441>'},
    'Classical': {'colour': '#459F3B', 'dash': False, 'emoji': '<:459F3B:1085200849170600026>'},
    'Correspondence': {'colour': '#F0E442', 'dash': True, 'emoji': '<:F0E442:1085200851225812992>'},
    'Chess960': {'colour': '#E69F00', 'dash': True, 'emoji': '<:E69F00:1085200853746585602>'},
    'King of the Hill': {'colour': '#D55E00','dash': True, 'emoji': '<:D55E00:1085200855487238236>'},
    'Three-check': {'colour': '#CC79A7', 'dash': True, 'emoji': '<:CC79A7:1085200858330968155>'},
    'Antichess': {'colour': '#DF5353', 'dash': True, 'emoji': '<:DF5353:1085200859757019146>'},
    'Atomic': {'colour': '#66558C', 'dash': True, 'emoji': '<:66558C:1085200861078233228>'},
    'Horde': {'colour': '#99E699', 'dash': True, 'emoji': '<:99E699:1085200863020204153>'},
    'Racing Kings': {'colour': '#FFAEAA', 'dash': True, 'emoji': '<:FFAEAA:1085200864521764944>'},
    'Crazyhouse': {'colour': '#56B4E9', 'dash': True, 'emoji': '<:56B4E9:1085200735710498836>'},
    'Puzzles': {'colour': '#0072B2', 'dash': True, 'emoji': '<:0072B2:1085200798830579875>'},
    'UltraBullet': {'colour': '#009E73', 'dash': True, 'emoji': '<:009E73:1085200846087782441>'}
}

# Bot URLs

user_avatar = "https://twirpz.files.wordpress.com/2015/06/twitter-avi-gender-balanced-figure.png?w=640"
icon_url = "https://cdn.discordapp.com/avatars/1076521458827804763/f371a0356a7f074bf9bd74800f453728.png?size=1024"
invite_url = "https://discord.com/api/oauth2/authorize?client_id=1076521458827804763&permissions=8&scope=bot"


# Emojis

lichess_crown = "<:crown_lichess:1079129114168004678>"
lichess_puzzles = "<:puzzles:1125119940735815811>"

# Request URLs

userpublicdata_url = "https://lichess.org/api/user/"
dailypuzzle_url = "https://lichess.org/api/puzzle/daily"

puzzles_image = "/home/spl1ce/Projects/Github/LichessBot/utils/media/puzzles.png"

# Embeds


InfoEmbed = discord.Embed(title = "Info", description = """
        Hey, I'm the LichessBot.
        My goal is to be Lichess but in discord.

        Note that I'm still in development and my dev doesn't really know what he is doing...
        """, color = white_color, timestamp=datetime.utcnow())
InfoEmbed.set_thumbnail(url=icon_url)
InfoEmbed.set_author(name="LichessBot", icon_url=icon_url)
InfoEmbed.add_field(name="Invite", value=f"[Link]({invite_url})")



InviteEmbed = discord.Embed(description=f"[Click here!]({invite_url})",color=white_color)


LimitErrorEmbed = discord.Embed(description='```ansi\n\u001b[1;31mPlease specify a valid time range: 1w, 1m, 3m, 6m, 1y, 2y, ytd or all```', color=discord.Colour.red())


