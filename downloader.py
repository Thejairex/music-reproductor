import gdown
import zipfile
import os

class Downloader:
    def __init__(self):
        pass
    
    def download_ffmpeg(self):
        gdown.download('https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip', 'ffmpeg.zip', quiet=False)
        
        with zipfile.ZipFile('ffmpeg.zip', 'r') as zip_ref:
            zip_ref.extractall()
            
        os.remove('ffmpeg.zip')
        os.rename('ffmpeg-master-latest-win64-gpl', 'ffmpeg')
            
    def download_youtube(self):
        pass
    
    def download_spotify(self):
        pass
    
if __name__ == '__main__':
    downloader = Downloader()
    downloader.download_ffmpeg()