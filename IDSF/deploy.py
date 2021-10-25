"""
combine two part:
speech recognition and intents, text segmentation to extract information from spoken sentence
"""

import time

from inference import JointBertTools
from stt_tools.convert_audio_format import convert
from stt_tools.speech_recognition_imp import read_from_microphone
from tools import *


def main():
    """
    """
    t1 = time.time()
    # Load model
    model_dir = "./sgd_model"
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
                weather_outdoor(city_name=city_name)
            elif any('timeRange' in key for key in slots_and_values):
                weather_outdoor()
        elif intent.strip() == 'PlaySong':
            # if intent is streaming music
            slots_and_values = get_expression(utterance)
            yt_search = ''
            for key in slots_and_values:
                if any(x in key for x in ['track', 'album', 'song_name']):
                    yt_search += ('' + slots_and_values[key])
            youtube(yt_search)


if __name__ == '__main__':
    main()
