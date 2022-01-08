import datetime
import requests
from Tasks.utils import *


def weather_outdoor(city_name='Hanoi', specific=None):
    """Get the information about the weather in place
    Args:
        city_name (str, optional): city to get information. Defaults to 'Hanoi'.
        specific (str, optional): specify what factor to get temp, humidity, pressure, wind, clouds, dt. Defaults to None.
    """

    if not specific:
        specific = ''

    try:
        api = r"330ff11e86b5ccbeba0a2f71aab88014"
        # city_name = convert_languages(city_name, dest='en').replace(' ', '').lower()
        city_name = city_name.replace(' ', '').lower()
        url = f"https://api.openweathermap.org/data/2.5/weather?appid={api}&q={city_name}"
        response = requests.get(url)
        data = response.json()

        if data["cod"] != "404":
            data_table = data["main"]
            current_temperature = data_table['temp'] - 273.15
            current_pressure = data_table["pressure"]
            current_humidity = data_table["humidity"]
            some_text = data["weather"]
            weather_description = some_text[0]["description"]

            msg = f"City: {data['name']}, {data['sys']['country']}\n" \
                f"{datetime.datetime.now()}\n" \
                f"Weather summary: {weather_description}, \n" \
                f">The temperature {round(current_temperature, 2)} Celsius, \n" \
                f">The humidity is {current_humidity} %, \n" \
                f">The pressure is {current_pressure} Pa"

            if not specific:
                print(msg)
            else:
                if specific in ['temp', 'pressure', 'humidity']:
                    print(f"{specific}: {data_table[f'{specific}']}")
                else:
                    print(f"{specific}: {data[f'{specific}']}")
        else:
            raise "API not found, 404 error"
    except Exception as r:
        print(r)
        print("not found in api, search web")
        kw = "Weather in" + city_name
        gg_search(kw, max_results=1)


if __name__ == '__main__':
    weather_outdoor(city_name='paris')
