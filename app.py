from flask import Flask
from flask import render_template
from flask import request
from urllib.parse import quote
from urllib.request import urlopen
import json

app = Flask(__name__)

OPEN_WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={0}&units=metric&APPID={1}"

OPEN_WEATHER_KEY = '1c5bb71698802ac933124f4edad4eb93'

NEWS_URL = "http://newsapi.org/v2/everything?q={0}&sortBy=publishedAt&apiKey={1}"

NEWS_KEY = '0cde40832cd04dd999d8107b7cf1d959'

@app.route("/")
def home():
    city = request.args.get('city')
    if not city:
        city = 'bangkok'
    weather = get_weather(city, OPEN_WEATHER_KEY)
    topic = 'covid-19'
    news = get_news(topic, NEWS_KEY,4)
    return render_template("home.html", weather=weather, news=news)

@app.route('/news')
def news():
    topic = request.args.get('topic')
    if not topic:
        topic = 'covid-19'
    nums = 20
    news = get_news(topic, NEWS_KEY,nums)
    return render_template("news.html", news=news,topic=topic)

   
@app.route('/about')
def about():
   return render_template('about.html')  

def get_weather(city,API_KEY):
    query = quote(city)
    url = OPEN_WEATHER_URL.format(query, API_KEY)
    data = urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get('weather'):

        description = parsed['weather'][0]['description']
        temperature = parsed['main']['temp']
        city = parsed['name']
        country = parsed['sys']['country']
        icon = parsed['weather'][0]['icon']
        pressure = parsed['main']['pressure']
        humidity = parsed['main']['humidity']
        windsp = parsed['wind']['speed']

        weather = {'description': description,
                   'temperature': temperature,
                   'city': city,
                   'country': country,
                   'icon':icon,
                   'pressure':pressure,
                   'humidity':humidity,
                   'windsp':windsp
                   }
    return weather

def get_news(topic,API_KEY,nums):
    query = quote(topic)
    url = NEWS_URL.format(query, API_KEY)
    data = urlopen(url).read()
    parsed = json.loads(data)
    news = []
    if parsed.get('articles'):
        
        for n in range(0,nums):
            articles = parsed['articles'][n] 
            news.append(articles)
    return news
