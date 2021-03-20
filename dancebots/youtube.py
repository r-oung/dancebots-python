#!/usr/bin/env python
# -*- coding: utf-8 -*-
import youtube_dl as yt

def get_youtube_mp3(url):
    print ("Downloading", url, "as MP3 from YouTube...")
    ytdl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }

    with yt.YoutubeDL(ytdl_opts) as ytdl:
        ytdl.download([url])

    return

if __name__ == "__main__":
    get_youtube_mp3('https://www.youtube.com/watch?v=HCjNJDNzw8Y')
