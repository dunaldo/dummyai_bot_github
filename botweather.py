"""Weather forecast."""
import urllib.request
from urllib.parse import urlencode
import json
from tokenweather import weatherToken

# Openweathermap Weather codes and corressponding emojis
thunderstorm = u'\U0001F4A8'    # Code: 200's, 900, 901, 902, 905
drizzle = u'\U0001F4A7'         # Code: 300's
rain = u'\U00002614'            # Code: 500's
snowflake = u'\U00002744'       # Code: 600's snowflake
snowman = u'\U000026C4'         # Code: 600's snowman, 903, 906
atmosphere = u'\U0001F301'      # Code: 700's foogy
clearSky = u'\U00002600'        # Code: 800 clear sky
fewClouds = u'\U000026C5'       # Code: 801 sun behind clouds
clouds = u'\U00002601'          # Code: 802-803-804 clouds general
hot = u'\U0001F525'             # Code: 904
defaultEmoji = u'\U0001F300'    # default emojis

degree_sign = u'\N{DEGREE SIGN}'

WEATHER_BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?'
WEATHER_API_KEY = weatherToken
WEATHER_CITY_NAME = 'q='
WEATHER_CITY_LAT = 'lat='
WEATHER_CITY_LNG = 'lon='
WEATHER_UNIT = 'metric'
WEATHER_DAY_CNT = 1


# You can find API description and request URL examples at https://openweathermap.org/
def ask_weather(lat, lon):
    """Encoding URL and trying to request it."""
    try:
        url_encode_pairs = {'lat': str(lat), 'lon': str(lon),
                            'APPID': WEATHER_API_KEY, 'units': WEATHER_UNIT,
                            'cnt': WEATHER_DAY_CNT, 'lang': 'ru'}
        encoded_url = urlencode(url_encode_pairs)
        weather_url_coords = WEATHER_BASE_URL + encoded_url
        weather_response = json.load(urllib.request.urlopen(weather_url_coords))
        return send_back_to_user(weather_response)
    except Exception:  # So, I don't have any idea what could go wrong, but to be sure...
        return "Can't find anything on given coordinates" + U'\U0001F626'


def type_weather(text):
    """Encoding URL and trying to request it."""
    try:
        url_encode_pairs = {'q': text,
                            'APPID': WEATHER_API_KEY, 'units': WEATHER_UNIT,
                            'cnt': WEATHER_DAY_CNT, 'lang': 'ru'}
        encoded_url = urlencode(url_encode_pairs)
        weather_url_coords = WEATHER_BASE_URL + encoded_url
        weather_response = json.load(urllib.request.urlopen(weather_url_coords))
        return send_back_to_user(weather_response)
    except Exception:  # Any input "text" that isn't a city, is not a city.
        return "I can't find corresponding city..." + U'\U0001F615'


# You can find API description and response examples at https://openweathermap.org/current
def send_back_to_user(weather_response):
    """Get response and send in back to user."""
    response_code = weather_response.get('cod')

    if weather_response.get('cod') is 200:
        city_name = weather_response.get("name")
        country_name = weather_response.get("sys").get("country")
        city_temperature = str(int(weather_response.get("main").get("temp")))
        city_humidity = str(weather_response.get("main").get("humidity"))
        city_wind = str(weather_response.get("wind").get("speed"))
        if weather_response.get("wind").get("deg"):
            city_wind_direction = weather_response.get("wind").get("deg")
            city_wind_direction = wind_direction(city_wind_direction)
        else:
            city_wind_direction = 'Calm'
        city_emoji = get_emoji(weather_response.get("weather")[0].get("id"))
        sendback = ('''Weather in {},{}:
Cloudiness {} {}{}
Humidity {}%
Wind {} {}m/s
Wind direction - {}''').format(city_name,
                               country_name,
                               city_emoji,
                               city_temperature,
                               degree_sign,
                               city_humidity,
                               thunderstorm,
                               city_wind,
                               city_wind_direction)
        return sendback
    else:
        error_message = weather_response.get('message')
        return (str(response_code) + ' - ' + error_message)


def wind_direction(deg):
    """Getting a wind direction in degrees and checking where it fits."""
    try:
        if 348.75 <= deg < 360:
            return 'north'
        elif 0 <= deg < 11.25:
            return 'north'
        elif 11.25 <= deg < 33.75:
            return 'north-northeast'
        elif 33.75 <= deg < 56.25:
            return 'northeast'
        elif 56.25 <= deg < 78.75:
            return 'east-northeast'
        elif 78.75 <= deg < 101.25:
            return 'east'
        elif 101.25 <= deg < 123.75:
            return 'east-southeast'
        elif 123.75 <= deg < 146.25:
            return 'southeast'
        elif 146.25 <= deg < 168.75:
            return 'south-southeast'
        elif 168.75 <= deg < 191.25:
            return 'south'
        elif 191.25 <= deg < 213.75:
            return 'south-southwest'
        elif 213.75 <= deg < 236.25:
            return 'southwest'
        elif 236.25 <= deg < 258.75:
            return 'west-southwest'
        elif 258.75 <= deg < 281.25:
            return 'west'
        elif 281.25 <= deg < 303.75:
            return 'west-northwest'
        elif 303.75 <= deg < 326.25:
            return 'northwest'
        elif 326.25 <= deg < 348.75:
            return 'north-northwest'
    except Exception:
        return 'Something gone wrong...'


def get_emoji(weather_id):
    """We have to get weather id to show corresponding icon."""
    if weather_id:
        if (str(weather_id)[0] == '2' or weather_id == 900 or
                weather_id == 901 or weather_id == 902 or weather_id == 905):
            return thunderstorm
        elif str(weather_id)[0] == '3':
            return drizzle
        elif str(weather_id)[0] == '5':
            return rain
        elif str(weather_id)[0] == '6' or weather_id == 903 or weather_id == 906:
            return snowflake + ' ' + snowman
        elif str(weather_id)[0] == '7':
            return atmosphere
        elif weather_id == 800:
            return clearSky
        elif weather_id == 801:
            return fewClouds
        elif weather_id == 802 or weather_id == 803 or weather_id == 804:
            return clouds
        elif weather_id == 904:
            return hot
        else:
            return defaultEmoji
    else:
        return defaultEmoji
