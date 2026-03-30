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
    
    timezone = pytz.timezone(WORLD_CITIES[city_name]["timezone"])
    now = datetime.now(timezone)
    hour = now.hour
    
    if 3 <= now.month <= 9:  
        sunrise_hour = 6
        sunset_hour = 20
    else:  
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
    pakistan_time = get_city_time("Karachi")
    pakistan_sunrise_sunset = get_sunrise_sunset("Karachi")
    
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
        <title>TimeSpot - Premium World Clock</title>
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
        <style>
            :root {{
                --bg-gradient: linear-gradient(135deg, #0f172a 0%, #064e3b 100%);
                --card-bg: rgba(255, 255, 255, 0.03);
                --card-border: rgba(255, 255, 255, 0.1);
                --text-main: #ffffff;
                --text-muted: rgba(255, 255, 255, 0.7);
                --accent: #3DDC84;
                --accent-glow: rgba(61, 220, 132, 0.3);
                --glass-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
            }}

            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
                font-family: 'Outfit', sans-serif;
            }}
            
            body {{ 
                background: var(--bg-gradient);
                min-height: 100vh;
                color: var(--text-main);
                transition: all 0.5s ease;
                position: relative;
                overflow-x: hidden;
            }}
            
            /* Animated Background Glowing Orbs */
            body::before, body::after {{
                content: '';
                position: fixed;
                width: 600px;
                height: 600px;
                border-radius: 50%;
                filter: blur(100px);
                z-index: 0;
                animation: float 20s infinite alternate ease-in-out;
            }}
            
            body::before {{
                top: -100px;
                right: -100px;
                background: radial-gradient(circle, var(--accent-glow) 0%, transparent 70%);
            }}
            
            body::after {{
                bottom: -150px;
                left: -150px;
                background: radial-gradient(circle, rgba(16, 185, 129, 0.2) 0%, transparent 70%);
                animation-delay: -10s;
            }}

            @keyframes float {{
                0% {{ transform: translate(0, 0) scale(1); }}
                50% {{ transform: translate(-50px, 50px) scale(1.1); }}
                100% {{ transform: translate(50px, -50px) scale(0.9); }}
            }}
            
            /* White Theme Colors */
            body.white-theme {{
                --bg-gradient: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
                --card-bg: rgba(255, 255, 255, 0.7);
                --card-border: rgba(255, 255, 255, 1);
                --text-main: #0f172a;
                --text-muted: #64748b;
                --accent: #059669;
                --accent-glow: rgba(5, 150, 105, 0.15);
                --glass-shadow: 0 10px 30px 0 rgba(148, 163, 184, 0.3);
            }}
            
            /* Orange/Sunset Theme Colors */
            body.orange-theme {{
                --bg-gradient: linear-gradient(135deg, #2d1305 0%, #7c2d12 100%);
                --card-bg: rgba(255, 255, 255, 0.05);
                --card-border: rgba(255, 255, 255, 0.15);
                --text-main: #ffffff;
                --text-muted: rgba(255, 255, 255, 0.8);
                --accent: #fb923c;
                --accent-glow: rgba(251, 146, 60, 0.3);
                --glass-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.4);
            }}
            
            .container {{
                max-width: 1100px;
                margin: 0 auto;
                padding: 30px 20px;
                position: relative;
                z-index: 1;
            }}
            
            /* Enhanced Header */
            .header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 50px;
                background: var(--card-bg);
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                padding: 15px 25px;
                border-radius: 100px;
                border: 1px solid var(--card-border);
                box-shadow: var(--glass-shadow);
                transition: all 0.3s ease;
            }}
            
            .logo {{
                display: flex;
                align-items: center;
                gap: 12px;
                font-size: 24px;
                font-weight: 700;
                color: var(--text-main);
                letter-spacing: -0.5px;
            }}
            
            .logo-icon {{
                width: 42px;
                height: 42px;
                background: var(--accent);
                border-radius: 50%;
                display: flex; 
                align-items: center;
                justify-content: center; 
                font-size: 22px;
                color: #fff;
                box-shadow: 0 0 15px var(--accent-glow);
            }}
            
            /* Enhanced Search Bar */
            .search-bar {{
                flex: 1;
                max-width: 450px;
                margin: 0 20px;
                position: relative;
            }}
            
            .search-bar input {{
                width: 100%;
                padding: 14px 20px 14px 45px;
                border: 1px solid var(--card-border);
                border-radius: 50px;
                background: rgba(255, 255, 255, 0.05);
                font-size: 15px;
                outline: none;
                color: var(--text-main);
                transition: all 0.3s ease;
            }}

            body.white-theme .search-bar input {{
                background: rgba(255, 255, 255, 0.8);
            }}
            
            .search-bar input:focus {{
                background: rgba(255, 255, 255, 0.1);
                border-color: var(--accent);
                box-shadow: 0 0 0 3px var(--accent-glow);
            }}

            .search-bar::before {{
                content: '🔍';
                position: absolute;
                left: 15px;
                top: 50%;
                transform: translateY(-50%);
                font-size: 16px;
                opacity: 0.6;
            }}
            
            .header-buttons {{
                display: flex;
                gap: 12px;
                align-items: center;
            }}
            
            .theme-controls {{
                display: flex;
                gap: 8px;
                background: rgba(0,0,0,0.1);
                padding: 5px;
                border-radius: 30px;
                margin-right: 15px;
            }}
            
            body.white-theme .theme-controls {{ background: rgba(0,0,0,0.05); }}

            .theme-btn {{
                padding: 8px 16px;
                border: none;
                border-radius: 20px;
                background: transparent;
                color: var(--text-muted);
                font-weight: 500;
                cursor: pointer;
                transition: all 0.3s ease;
                font-size: 13px;
            }}
            
            .theme-btn:hover {{ color: var(--text-main); }}
            
            .theme-btn.active {{
                background: var(--card-bg);
                color: var(--text-main);
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                border: 1px solid var(--card-border);
            }}
            
            .btn {{
                padding: 12px 24px;
                border: none;
                border-radius: 30px;
                background: rgba(255, 255, 255, 0.1);
                color: var(--text-main);
                font-weight: 600;
                font-size: 14px;
                cursor: pointer;
                transition: all 0.3s ease;
                border: 1px solid var(--card-border);
            }}
            
            .btn-primary {{
                background: var(--accent);
                color: #fff;
                border: none;
                box-shadow: 0 4px 15px var(--accent-glow);
            }}

            .btn:hover {{
                transform: translateY(-2px);
                background: rgba(255, 255, 255, 0.2);
            }}

            .btn-primary:hover {{
                background: var(--accent);
                filter: brightness(1.1);
            }}
            
            /* Premium Main Clock Area */
            .main-clock {{
                background: var(--card-bg);
                border-radius: 40px;
                padding: 70px 40px;
                margin-bottom: 50px;
                text-align: center;
                box-shadow: var(--glass-shadow);
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                border: 1px solid var(--card-border);
                position: relative;
                overflow: hidden;
            }}
            
            .main-clock::before {{
                content: '';
                position: absolute;
                top: 0; left: 0; right: 0;
                height: 4px;
                background: linear-gradient(90deg, transparent, var(--accent), transparent);
                opacity: 0.8;
            }}
            
            .main-time {{
                font-size: 140px;
                font-weight: 300;
                color: var(--text-main);
                margin-bottom: 10px;
                letter-spacing: -4px;
                font-variant-numeric: tabular-nums;
                text-shadow: 0 10px 30px rgba(0,0,0,0.2);
                line-height: 1;
            }}
            
            .main-location {{
                font-size: 36px;
                color: var(--text-main);
                margin-bottom: 8px;
                font-weight: 600;
                letter-spacing: -0.5px;
            }}
            
            .main-date {{
                font-size: 20px;
                color: var(--text-muted);
                margin-bottom: 25px;
                font-weight: 400;
            }}
            
            .sun-info {{
                display: inline-flex;
                align-items: center;
                gap: 15px;
                background: rgba(0,0,0,0.2);
                padding: 12px 25px;
                border-radius: 50px;
                font-size: 16px;
                color: var(--text-main);
                margin-bottom: 30px;
                border: 1px solid var(--card-border);
            }}

            body.white-theme .sun-info {{ background: rgba(255,255,255,0.5); }}
            
            .format-toggles {{
                display: flex;
                gap: 10px;
                justify-content: center;
            }}
            
            .format-btn {{
                padding: 8px 20px;
                border: 1px solid var(--card-border);
                border-radius: 20px;
                background: transparent;
                color: var(--text-muted);
                cursor: pointer;
                transition: all 0.3s ease;
                font-weight: 600;
                font-size: 14px;
            }}
            
            .format-btn.active {{
                background: var(--accent);
                color: #fff;
                border-color: var(--accent);
                box-shadow: 0 4px 15px var(--accent-glow);
            }}
            
            .slogan {{
                text-align: center;
                font-size: 28px;
                margin-bottom: 50px;
                font-weight: 300;
                background: linear-gradient(to right, var(--text-main), var(--text-muted));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}
            
            /* Enhanced Grid & Cards */
            .cities-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
                gap: 25px;
                margin-bottom: 50px;
            }}
            
            .city-card {{
                background: var(--card-bg);
                border-radius: 24px;
                padding: 30px 25px;
                text-align: center; 
                transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
                cursor: pointer;
                backdrop-filter: blur(16px);
                -webkit-backdrop-filter: blur(16px);
                border: 1px solid var(--card-border);
                box-shadow: var(--glass-shadow);
                position: relative;
                overflow: hidden;
            }}
            
            .city-card:hover {{
                transform: translateY(-10px) scale(1.02);
                border-color: rgba(255, 255, 255, 0.3);
            }}

            .city-card::after {{
                content: '';
                position: absolute;
                top: 0; left: 0; right: 0; bottom: 0;
                background: radial-gradient(circle at top right, rgba(255,255,255,0.1), transparent 60%);
                opacity: 0;
                transition: opacity 0.3s ease;
            }}

            .city-card:hover::after {{ opacity: 1; }}
            
            .city-card.featured {{
                border: 1px solid var(--accent);
                box-shadow: 0 10px 30px var(--accent-glow);
            }}
            
            .city-time {{
                font-size: 46px;
                font-weight: 300;
                margin-bottom: 5px;
                color: var(--text-main);
                font-variant-numeric: tabular-nums;
            }}
            
            .city-name {{
                font-size: 22px;
                font-weight: 600;
                margin-bottom: 4px;
                color: var(--text-main);
            }}
            
            .city-country {{
                font-size: 14px;
                color: var(--text-muted);
                margin-bottom: 15px;
                font-weight: 400;
            }}
            
            .city-time-of-day {{
                font-size: 13px;
                font-weight: 600;
                padding: 6px 14px;
                border-radius: 20px;
                display: inline-block;
                margin-bottom: 12px;
                text-transform: uppercase;
                letter-spacing: 1px;
            }}
            
            .city-time-of-day.day {{ background: rgba(253, 224, 71, 0.2); color: #fde047; }}
            .city-time-of-day.night {{ background: rgba(56, 189, 248, 0.2); color: #38bdf8; }}
            .city-time-of-day.morning {{ background: rgba(251, 146, 60, 0.2); color: #fb923c; }}
            .city-time-of-day.evening {{ background: rgba(192, 132, 252, 0.2); color: #c084fc; }}
            
            body.white-theme .city-time-of-day.day {{ background: #fef08a; color: #854d0e; }}
            body.white-theme .city-time-of-day.night {{ background: #bae6fd; color: #075985; }}
            body.white-theme .city-time-of-day.morning {{ background: #fed7aa; color: #9a3412; }}
            body.white-theme .city-time-of-day.evening {{ background: #e9d5ff; color: #581c87; }}

            .utc-offset {{
                font-size: 13px;
                color: var(--text-muted);
                background: rgba(0,0,0,0.1);
                padding: 4px 10px;
                border-radius: 8px;
            }}
            
            .add-city {{
                background: transparent;
                border: 2px dashed var(--card-border);
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                opacity: 0.7;
            }}
            
            .add-city:hover {{
                opacity: 1;
                border-color: var(--text-muted);
                background: rgba(255,255,255,0.05);
            }}
            
            .add-city-icon {{
                font-size: 40px;
                margin-bottom: 10px;
                font-weight: 300;
            }}
            
            .add-city-text {{
                font-size: 16px;
                font-weight: 500;
            }}
            
            /* Responsive */
            @media (max-width: 900px) {{
                .header {{ flex-wrap: wrap; border-radius: 20px; }}
                .search-bar {{ order: 3; max-width: 100%; margin: 15px 0 0 0; }}
            }}

            @media (max-width: 768px) {{
                .main-time {{ font-size: 80px; }}
                .main-location {{ font-size: 28px; }}
                .main-clock {{ padding: 40px 20px; }}
                .slogan {{ font-size: 20px; }}
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
                <div class="header-buttons">
                    <div class="theme-controls">
                        <button class="theme-btn" onclick="setTheme('orange')">Sunset</button>
                        <button class="theme-btn" onclick="setTheme('white')">Light</button>
                        <button class="theme-btn active" onclick="setTheme('dark')">Dark</button>
                    </div>
                    <button class="btn">Log In</button>
                    <button class="btn btn-primary">Get App</button>
                </div>
                <div class="search-bar">
                    <input type="text" placeholder="Search for cities or timezones..." id="searchInput">
                </div>
            </div>
            
            <div class="main-clock">
                <div class="main-time" id="mainTime">{pakistan_time["time"]}</div>
                <div class="main-location">Karachi, {WORLD_CITIES["Karachi"]["country"]}</div>
                <div class="main-date">{pakistan_time["date"]}</div>
                <div class="sun-info">
                    <span>☀️ {pakistan_sunrise_sunset["sunrise"]}</span>
                    <span>-</span>
                    <span>🌙 {pakistan_sunrise_sunset["sunset"]}</span>
                    <span style="opacity:0.6; font-size: 14px; margin-left:10px;">({pakistan_sunrise_sunset["duration"]})</span>
                </div>
                <div class="format-toggles">
                    <button class="format-btn" onclick="toggleFormat('12h')">12h</button>
                    <button class="format-btn active" onclick="toggleFormat('24h')">24h</button>
                </div>
            </div>
            
            <div class="slogan">
                Life moves fast. Stay on time, beautifully.
            </div>
            
            <div class="cities-grid">
                {''.join([f'''
                <div class="city-card {'featured' if city == 'Karachi' else ''}" onclick="setMainCity('{city}')">
                    <div class="city-time">{city_times[city]["time"]}</div>
                    <div class="city-name">{city}</div>
                    <div class="city-country">{city_times[city]["country"]}</div>
                    <div class="city-time-of-day {city_times[city]["time_of_day"].lower()}">{city_times[city]["time_of_day"]}</div>
                    <br>
                    <span class="utc-offset">UTC{city_times[city]["utc_offset"]}</span>
                </div>
                ''' for city in city_times.keys()])}
                
                <div class="city-card add-city" onclick="document.getElementById('searchInput').focus()">
                    <div class="add-city-icon">+</div>
                    <div class="add-city-text">Add City</div>
                </div>
            </div>
        </div>
        
        <script>
            let currentFormat = '24h';
            let updateInterval;
            let currentMainCity = 'Karachi';

            function updateTime() {{
                fetch(`/api/time/${{currentMainCity}}`)
                    .then(response => response.json())
                    .then(data => {{
                        document.getElementById('mainTime').textContent = data.time;
                    }})
                    .catch(error => console.error('Error:', error));
            }}
            
            function setTheme(theme) {{
                document.body.className = ''; 
                if (theme !== 'dark') {{
                   document.body.classList.add(theme + '-theme');
                }}
                
                document.querySelectorAll('.theme-btn').forEach(btn => btn.classList.remove('active'));
                event.target.classList.add('active');
            }}
            
            function toggleFormat(format) {{
                currentFormat = format;
                document.querySelectorAll('.format-btn').forEach(btn => btn.classList.remove('active'));
                event.target.classList.add('active');
            }}
            
            function setMainCity(city) {{
                currentMainCity = city;
                fetch(`/api/time/${{city}}`)
                    .then(response => response.json())
                    .then(data => {{
                        document.getElementById('mainTime').textContent = data.time;
                        document.querySelector('.main-location').textContent = `${{city}}, ${{data.country || ''}}`;
                        document.querySelector('.main-date').textContent = data.date;
                        
                        // Update UI to highlight selected
                        document.querySelectorAll('.city-card').forEach(c => c.classList.remove('featured'));
                        // Simplistic matching for demo
                        let cards = document.querySelectorAll('.city-name');
                        cards.forEach(c => {{
                            if(c.textContent === city) c.parentElement.classList.add('featured');
                        }});
                    }})
                    .catch(error => console.error('Error:', error));
            }}
            
            updateInterval = setInterval(updateTime, 1000);
        </script>
    </body>
    </html>
    """
    return html_content

@app.route('/api/time/<city>')
def get_time_api(city):
    time_data = get_city_time(city)
    if not time_data:
        return jsonify({"error": "City not found"}), 404
    
    timezone = pytz.timezone(WORLD_CITIES[city]["timezone"])
    now = datetime.now(timezone)
    time_data["time_of_day"] = get_time_of_day(now.hour)
    time_data["sunrise_sunset"] = get_sunrise_sunset(city)
    time_data["country"] = WORLD_CITIES[city]["country"]
    
    return jsonify(time_data)

@app.route('/api/cities')
def get_cities():
    return jsonify(WORLD_CITIES)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
