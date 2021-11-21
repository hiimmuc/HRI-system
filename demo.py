"""
combine two part:
speech recognition and intents, text segmentation to extract information from spoken sentence
"""
import time

from ASR.STT import read_from_microphone
from DialogManagement import *
from IDSF.inference_module import JointBertTools
from Tasks import music, weather
from Tasks.utils import *


def main():
    """
    """
    t1 = time.time()
    # Load model
    model_dir = "IDSF/backup/sgd"
    batch_size = 32
    predict_tools = JointBertTools(model_dir=model_dir, batch_size=batch_size)
    print(f"[INFO] load model:{time.time() - t1}")
    # iteration till user type n or no to stop
    while input("continue?").lower() not in ['no', 'n']:
        text = [convert_languages(read_from_microphone())]
        print(text)
        predict_text = predict_tools.predict(text)[0]
        print(predict_text)
        intent, utterance = predict_text.split('->')
        print(intent, utterance)
        if intent.strip() == 'GetWeather':
            # if intent is getting weather information
            slots_and_values = get_expression(utterance)
            if any('city' in key for key in slots_and_values):
                city_name = slots_and_values['B-city']
                weather.weather_outdoor(city_name=city_name)
            elif any('timeRange' in key for key in slots_and_values):
                weather.weather_outdoor()
        elif intent.strip() == 'PlaySong':
            # if intent is streaming music
            slots_and_values = get_expression(utterance)
            yt_search = ''
            for key in slots_and_values:
                if any(x in key for x in ['track', 'album', 'song_name']):
                    yt_search += ('' + slots_and_values[key])
            music.youtube(yt_search)


def dummy():
    """
    """
    while input("continue?").lower() not in ['no', 'n']:
        text = [convert_languages(read_from_microphone())]
        print(text)
        intent = 'GetWeather'
        if intent.strip() == 'GetWeather':
            # if intent is getting weather information
            weather.weather_outdoor(city_name='paris')
        elif intent.strip() == 'PlaySong':
            # if intent is streaming music
            yt_search = 'Faded Alan Walker'
            music.youtube(yt_search)
    pass


if __name__ == '__main__':
    main()
    # dummy()
    pass
