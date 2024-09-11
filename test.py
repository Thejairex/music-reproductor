from pytube import Playlist

url = 'https://www.youtube.com/watch?v=jIpiLvkDIK8&list=PLycPWAqYz2nMrvDaFqWDDMapUsc9AQ7Gu'

playlist = Playlist(url)

for video in playlist.videos[1:]:
    print(video.title)