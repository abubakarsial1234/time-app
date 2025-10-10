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
                background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%);
                min-height: 100vh;
                color: #333;
                transition: all 0.3s ease;
            }}
            
            body.dark-mode {{
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
                color: #e0e0e0;
            }}
            
            body.white-theme {{
                background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
                color: #333;
            }}
            
            body.white-theme.dark-mode {{
                background: linear-gradient(135deg, #f0f0f0 0%, #e8e8e8 100%);
                color: #333;
            }}
            
            .container {{
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
            }}
            
            .header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 40px;
                background: rgba(255, 255, 255, 0.1);
                backdrop-filter: blur(10px);
                padding: 20px;
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.2);
                transition: all 0.3s ease;
            }}
            
            body.dark-mode .header {{
                background: rgba(0, 0, 0, 0.3);
                border: 1px solid rgba(255, 255, 255, 0.1);
            }}
            
            body.white-theme .header {{
                background: rgba(255, 255, 255, 0.8);
                border: 1px solid rgba(0, 0, 0, 0.1);
            }}
            
            body.white-theme.dark-mode .header {{
                background: rgba(255, 255, 255, 0.9);
                border: 1px solid rgba(0, 0, 0, 0.2);
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
                background: white;
                border-radius: 50%;
                display: flex; 
                align-items: center;
                justify-content: center; 
                font-size: 20px;
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
                padding: 8px 12px;
                border: 2px solid white;
                border-radius: 20px;
                background: transparent;
                color: white;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.3s ease;
                font-size: 12px;
            }}
            
            .theme-btn:hover {{
                background: white;
                color: #ff6b35;
            }}
            
            .theme-btn.active {{
                background: white;
                color: #ff6b35;
            }}
            
            body.dark-mode .theme-btn {{
                border-color: #e0e0e0;
                color: #e0e0e0;
            }}
            
            body.dark-mode .theme-btn:hover {{
                background: #e0e0e0;
                color: #1a1a2e;
            }}
            
            body.dark-mode .theme-btn.active {{
                background: #e0e0e0;
                color: #1a1a2e;
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
                color: #ff6b35;
            }}
            
            .main-clock {{
                background: rgba(255, 255, 255, 0.95);
                border-radius: 30px;
                padding: 60px;
                margin-bottom: 40px;
                text-align: center;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
                backdrop-filter: blur(10px);
                transition: all 0.3s ease;
            }}
            
            body.dark-mode .main-clock {{
                background: rgba(0, 0, 0, 0.4);
                color: #e0e0e0;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
            }}
            
            body.white-theme .main-clock {{
                background: rgba(255, 255, 255, 0.98);
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.05);
            }}
            
            .main-time {{
                font-size: 120px;
                font-weight: 300;
                color: #333;
                margin-bottom: 20px;
                letter-spacing: -2px;
            }}
            
            .main-location {{
                font-size: 32px;
                color: #666;
                margin-bottom: 10px;
                font-weight: 500;
            }}
            
            .main-date {{
                font-size: 24px;
                color: #888;
                margin-bottom: 30px;
            }}
            
            .sun-info {{
                font-size: 18px;
                color: #666;
                margin-bottom: 20px;
            }}
            
            .format-toggles {{
                display: flex;
                gap: 10px;
                justify-content: center;
            }}
            
            .format-btn {{
                padding: 8px 16px;
                border: 2px solid #ddd;
                border-radius: 20px;
                background: transparent;
                color: #666;
                cursor: pointer;
                transition: all 0.3s ease;
            }}
            
            .format-btn.active {{
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
                background: rgba(255, 255, 255, 0.95);
                border-radius: 20px;
                padding: 30px;
                text-align: center;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                cursor: pointer;
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }}
            
            body.dark-mode .city-card {{
                background: rgba(0, 0, 0, 0.4);
                border: 1px solid rgba(255, 255, 255, 0.1);
                color: #e0e0e0;
            }}
            
            body.white-theme .city-card {{
                background: rgba(255, 255, 255, 0.98);
                border: 1px solid rgba(0, 0, 0, 0.1);
            }}
            
            .city-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 15px 30px rgba(0, 0, 0, 0.1);
            }}
            
            .city-card.featured {{
                background: #333;
                color: white;
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
                border-color: #ff6b35;
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
            <!-- Header -->
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
                        <button class="theme-btn active" onclick="setTheme('default')">Orange</button>
                        <button class="theme-btn" onclick="setTheme('white')">White</button>
                        <button class="theme-btn" onclick="toggleDarkMode()">🌙 Dark</button>
                    </div>
                    <button class="btn">Log In</button>
                    <button class="btn">Get the App</button>
                </div>
            </div>
            
            <!-- Main Clock Display -->
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
            
            <!-- Slogan -->
            <div class="slogan">
                Life moves fast. Stay on time and enjoy every moment!
            </div>
            
            <!-- Featured Cities Grid -->
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
            
            <!-- All Cities Section -->
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
            let currentTheme = 'default';
            let isDarkMode = false;
            
            function updateTime() {{
                fetch(`/api/time/${{currentMainCity}}`)
                    .then(response => response.json())
                    .then(data => {{
                        document.getElementById('mainTime').textContent = data.time;
                    }})
                    .catch(error => console.error('Error:', error));
            }}
            
            function setTheme(theme) {{
                currentTheme = theme;
                document.body.classList.remove('white-theme');
                if (theme === 'white') {{
                    document.body.classList.add('white-theme');
                }}
                
                // Update theme button states
                document.querySelectorAll('.theme-btn').forEach(btn => {{
                    btn.classList.remove('active');
                    if (btn.textContent.toLowerCase().includes(theme)) {{
                        btn.classList.add('active');
                    }}
                }});
            }}
            
            function toggleDarkMode() {{
                isDarkMode = !isDarkMode;
                document.body.classList.toggle('dark-mode');
                
                // Update dark mode button
                const darkBtn = document.querySelector('.theme-btn[onclick="toggleDarkMode()"]');
                darkBtn.textContent = isDarkMode ? '☀️ Light' : '🌙 Dark';
                darkBtn.classList.toggle('active', isDarkMode);
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

