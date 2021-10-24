import argparse
import os

try:
    from pydub import AudioSegment
except Exception as er:
    print('[ERROR]', er)


def convert(audio_path):
    formats_to_convert = ['.m4a', '.mp3', '.']
    dir_path, audio_name = os.path.split(audio_path)

    for (dirpath, dirnames, filenames) in os.walk(dir_path):
        for filename in filenames:
            if filename.endswith(tuple(formats_to_convert)):

                filepath = dirpath + '/' + filename
                (path, file_extension) = os.path.splitext(filepath)
                file_extension_final = file_extension.replace('.', '')
                try:
                    track = AudioSegment.from_file(
                        filepath, file_extension_final)

                    wav_filename = filename.replace(
                        file_extension_final, 'wav')
                    wav_path = dirpath + '/' + wav_filename
                    print('CONVERTING: ' + str(filepath))
                    file_handle = track.export(wav_path, format='wav')
                    os.remove(filepath)
                except:
                    print("ERROR CONVERTING " + str(filepath))


if __name__ == '__main__':
    convert('/media/phgnam/HDD 1 _ User Data/Laboratories/TOW/Lec2-api/Code/sample2.m4a')
