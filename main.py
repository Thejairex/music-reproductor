from pygame import mixer
import yt_dlp
import os
import time

class Reproductor:
    def __init__(self):
        self.canciones = []
        self.is_pause = False

    def agregar_cancion(self, cancion):
        self.canciones.append(cancion)
        
    def download_audio(self,youtube_url):
        yt_ops = {
            'format': 'bestaudio/best',
            'outtmpl': 'music.%(ext)s',
            'ffmpeg-location': '/ffmpeg',
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        yt_dlp.YoutubeDL(yt_ops).download(youtube_url)
        
        return "music.mp3"
    
    
    def play_audio(self, file_path):
        mixer.init()
        mixer.music.load(file_path)
        mixer.music.play()
        self.is_pause = False
    
    def control_audio(self):
        while mixer.music.get_busy() or self.is_pause:
            command = input("Introduce un comando (pause, resume, stop, volume [0.0-1.0]): ").strip().lower()
            
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
        
            time.sleep(0.1)
        mixer.quit()
        
def main():
    rep = Reproductor()
    youtube_url = input("Introduce el enlace de YouTube: ")
    audio_file = rep.download_audio(youtube_url)
    rep.play_audio(audio_file)
    rep.control_audio()
    
    os.remove(audio_file)

if __name__ == "__main__":
    main()