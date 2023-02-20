import discord

from datetime import datetime

 # IDs

owner_id = 345928604057731073
white_color = 0xffffff

# Bot URLs

user_avatar = "https://twirpz.files.wordpress.com/2015/06/twitter-avi-gender-balanced-figure.png?w=640"
icon_url = "https://cdn.discordapp.com/avatars/1076521458827804763/f371a0356a7f074bf9bd74800f453728.png?size=1024"
invite_url = "https://discord.com/api/oauth2/authorize?client_id=1076521458827804763&permissions=8&scope=bot"


# Request URLs

user_public_data = "https://lichess.org/api/user/"


# Embeds

InfoEmbed = discord.Embed(title = "Info", description = """
        Hey, I'm the LichessBot.
        My goal is to be Lichess but in discord.

        Note that I'm still in development and my dev doesn't know what he is doing...
        """, color = white_color, timestamp=datetime.utcnow())
InfoEmbed.set_thumbnail(url=icon_url)
InfoEmbed.set_author(name="LichessBot", icon_url=icon_url)
InfoEmbed.add_field(name="Invite", value=f"[Link]({invite_url})")


InviteEmbed = discord.Embed(description=f"[Click here!]({invite_url})",color=white_color)



