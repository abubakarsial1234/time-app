from flask import Flask, jsonify
from datetime import datetime
import pytz
import json

app = Flask(__name__)

# World cities with their timezones and coordinates
WORLD_CITIES = {
    "London": {"timezone": "Europe/London", "country": "United Kingdom", "lat": 51.5074, "lon": -0.1278},
    "New York": {"timezone": "America/New_York", "country": "United States", "lat": 40.7128, "lon": -74.0060},
    "Los Angeles": {"timezone": "America/Los_Angeles", "country": "United States", "lat": 34.0522, "lon": -118.2437},
    "Paris": {"timezone": "Europe/Paris", "country": "France", "lat": 48.8566, "lon": 2.3522},
    "Tokyo": {"timezone": "Asia/Tokyo", "country": "Japan", "lat": 35.6762, "lon": 139.6503},
    "Sydney": {"timezone": "Australia/Sydney", "country": "Australia", "lat": -33.8688, "lon": 151.2093},
    "Dubai": {"timezone": "Asia/Dubai", "country": "UAE", "lat": 25.2048, "lon": 55.2708},
    "Moscow": {"timezone": "Europe/Moscow", "country": "Russia", "lat": 55.7558, "lon": 37.6176},
    "Singapore": {"timezone": "Asia/Singapore", "country": "Singapore", "lat": 1.3521, "lon": 103.8198},
    "Hong Kong": {"timezone": "Asia/Hong_Kong", "country": "Hong Kong", "lat": 22.3193, "lon": 114.1694},
    "Karachi": {"timezone": "Asia/Karachi", "country": "Pakistan", "lat": 24.8607, "lon": 67.0011},
    "Mumbai": {"timezone": "Asia/Kolkata", "country": "India", "lat": 19.0760, "lon": 72.8777},
    "Beijing": {"timezone": "Asia/Shanghai", "country": "China", "lat": 39.9042, "lon": 116.4074},
    "Toronto": {"timezone": "America/Toronto", "country": "Canada", "lat": 43.6532, "lon": -79.3832},
    "São Paulo": {"timezone": "America/Sao_Paulo", "country": "Brazil", "lat": -23.5505, "lon": -46.6333},
    "Mexico City": {"timezone": "America/Mexico_City", "country": "Mexico", "lat": 19.4326, "lon": -99.1332},
    "Cairo": {"timezone": "Africa/Cairo", "country": "Egypt", "lat": 30.0444, "lon": 31.2357},
    "Johannesburg": {"timezone": "Africa/Johannesburg", "country": "South Africa", "lat": -26.2041, "lon": 28.0473},
    "Istanbul": {"timezone": "Europe/Istanbul", "country": "Turkey", "lat": 41.0082, "lon": 28.9784},
    "Bangkok": {"timezone": "Asia/Bangkok", "country": "Thailand", "lat": 13.7563, "lon": 100.5018}
}

def get_city_time(city_name):
    """Get current time for a specific city"""
    if city_name not in WORLD_CITIES:
        return None
    
    timezone = pytz.timezone(WORLD_CITIES[city_name]["timezone"])
    now = datetime.now(timezone)
    
    return {
        "time": now.strftime("%H:%M:%S"),
        "date": now.strftime("%A, %b %d %Y"),
        "timezone": now.strftime("%Z%z"),
        "utc_offset": now.strftime("%z")
    }

def get_time_of_day(hour):
    """Determine time of day based on hour"""
    if 6 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 18:
        return "Day"
    elif 18 <= hour < 22:
        return "Evening"
    else:
        return "Night"

def get_sunrise_sunset(city_name):
    """Get sunrise and sunset times for a city (simplified calculation)"""
    if city_name not in WORLD_CITIES:
        return {"sunrise": "07:00", "sunset": "19:00", "duration": "12h 00m"}
    
    # Simplified sunrise/sunset calculation
    # In a real app, you'd use a proper API like OpenWeatherMap
    timezone = pytz.timezone(WORLD_CITIES[city_name]["timezone"])
    now = datetime.now(timezone)
    hour = now.hour
    
    # Basic seasonal adjustment (very simplified)
    if 3 <= now.month <= 9:  # Spring/Summer
        sunrise_hour = 6
        sunset_hour = 20
    else:  # Fall/Winter
        sunrise_hour = 7
        sunset_hour = 18
    
    sunrise = f"{sunrise_hour:02d}:{30 if hour % 2 == 0 else 45}"
    sunset = f"{sunset_hour:02d}:{15 if hour % 2 == 0 else 30}"
    duration = f"{sunset_hour - sunrise_hour}h {(sunset_hour - sunrise_hour) * 60 % 60:02d}m"
    
    return {
        "sunrise": sunrise,
        "sunset": sunset,
        "duration": duration
    }

@app.route('/')
def index():
    """Main page showing world clock interface"""
    # Get current time for Karachi (Pakistan) as the main display
    pakistan_time = get_city_time("Karachi")
    pakistan_timezone = pytz.timezone(WORLD_CITIES["Karachi"]["timezone"])
    now_pakistan = datetime.now(pakistan_timezone)
    pakistan_sunrise_sunset = get_sunrise_sunset("Karachi")
    
    # Get times for featured cities
    featured_cities = ["Karachi", "London", "New York", "Dubai"]
    city_times = {}
    
    for city in featured_cities:
        if city in WORLD_CITIES:
            time_data = get_city_time(city)
            timezone = pytz.timezone(WORLD_CITIES[city]["timezone"])
            now = datetime.now(timezone)
            city_times[city] = {
                "time": time_data["time"],
                "time_of_day": get_time_of_day(now.hour),
                "utc_offset": time_data["utc_offset"],
                "country": WORLD_CITIES[city]["country"]
            }
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>TimeSpot - World Clock</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{ 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                /* --- CHANGED: Dark Green Gradient --- */
                background: linear-gradient(135deg, #011F13 0%, #0A2D27 50%, #1E3A3A 100%);
                min-height: 100vh;
                color: #ffffff;
                transition: all 0.3s ease;
                position: relative;
                overflow-x: hidden;
            }}
            
            body::before {{
                content: '';
                position: fixed;
                top: 0;
                right: 0;
                width: 300px;
                height: 300px;
                /* --- CHANGED: Green Glow --- */
                background: radial-gradient(circle, rgba(61, 220, 132, 0.2) 0%, transparent 70%);
                border-radius: 50%;
                z-index: 0;
            }}
            
            body::after {{
                content: '';
                position: fixed;
                bottom: 0;
                right: -100px;
                width: 400px;
                height: 400px;
                /* --- CHANGED: Green Glow --- */
                background: radial-gradient(circle, rgba(61, 220, 132, 0.15) 0%, transparent 70%);
                border-radius: 50%;
                z-index: 0;
            }}
            
            body.white-theme {{
                background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
                color: #333;
            }}
            
            body.white-theme::before,
            body.white-theme::after {{
                display: none;
            }}
            
            /* This orange-theme is no longer used by buttons, but kept for reference */
            body.orange-theme {{
                background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%);
                color: #333;
            }}
            
            body.orange-theme::before,
            body.orange-theme::after {{
                display: none;
            }}
            
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                position: relative;
                z-index: 1;
            }}
            
            .header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 40px;
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(20px);
                padding: 20px;
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.1);
                transition: all 0.3s ease;
            }}
            
            body.white-theme .header {{
                background: rgba(255, 255, 255, 0.8);
                border: 1px solid rgba(0, 0, 0, 0.1);
            }}

            .logo {{
                display: flex;
                align-items: center;
                gap: 10px;
                font-size: 24px;
                font-weight: bold;
                color: white;
            }}
            
            .logo-icon {{
                width: 40px;
                height: 40px;
                /* --- CHANGED: Accent Color --- */
                background: #3DDC84;
                border-radius: 50%;
                display: flex; 
                align-items: center;
                justify-content: center; 
                font-size: 20px;
                color: #111;
            }}
            
            .search-bar {{
                flex: 1;
                max-width: 400px;
                margin: 0 20px;
            }}
            
            .search-bar input {{
                width: 100%;
                padding: 12px 20px;
                border: none;
                border-radius: 25px;
                background: rgba(255, 255, 255, 0.9);
                font-size: 16px;
                outline: none;
                color: #333;
            }}
            
            body.white-theme .search-bar input {{
                background: rgba(255, 255, 255, 0.95);
                border: 1px solid rgba(0, 0, 0, 0.1);
            }}

            .header-buttons {{
                display: flex;
                gap: 15px;
                align-items: center;
            }}
            
            .theme-controls {{
                display: flex;
                gap: 10px;
                align-items: center; 
                margin-right: 15px;
            }}
            
            .theme-btn {{
                padding: 8px 16px;
                /* --- CHANGED: Accent Color --- */
                border: 2px solid #3DDC84;
                border-radius: 20px;
                background: transparent;
                color: white;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.3s ease;
                font-size: 12px;
                min-width: 60px;
            }}
            
            .theme-btn:hover {{
                /* --- CHANGED: Accent Color Glow --- */
                background: rgba(61, 220, 132, 0.1);
            }}
            
            .theme-btn.active {{
                /* --- CHANGED: Accent Color --- */
                background: #3DDC84;
                color: #111;
            }}
            
            .theme-btn.white {{
                /* --- CHANGED: Accent Color --- */
                border-color: #3DDC84;
                color: #333;
                background: white;
            }}
            
            .theme-btn.white:hover {{
                background: #f0f0f0;
            }}
            
            .theme-btn.white.active {{
                background: white;
                color: #333;
                /* --- CHANGED: Accent Color --- */
                border-color: #3DDC84;
            }}
            
            .theme-btn.dark {{
                /* --- CHANGED: Accent Color --- */
                border-color: #3DDC84;
                color: white;
                background: transparent;
            }}
            
            .theme-btn.dark:hover {{
                /* --- CHANGED: Accent Color Glow --- */
                background: rgba(61, 220, 132, 0.1);
            }}
            
            .theme-btn.dark.active {{
                /* --- CHANGED: Accent Color --- */
                background: #3DDC84;
                color: #111;
            }}
            
            .btn {{
                padding: 10px 20px;
                border: 2px solid white;
                border-radius: 25px;
                background: transparent;
                color: white;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.3s ease;
            }}
            
            .btn:hover {{
                background: white;
                /* --- CHANGED: Accent Color --- */
                color: #0A2D27;
            }}
            
            .main-clock {{
                background: rgba(0, 0, 0, 0.4);
                border-radius: 30px;
                padding: 60px;
                margin-bottom: 40px;
                text-align: center;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3), 
                            0 0 0 1px rgba(61, 220, 132, 0.2),
                            inset 0 1px 0 rgba(61, 220, 132, 0.1);
                backdrop-filter: blur(20px);
                transition: all 0.3s ease;
                position: relative;
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }}
            
            .main-clock::before {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 2px;
                /* --- CHANGED: Accent Color --- */
                background: linear-gradient(90deg, transparent 0%, #3DDC84 50%, transparent 100%);
                border-radius: 30px 30px 0 0;
            }}
            
            body.white-theme .main-clock {{
                background: rgba(255, 255, 255, 0.98);
                color: #333;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.05);
                border: 1px solid rgba(0, 0, 0, 0.1);
            }}
            
            body.white-theme .main-clock::before {{
                /* --- CHANGED: Accent Color --- */
                background: linear-gradient(90deg, transparent 0%, #3DDC84 50%, transparent 100%);
            }}
            
            .main-time {{
                font-size: 120px;
                font-weight: 300;
                color: white;
                margin-bottom: 20px;
                letter-spacing: -2px;
            }}
            
            body.white-theme .main-time {{
                color: #333;
            }}

            .main-location {{
                font-size: 32px;
                color: white;
                margin-bottom: 10px;
                font-weight: 500;
            }}
            
            .main-date {{
                font-size: 24px;
                color: rgba(255, 255, 255, 0.8);
                margin-bottom: 30px;
            }}
            
            .sun-info {{
                font-size: 18px;
                color: white;
                margin-bottom: 20px;
            }}
            
            body.white-theme .main-location,
            body.white-theme .main-date,
            body.white-theme .sun-info {{
                color: #333;
            }}
            
            body.white-theme .main-date {{
                color: #666;
            }}
            
            .format-toggles {{
                display: flex;
                gap: 10px;
                justify-content: center;
            }}
            
            .format-btn {{
                padding: 8px 16px;
                /* --- CHANGED: Accent Color --- */
                border: 2px solid #3DDC84;
                border-radius: 20px;
                background: transparent;
                color: white;
                cursor: pointer;
                transition: all 0.3s ease;
                font-size: 12px;
                min-width: 50px;
            }}
            
            .format-btn.active {{
                /* --- CHANGED: Accent Color --- */
                background: #3DDC84;
                color: #111;
                border-color: #3DDC84;
            }}
            
            .format-btn:not(.active) {{
                background: transparent;
                color: white;
                /* --- CHANGED: Accent Color --- */
                border-color: #3DDC84;
            }}
            
            body.white-theme .format-btn {{
                color: #333;
                border-color: #ddd;
            }}
            
            body.white-theme .format-btn.active {{
                background: #333;
                color: white;
                border-color: #333;
            }}
            
            .slogan {{
                text-align: center;
                font-size: 24px;
                color: white;
                margin-bottom: 40px;
                font-weight: 300;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            
            .cities-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 20px;
                margin-bottom: 40px;
            }}
            
            .city-card {{
                background: rgba(0, 0, 0, 0.4);
                border-radius: 20px;
                padding: 30px;
                text-align: center; 
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                cursor: pointer;
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.1);
                color: white;
            }}
            
            .city-card.featured {{
                /* --- CHANGED: Accent Color Glow --- */
                background: rgba(61, 220, 132, 0.1);
                border: 1px solid rgba(61, 220, 132, 0.2);
            }}
            
            body.white-theme .city-card {{
                background: rgba(255, 255, 255, 0.98);
                border: 1px solid rgba(0, 0, 0, 0.1);
                color: #333;
            }}
            
            .city-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
            }}
            
            .city-time {{
                font-size: 48px;
                font-weight: 300;
                margin-bottom: 10px;
            }}
            
            .city-name {{
                font-size: 20px;
                font-weight: 500;
                margin-bottom: 5px;
            }}
            
            .city-country {{
                font-size: 14px;
                color: #888;
                margin-bottom: 10px;
            }}
            
            .city-time-of-day {{
                font-size: 14px;
                padding: 5px 12px;
                border-radius: 15px;
                display: inline-block;
                margin-bottom: 10px;
            }}
            
            .city-time-of-day.day {{
                background: #ffeb3b;
                color: #333;
            }}
            
            .city-time-of-day.night {{
                background: #2196f3;
                color: white;
            }}
            
            .city-time-of-day.morning {{
                background: #ff9800;
                color: white;
            }}
            
            .city-time-of-day.evening {{
                background: #9c27b0;
                color: white;
            }}
            
            .utc-offset {{
                font-size: 12px;
                color: #666;
                font-family: monospace;
            }}
            
            .add-city {{
                background: rgba(255, 255, 255, 0.1);
                border: 2px dashed rgba(255, 255, 255, 0.5);
                border-radius: 20px;
                padding: 30px;
                text-align: center;
                color: white;
                cursor: pointer;
                transition: all 0.3s ease;
                backdrop-filter: blur(10px);
            }}
            
            .add-city:hover {{
                background: rgba(255, 255, 255, 0.2);
                border-color: rgba(255, 255, 255, 0.8);
            }}
            
            .add-city-icon {{
                font-size: 48px;
                margin-bottom: 15px;
            }}
            
            .add-city-text {{
                font-size: 18px;
                font-weight: 500;
            }}
            
            .all-cities {{
                background: rgba(255, 255, 255, 0.95);
                border-radius: 20px;
                padding: 30px;
                backdrop-filter: blur(10px);
            }}
            
            .all-cities h2 {{
                font-size: 28px;
                margin-bottom: 20px;
                color: #333;
                text-align: center;
            }}
            
            .cities-list {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
                gap: 15px;
            }}
            
            .city-item {{
                background: #f8f9fa;
                padding: 15px;
                border-radius: 10px;
                text-align: center;
                cursor: pointer;
                transition: all 0.3s ease;
                border: 2px solid transparent;
            }}
            
            .city-item:hover {{
                background: #e9ecef;
                /* --- CHANGED: Accent Color --- */
                border-color: #3DDC84;
            }}
            
            .city-item-name {{
                font-weight: 500;
                margin-bottom: 5px;
                color: #333;
            }}
            
            .city-item-country {{
                font-size: 12px;
                color: #666;
            }}
            
            @media (max-width: 768px) {{
                .main-time {{
                    font-size: 80px;
                }}
                
                .header {{
                    flex-direction: column;
                    gap: 20px;
                }}
                
                .search-bar {{
                margin: 0; 
                    max-width: 100%;
                }}
                
                .cities-grid {{
                    grid-template-columns: 1fr;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">
                    <div class="logo-icon">🕐</div>
                    <span>TimeSpot</span>
                </div>
                <div class="search-bar">
                    <input type="text" placeholder="Q Search" id="searchInput">
                </div>
                <div class="header-buttons">
                    <div class="theme-controls">
                        <button class="theme-btn" onclick="setTheme('orange')">Orange</button>
                        <button class="theme-btn white" onclick="setTheme('white')">White</button>
                        <button class="theme-btn dark active" onclick="setTheme('dark')">🌙 Dark</button>
                    </div>
                    <button class="btn">Log In</button>
                    <button class="btn">Get the App</button>
                </div>
            </div>
            
            <div class="main-clock">
                <div class="main-time" id="mainTime">{pakistan_time["time"]}</div>
                <div class="main-location">Karachi, {WORLD_CITIES["Karachi"]["country"]}</div>
                <div class="main-date">{pakistan_time["date"]}</div>
                <div class="sun-info">
                    Sun ☀️: {pakistan_sunrise_sunset["sunrise"]} - {pakistan_sunrise_sunset["sunset"]} ({pakistan_sunrise_sunset["duration"]})
                </div>
                <div class="format-toggles">
                    <button class="format-btn" onclick="toggleFormat('12h')">12h</button>
                    <button class="format-btn active" onclick="toggleFormat('24h')">24h</button>
                </div>
            </div>
            
            <div class="slogan">
                Life moves fast. Stay on time and enjoy every moment!
            </div>
            
            <div class="cities-grid">
                {''.join([f'''
                <div class="city-card {'featured' if city == 'Karachi' else ''}" onclick="setMainCity('{city}')">
                    <div class="city-time">{city_times[city]["time"]}</div>
                    <div class="city-name">{city}</div>
                    <div class="city-country">{city_times[city]["country"]}</div>
                    <div class="city-time-of-day {city_times[city]["time_of_day"].lower()}">{city_times[city]["time_of_day"]}</div>
                    <div class="utc-offset">UTC{city_times[city]["utc_offset"]}</div>
                </div>
                ''' for city in city_times.keys()])}
                
                <div class="add-city" onclick="showAllCities()">
                    <div class="add-city-icon">+</div>
                    <div class="add-city-text">Add Another City</div>
                </div>
            </div>
            
            <div class="all-cities" id="allCities" style="display: none;">
                <h2>All Available Cities</h2>
                <div class="cities-list">
                    {''.join([f'''
                    <div class="city-item" onclick="setMainCity('{city}')">
                        <div class="city-item-name">{city}</div>
                        <div class="city-item-country">{data["country"]}</div>
                    </div>
                    ''' for city, data in WORLD_CITIES.items()])}
                </div>
            </div>
        </div>
        
        <script>
            let currentFormat = '24h';
            let updateInterval;
            let currentMainCity = 'Karachi';
            let currentTheme = 'dark';

            function updateTime() {{
                fetch(`/api/time/${{currentMainCity}}`)
                    .then(response => response.json())
                    .then(data => {{
                        document.getElementById('mainTime').textContent = data.time;
                    }})
                    .catch(error => console.error('Error:', error));
            }}
            
            function setTheme(theme) {{
                document.body.className = ''; // Clear all classes
                if (theme !== 'dark') {{
                   document.body.classList.add(theme + '-theme');
                }}
                
                // Update theme button states
                document.querySelectorAll('.theme-btn').forEach(btn => btn.classList.remove('active'));
                document.querySelector(`.theme-btn[onclick="setTheme('${{theme}}')"]`).classList.add('active');
            }}
            
            function toggleFormat(format) {{
                currentFormat = format;
                document.querySelectorAll('.format-btn').forEach(btn => btn.classList.remove('active'));
                event.target.classList.add('active');
                // Format toggle logic would go here
            }}
            
            function setMainCity(city) {{
                currentMainCity = city;
                fetch(`/api/time/${{city}}`)
                    .then(response => response.json())
                    .then(data => {{
                        document.getElementById('mainTime').textContent = data.time;
                        document.querySelector('.main-location').textContent = `${{city}}, ${{data.country || ''}}`;
                        document.querySelector('.main-date').textContent = data.date;
                        document.querySelector('.sun-info').innerHTML = 
                            `Sun ☀️: ${{data.sunrise_sunset.sunrise}} - ${{data.sunrise_sunset.sunset}} (${{data.sunrise_sunset.duration}})`;
                    }})
                    .catch(error => console.error('Error:', error));
                
                // Hide all cities section if open
                document.getElementById('allCities').style.display = 'none';
            }}
            
            function showAllCities() {{
                const allCities = document.getElementById('allCities');
                allCities.style.display = allCities.style.display === 'none' ? 'block' : 'none';
            }}
            
            // Enhanced search functionality
            document.getElementById('searchInput').addEventListener('input', function(e) {{
                const searchTerm = e.target.value.toLowerCase().trim();
                
                if (searchTerm.length === 0) {{
                    // Show all cities when search is empty
                    document.querySelectorAll('.city-item').forEach(item => {{
                        item.style.display = 'block';
                    }});
                    document.querySelectorAll('.city-card').forEach(card => {{
                        card.style.display = 'block';
                    }});
                    return;
                }}
                
                // Search in all cities section
                const cityItems = document.querySelectorAll('.city-item');
                cityItems.forEach(item => {{
                    const cityName = item.querySelector('.city-item-name').textContent.toLowerCase();
                    const country = item.querySelector('.city-item-country').textContent.toLowerCase();
                    
                    if (cityName.includes(searchTerm) || country.includes(searchTerm)) {{
                        item.style.display = 'block';
                    }} else {{
                        item.style.display = 'none';
                    }}
                }});
                
                // Search in featured cities
                const cityCards = document.querySelectorAll('.city-card');
                cityCards.forEach(card => {{
                    const cityName = card.querySelector('.city-name').textContent.toLowerCase();
                    const country = card.querySelector('.city-country').textContent.toLowerCase();
                    
                    if (cityName.includes(searchTerm) || country.includes(searchTerm)) {{
                        card.style.display = 'block';
                    }} else {{
                        card.style.display = 'none';
                    }}
                }});
                
                // Auto-select first matching city if found
                const matchingCities = Array.from(cityItems).filter(item => 
                    item.style.display !== 'none'
                );
                
                if (matchingCities.length === 1 && searchTerm.length > 2) {{
                    const cityName = matchingCities[0].querySelector('.city-item-name').textContent;
                    setMainCity(cityName);
                }}
            }});
            
            // Set initial theme
            setTheme('dark');
            
            // Update time every second
            updateInterval = setInterval(updateTime, 1000);
        </script>
    </body>
    </html>
    """
    return html_content

@app.route('/api/time/<city>')
def get_time_api(city):
    """API endpoint to get time for a specific city"""
    time_data = get_city_time(city)
    if not time_data:
        return jsonify({"error": "City not found"}), 404
    
    # Add time of day and sunrise/sunset info
    timezone = pytz.timezone(WORLD_CITIES[city]["timezone"])
    now = datetime.now(timezone)
    time_data["time_of_day"] = get_time_of_day(now.hour)
    time_data["sunrise_sunset"] = get_sunrise_sunset(city)
    time_data["country"] = WORLD_CITIES[city]["country"]
    
    return jsonify(time_data)

@app.route('/api/cities')
def get_cities():
    """API endpoint to get all available cities"""
    return jsonify(WORLD_CITIES)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)