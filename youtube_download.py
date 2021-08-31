"""
This function contain every function to download a music on youtube
"""
import asyncio

import discord
import youtube_dl

from config import config

# set empty debug message
youtube_dl.utils.bug_reports_message = lambda: ''

# configuration for dowload
ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
    'outtmpl': f"{config.music_folder}%(title)s.%(ext)s"
}

ffmpeg_options = {
    'options': '-vn'
}

yt_dl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    """
    This class will download a youtube video from a given link
    """

    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream: bool = False):
        """
        This function will download the video from a url
        :param url: the url of the YouTube video
        :param loop: *
        :param stream: *
        :return: a name of the file where the video is stored and the name of the video
        """
        loop = loop or asyncio.get_event_loop()

        data = await loop.run_in_executor(None, lambda: yt_dl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['title'] if stream else yt_dl.prepare_filename(data)

        return filename, data['title']
