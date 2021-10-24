# from convert_audio_format import convert
import argparse
import os

try:
    import speech_recognition as sr
except Exception as r:
    print(r)
    raise r

MyRecognizer = sr.Recognizer()
parser = argparse.ArgumentParser()
parser.add_argument('--audio', required=False, type=str, default='')
args = parser.parse_args()


def read_from_audio(audio_path, lang='en-US'):
    """function read text from audio wav file

    Args:
        audio_path (str): path to audio file
        lang (str, optional): language used. Defaults to 'en-US'.

    Returns:
        transcript: text
    """
    dir_path, audio_name = os.path.split(audio_path)
    format_allows = ['.m4a', '.mp3', '.wav']
    # convert(audio_path)
    if not any(f in audio_name for f in format_allows):
        raise Exception('format error')

    fm = audio_name.split('.')[-1]
    audio_name = audio_name.replace(fm, 'wav')
    new_audio_path = os.path.join(dir_path, audio_name)

    sample = sr.AudioFile(new_audio_path)

    with sample as source:
        MyRecognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio_data = MyRecognizer.record(sample)

    return MyRecognizer.recognize_google(audio_data, language=lang)


def read_from_microphone(lang='en-US'):
    """This is a function to read data directly from microphone

    Args:
        lang (str, optional): language used. Defaults to 'vi-VN'.

    Returns:
        transcript: text got from microphone
    """
    input_message = ''
    print('Say something!')
    with sr.Microphone(sample_rate=44100) as mic:
        print("You:", end='')
        MyRecognizer.adjust_for_ambient_noise(mic)
        print("->> ", end='')
        audio = MyRecognizer.listen(mic, timeout=4)

    try:
        input_message = MyRecognizer.recognize_google(audio,
                                                      language=lang)
        print(input_message, end='\n')
        return input_message
    except Exception as error:
        raise Exception(error)
    pass


if __name__ == '__main__':
    print(read_from_microphone())

    pass
