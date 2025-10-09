from flask import Flask
from datetime import datetime
import pytz

# Flask application initialize karna
app = Flask(__name__)

# Pakistan ka time zone set karna
pakistan_timezone = pytz.timezone("Asia/Karachi")

@app.route('/')
def get_time():
    """
    Yeh function current Pakistan waqt return karta hai.
    """
    # Pakistan ke time zone ke hisab se waqt hasil karna
    now_pakistan = datetime.now(pakistan_timezone)
    
    # Waqt ko behtar format mein dikhana
    time_str = now_pakistan.strftime("%H:%M:%S")
    date_str = now_pakistan.strftime("%d-%B-%Y")
    
    # HTML response tayyar karna
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Pakistan Time</title>
        <style>
            body {{ 
                display: flex; 
                justify-content: center; 
                align-items: center; 
                height: 100vh; 
                margin: 0; 
                background-color: #2c3e50; 
                color: #ecf0f1; 
                font-family: 'Arial', sans-serif; 
            }}
            .time-container {{ 
                text-align: center; 
                border: 2px solid #3498db; 
                padding: 40px; 
                border-radius: 15px; 
                background-color: #34495e; 
                box-shadow: 0 10px 20px rgba(0,0,0,0.2);
            }}
            h1 {{ 
                font-size: 3em; 
                margin-bottom: 10px;
                color: #3498db;
            }}
            p {{ 
                font-size: 5em; 
                margin: 0; 
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="time-container">
            <h1>Pakistan Mein Abhi Waqt Hai</h1>
            <p>{time_str}</p>
            <p style="font-size: 2em; margin-top: 10px;">{date_str}</p>
        </div>
    </body>
    </html>
    """
    return html_content

# Application ko run karna
if __name__ == '__main__':
    # '0.0.0.0' par host karna taake yeh container ke bahar se access ho sake
    app.run(host='0.0.0.0', port=5000)

