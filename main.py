from pygame import mixer
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse, parse_qs
from pytube import Playlist, YouTube
from threading import Thread
import os
import time
import yt_dlp
import emoji

class Reproductor:
    def __init__(self):
        self.queue = []
        self.cursor = 0
        self.is_pause = False
        self.path_ffmpeg = os.path.join(os.getcwd(), r'ffmpeg\bin')
        self.limit_thread = os.cpu_count() - 1
        print(self.limit_thread)
        os.environ['PATH'] += os.pathsep + self.path_ffmpeg
        
        if not os.path.exists('Music'):
            os.mkdir('Music')
        
    def download_audio(self,youtube_url, title):
        path_song = f'Music/{title}'
        yt_ops = {
            'format': 'bestaudio[ext=webm]',
            'outtmpl': f'{path_song}.%(ext)s',
            'quiet': True,
            'noplaylist': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }
        
        
        # Descargar audio de YouTube
        yt_dlp.YoutubeDL(yt_ops).download([youtube_url])

        path_song += '.mp3'
        return path_song
    
    def process_playlist(self, url):
        playlist = Playlist(url)
        first_song = playlist.videos[0]
        
        # play the first song
        self.process_single_video(first_song.watch_url)
        self.play_audio()
        
        control = Thread(target=self.control_audio)
        control.start()
        
        # process the rest of the songs
        with ThreadPoolExecutor(max_workers=self.limit_thread) as executor:
            futures = []
            for video in playlist.videos:
                if video != first_song:
                    futures.append(executor.submit(self.process_single_video, video.watch_url))
                    
            for future in futures:
                future.result()
        
        control.join()
        
    def process_single_video(self, url):
        video = YouTube(url)

        # Get the video URL
        video_url = video.watch_url
        
        # Get the video title
        video_title = video.title.replace('/', '_').replace('\\', '_').replace('|', '').replace('"', '')
        video_title = emoji.replace_emoji(video_title)
        
        # Download the song
        song_path = self.download_audio(video_url, video_title)
        
        
        # Add the song to the queue
        self.queue.append(song_path)
        print(f"Added song: {video_title}", end='\r')


    def process_url(self, url): 
        query_params = parse_qs(urlparse(url).query)
        
        if 'list' in query_params:
            print("Detectada lista de reproducción.")
            self.process_playlist(url)
        else:
            print("Detectada canción individual.")
            self.process_single_video(url)
    
            # play audio
            self.play_audio()
            self.control_audio()
    
    def play_audio(self):
        mixer.init()
        mixer.music.load(self.queue[self.cursor])
        mixer.music.play()
        self.is_pause = False
    
    def control_audio(self):
        while mixer.music.get_busy() or self.is_pause:
            print(f"Reproduciendo: {self.queue[self.cursor]}", end='\r')
            command = input("Introduce un comando (pause, resume, stop, volume [0.0-1.0]), next, prev: ").strip().lower()
            
            if command == "resume":
                mixer.music.unpause()
                self.is_pause = False
            elif command == "pause":
                if mixer.music.get_busy() and not self.is_pause:
                    mixer.music.pause()
                    self.is_pause = True
            
            elif command == "stop":
                mixer.music.stop()
                self.is_pause = False
                break
            
            elif command.startswith("volume"):
                volume = float(command.split()[1])
                mixer.music.set_volume(volume)
                print(f"Volumen actual: {volume}")

            elif command == "next":
                self.cursor = (self.cursor + 1) % len(self.queue)
                self.play_audio()
            
            elif command == "prev":
                self.cursor = (self.cursor - 1) % len(self.queue)
                self.play_audio()
        
            time.sleep(0.1)
        mixer.quit()
        
def main():
    rep = Reproductor()
    youtube_url = input("Introduce el enlace de YouTube: ")
    rep.process_url(youtube_url)

if __name__ == "__main__":
    main()