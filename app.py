from flask import Flask, render_template, request, redirect, url_for, flash
import requests
from config import Config
from models import db, UserPreference
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Initialize database tables
with app.app_context():
    db.create_all()

# Helper functions for API calls
def get_weather(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={app.config["OPENWEATHER_API_KEY"]}&units=metric'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

def get_hourly_weather(city):
    current_weather = get_weather(city)
    if current_weather and current_weather.get('coord'):
        lat = current_weather['coord']['lat']
        lon = current_weather['coord']['lon']
        url = f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely,daily,alerts&appid={app.config["OPENWEATHER_API_KEY"]}&units=metric'
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching hourly weather data: {e}")
            return {}
    return {}

def get_news(keyword=None, category=None):
    base_url = 'https://newsapi.org/v2/top-headlines'
    params = {
        'apiKey': app.config["NEWSAPI_API_KEY"],
        'country': 'us'
    }
    if keyword:
        params['q'] = keyword
    if category:
        params['category'] = category
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news data: {e}")
        return None

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('index.html')

@app.route('/weather', methods=['GET', 'POST'])
def weather():
    data = {}
    hourly_data = {}
    city = request.args.get('city', 'Tokyo')  # Default city
    if request.method == 'POST':
        city = request.form.get('city')
    data = get_weather(city)
    hourly_data = get_hourly_weather(city)
    return render_template('weather.html', weather=data, hourly=hourly_data, city=city)

@app.route('/news', methods=['GET', 'POST'])
def news():
    keyword = request.args.get('keyword', '')
    category = request.args.get('category', '')
    news_data = get_news(keyword, category)
    return render_template('news.html', news=news_data, keyword=keyword, category=category)

@app.route('/save_preference', methods=['POST'])
def save_preference():
    favorite_city = request.form.get('favorite_city')
    preferred_topic = request.form.get('preferred_topic')
    if favorite_city and preferred_topic:
        pref = UserPreference(favorite_city=favorite_city, preferred_topic=preferred_topic)
        db.session.add(pref)
        db.session.commit()
        flash('Preferences saved!', 'success')
    else:
        flash('Please fill out all fields.', 'error')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)

