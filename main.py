from bottle import Bottle, run, static_file, view, request
import youtube_dl
from path import Path
from multiprocessing import Pool
import threading
app = Bottle()

media_path = Path("E:/media")
def download(url,audio=False):
    if not audio:
        ydl_opts = {'format':'mp4'}
    else:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }]
        }
    ydl_opts["outtmpl"] = media_path / '%(title)s.%(ext)s'
    ydl = youtube_dl.YoutubeDL(ydl_opts)
    with ydl:
        ydl.download([url])

@app.route('/')
@view('home')
def index():
    url = request.query.get('url',None)
    audio = request.query.get('audio',False)
    if url:
        t = threading.Thread(target=download, args = (url,audio))
        t.daemon = True
        t.start()
        # download(url,audio)

    return {}

if __name__ == "__main__":
    if not media_path.exists():
        media_path.mkdir()
    run(app)