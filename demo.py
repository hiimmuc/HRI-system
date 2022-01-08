"""
combine two part:
speech recognition and intents, text segmentation to extract information from spoken sentence
"""
import time

from ASR.STT import *
from DialogManagement import *
from IDSF.inference_module import JointBertTools
from Tasks import music, weather
from Tasks.utils import *

recog = Recognizer()


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
        text = [convert_languages(recog.read_from_microphone())]
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
        elif intent.strip() in ['PlaySong', 'PlayMusic', 'PlayMedia']:
            # if intent is streaming music
            slots_and_values = get_expression(utterance)
            song_name = ''
            for key in slots_and_values:
                if any(x in key for x in ['track', 'album', 'song_name']):
                    song_name += ('' + slots_and_values[key])
            # music.youtube(song_name)
            music.play_from_lib(song_name=song_name)


if __name__ == '__main__':
    main()
    # dummy()
    pass
