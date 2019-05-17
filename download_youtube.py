from youtube_dl import YoutubeDL as yt
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}
down=yt(ydl_opts).download(['https://www.youtube.com/playlist?list=PLl0zPB9P7QsKQuBzizFcZbewiwkOvfOfh'])
