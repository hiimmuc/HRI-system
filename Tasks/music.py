import webbrowser

from youtube_search import YoutubeSearch
import os
import random
import glob
import pyaudio
import wave
import sys
from pathlib import Path

LIB_PATH = str(Path("Tasks/backup/music_lib"))
allowed_ext = ['.mp3', '.wav', '.flac', '.ogg']
lib = list(filter(lambda x: x, [path for ext in allowed_ext for path in glob.glob(os.path.join(LIB_PATH, f'*{ext}'))]))


def youtube(what):
    '''search what on youtube, for steaming
    Args:
        what (str): what to search for
    '''
    while True:
        result = YoutubeSearch(what, max_results=10).to_dict()
        if result:
            break
    url = 'https://www.youtube.com' + result[0]['url_suffix']
    webbrowser.open(url)
    return True


class AudioFile:
    chunk = 1024

    def __init__(self, file):
        """ Init audio stream """
        self.wf = wave.open(file, 'rb')
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=self.p.get_format_from_width(self.wf.getsampwidth()),
            channels=self.wf.getnchannels(),
            rate=self.wf.getframerate(),
            output=True
        )

    def play(self):
        """ Play entire file """
        data = self.wf.readframes(self.chunk)
        while data != '':
            self.stream.write(data)
            data = self.wf.readframes(self.chunk)

    def close(self):
        """ Graceful shutdown """
        self.stream.close()
        self.p.terminate()


def play_from_lib(song_name):
    '''play song from library'''
    if any(song_name in lib_song.lower() for lib_song in lib):
        print(f'Playing {song_name}')
        song_path = list(filter(lambda lib_song: song_name in lib_song.lower(), lib))[0]
        song = AudioFile(f'{song_path}')
        song.play()
        song.close()
        return True
    else:
        print(f'{song_name} not in library, play random song')
        if len(lib) > 0:
            song_path = random.choice(lib)
            song = AudioFile(f'{song_path}')
            song.play()
            song.close()
            return True
        else:
            print('No songs in library')
            return False


if __name__ == '__main__':
    print(lib)
    play_from_lib("river234")
