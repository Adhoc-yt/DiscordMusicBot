"""
This is a music bot for Discord
GitHub: ChlouisPy

This bot can
- Play music from youtube
- Play a sound from a file
- Allow to create track
- Pause/play/skip a music
"""
import asyncio
from datetime import datetime
import json
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
import youtube_dl

from youtube_download import YTDLSource
from config import config
from utils import console_log, has_role, check_link, delete_music_folder
from multi_server import ServerMusic

# start the dot environment
load_dotenv()

# init the bot
bot = commands.Bot(command_prefix="!")
bot.remove_command('help')

MultiServer = ServerMusic()


# all command for the bot
@bot.command()
async def play(ctx: discord.Message, link: str) -> None:
    """
    This function will play a music in channel

    first this function will check if the users who type the command has the permission to do it
    next it check if the link is possible (to prevent malware ore strange video)

    :param ctx: discord message
    :param link: the youtube link
    :return: None
    """

    # check if the command is enable
    if not config.play.ACTIVATE:
        console_log(
            f"{ctx.author.name}#{ctx.author.discriminator} "
            f"used !play in server {ctx.guild.name} "
            f"with link: {link} | error: FUNCTION DISABLE"
        )
        await ctx.send("{}, this function is disable".format(ctx.message.author.name))
        return

    # check if the user is banned
    if ctx.author.id in config.banned_ids:
        console_log(
            f"{ctx.author.name}#{ctx.author.discriminator} "
            f"used !play in server {ctx.guild.name} "
            f"with link: {link} | error: USER BANNED"
        )
        await ctx.send("{}, your are banned, you can't use MusicBot".format(ctx.message.author.name))
        return

    # check if user has role
    if not has_role([r.name for r in ctx.author.roles], config.play.role):
        console_log(
            f"{ctx.author.name}#{ctx.author.discriminator} "
            f"used !play in server {ctx.guild.name} "
            f"with link: {link} | error: USER DON'T HAVE A CORRECT ROLE TO USE THIS COMMAND"
        )
        await ctx.send("{}, you don't have the required role to do that".format(ctx.message.author.name))
        return

    # check that the link is ok
    if not check_link(link, config.authorized_link):
        console_log(
            f"{ctx.author.name}#{ctx.author.discriminator} "
            f"used !play in server {ctx.guild.name} "
            f"with link: {link} | error: LINK IS NOT AUTHORIZED"
        )
        await ctx.send("{}, your link is not correct".format(ctx.message.author.name))
        return

    # remove < and > in link
    link = link.replace("<", "").replace(">", "")

    # check if the author is connected
    if not ctx.message.author.voice:
        console_log(
            f"{ctx.author.name}#{ctx.author.discriminator} "
            f"used !play in server {ctx.guild.name} "
            f"with link: {link} | error: USER IS NOT IN A VOICE CHANNEL"
        )
        await ctx.send("{}, your are not connected to a voice channel".format(ctx.message.author.name))
        return

    # start playing music
    title: str = ""

    try:
        server = ctx.message.guild
        voice_channel = server.voice_client

        # fake typing during download
        async with ctx.typing():
            # get the file name for the music
            filename, title = await YTDLSource.from_url(link, loop=bot.loop)
            # start playing the music
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
            # log in the console the result
            console_log(f"{ctx.author.name}#{ctx.author.discriminator} "
                        f"used !play in server {ctx.guild.name} "
                        f"with link: {link}"
                        )
            # set information in multi server class
            MultiServer.add_music(ctx.guild.id, filename, ctx.author.id, title)

        await ctx.send('**Now playing:** `{}`'.format(title))

    except Exception as e:
        # if the bot is not connected to the voice channel connect it and restart the music
        # if the bot cannot connect to the voice channel a second time send a error message
        destination = ctx.author.voice.channel

        console_log(f"Connecting the bot in to {destination} {str(e).replace(str(e), '')}")
        try:
            # join the channel
            await destination.connect()
            MultiServer.set_join(ctx.guild.id)

            server = ctx.message.guild
            voice_channel = server.voice_client
            voice_channel.play(discord.FFmpegPCMAudio(executable=config.encoder, source=filename))

            console_log(f"{ctx.author.name}#{ctx.author.discriminator} "
                        f"used !play in server {ctx.guild.name} "
                        f"with link: {link}"
                        )

            # set information in multi server class
            MultiServer.add_music(ctx.guild.id, filename, ctx.author.id, title)

            await ctx.send('**Now playing:** `{}`'.format(title))

        except Exception as e:
            # if e == Already playing audio. add to the queue the music
            print(str(e))
            if str(e) == "Already connected to a voice channel.":
                console_log(f"{ctx.author.name}#{ctx.author.discriminator} "
                            f"used !play in server {ctx.guild.name} "
                            f"with link: {link} and added to the queue"
                            )

                # set information in multi server class
                MultiServer.add_music(ctx.guild.id, filename, ctx.author.id, title)
                await ctx.send(f"{title} added to the queue")

            else:
                console_log(f"Impossible to connect the bot into the voice channel {destination} {str(e)}")
                await ctx.send(f"Unable to connect into {destination}")

    print(MultiServer.SERVER_DATA)


"""
@bot.command(name='join', help='Tells the bot to join the voice channel')
async def join(ctx):
    
    # console_log("1")
    # if not ctx.message.author.voice:
    #    await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name))
    #    return
    #else:
    #    channel = ctx.message.author.voice.channel
    #await channel.connect()
    destination = ctx.author.voice.channel
    print("des", destination)

    # if ctx.voice_state.voice:
    #    await ctx.voice_state.voice.move_to(destination)
    #    return

    ctx.voice_state.voice = await destination.connect()

    await ctx.send(f"Joined {ctx.author.voice.channel} Voice Channel")

"""
@bot.command(name='leave', help='To make the bot leave the voice channel')
async def leave(ctx):
    console_log("2")
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")
"""

@bot.command(name='play_song', help='To play song')
async def play(ctx, url):
    console_log("3")
    try:
        server = ctx.message.guild
        voice_channel = server.voice_client

        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
        await ctx.send('**Now playing:** {}'.format(filename))
    except Exception as e:
        await ctx.send("The bot is not connected to a voice channel.")
        print(e)


@bot.command(name='pause', help='This command pauses the song')
async def pause(ctx):
    console_log("4")
    voice_client = ctx.message.guild.voice_client
    if await voice_client.is_playing():
        await voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")


@bot.command(name='resume', help='Resumes the song')
async def resume(ctx):
    console_log("5")
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        await voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")
"""

@bot.command(name='stop', help='Stops the song')
async def stop(ctx):
    console_log("6")
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        await voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")



@bot.event
async def on_ready() -> None:
    console_log("MusicBot ready")
    console_log(f"Ready on {len(bot.guilds)} server")


if __name__ == '__main__':
    delete_music_folder()
    KEY: str = open("key").read()
    bot.run(KEY)
