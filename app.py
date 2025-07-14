import os
import requests
from flask import Flask, render_template, jsonify
from geopy.geocoders import Nominatim

# Initialize the Flask app
app = Flask(__name__)

# Geocoder to convert place names into coordinates
geolocator = Nominatim(user_agent="crisis-mapper")

# NewsAPI key (get yours from https://newsapi.org/)
NEWS_API_KEY = 'YOUR_NEWSAPI_KEY'
KEYWORDS = ['earthquake', 'fire', 'flood', 'hurricane', 'volcano']

# Function to fetch news articles related to crises
def fetch_news():
    query = ' OR '.join(KEYWORDS)  # Join keywords with OR logic for search
    url = f'https://newsapi.org/v2/everything?q={query}&apiKey={NEWS_API_KEY}'
    response = requests.get(url)
    articles = response.json().get('articles', [])
    return articles

# Function to geocode a location and return coordinates (latitude, longitude)
def geocode_location(place_name):
    try:
        location = geolocator.geocode(place_name)
        return (location.latitude, location.longitude) if location else None
    except Exception as e:
        print(f"Geocoding error: {e}")
        return None

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to fetch event data in JSON format for the frontend
@app.route('/events')
def get_events():
    articles = fetch_news()  # Get crisis articles from the news API
    events = []  # This will store our event data

    for article in articles:
        location_name = article['title']  # Use article title or description to extract location
        coords = geocode_location(location_name)  # Get coordinates from the place name

        # Only add events that can be geocoded
        if coords:
            events.append({
                'title': article['title'],
                'description': article['description'],
                'lat': coords[0],
                'lon': coords[1],
                'source': article['url']
            })
    
    return jsonify(events)  # Send events as JSON to the frontend

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
