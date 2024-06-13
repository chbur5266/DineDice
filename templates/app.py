from flask import Flask, render_template, request
import requests
import random
import folium

app = Flask(__name__)

# Yelp API Key
API_KEY = "nHykIZKwUBTK89XGz1Fsj8GD5LgEDGW-OhpN2F8_Twnz-yeaDFs-xan7MWjStU7x1gZVoXH8xdE8OvxDJXynx7Lj8saPYftvbuCdH4RKqrMP9NWRGI492hpA0PxoZnYx"

def get_random_restaurant(zip_code, distance):
    try:
        headers = {
            "Authorization": f"Bearer {API_KEY}"
        }
        params = {
            "location": zip_code,
            "radius": int(distance * 1609.34),  # Convert miles to meters
            "categories": "restaurants",
            "limit": 50,  # Limit to 50 restaurants
            "sort_by": "best_match"
        }
        response = requests.get("https://api.yelp.com/v3/businesses/search", headers=headers, params=params)
        data = response.json()
        if "businesses" in data:
            if data["businesses"]:
                return random.choice(data["businesses"])
        else:
            app.logger.error(f"No 'businesses' key in Yelp API response: {data}")
    except Exception as e:
        app.logger.error(f"Error fetching restaurant data: {e}")
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        zip_code = request.form['zip_code']
        distance = float(request.form['distance'])
        restaurant = get_random_restaurant(zip_code, distance)
        if restaurant:
            return render_template('result.html', restaurant=restaurant)
        else:
            return render_template('result.html', error="No restaurants found.")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)