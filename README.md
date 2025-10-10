# TimeSpot - World Clock Application

A beautiful, modern world clock application built with Flask that displays times for cities around the world, similar to the TimeSpot design.

## Features

- 🕐 Real-time world clock for 20+ major cities
- 🌅 Sunrise and sunset information
- 🎨 Modern, responsive UI with orange gradient background
- 📱 Mobile-friendly design
- 🔍 Search functionality for cities
- 🌍 UTC offset display
- ⏰ Time of day indicators (Morning, Day, Evening, Night)

## Supported Cities

- London, United Kingdom
- New York, United States
- Los Angeles, United States
- Paris, France
- Tokyo, Japan
- Sydney, Australia
- Dubai, UAE
- Moscow, Russia
- Singapore, Singapore
- Hong Kong, Hong Kong
- Karachi, Pakistan
- Mumbai, India
- Beijing, China
- Toronto, Canada
- São Paulo, Brazil
- Mexico City, Mexico
- Cairo, Egypt
- Johannesburg, South Africa
- Istanbul, Turkey
- Bangkok, Thailand

## Quick Start with Docker

### Build the Docker Image

```bash
docker build -t timespot .
```

### Run the Container

```bash
docker run -p 5000:5000 timespot
```

The application will be available at `http://localhost:5000`

## Development Setup

### Prerequisites

- Python 3.11+
- pip

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## API Endpoints

- `GET /` - Main application interface
- `GET /api/time/<city>` - Get time information for a specific city
- `GET /api/cities` - Get list of all available cities

## Example API Response

```json
{
  "time": "14:30:45",
  "date": "Friday, Jan 24 2025",
  "timezone": "GMT+0000",
  "utc_offset": "+0000",
  "time_of_day": "Day",
  "sunrise_sunset": {
    "sunrise": "07:45",
    "sunset": "18:30",
    "duration": "10h 45m"
  },
  "country": "United Kingdom"
}
```

## Docker Commands

### Build and Run in One Command

```bash
docker build -t timespot . && docker run -p 5000:5000 timespot
```

### Run in Background

```bash
docker run -d -p 5000:5000 --name timespot-app timespot
```

### Stop the Container

```bash
docker stop timespot-app
docker rm timespot-app
```

## Technologies Used

- **Backend**: Flask (Python web framework)
- **Timezone Handling**: pytz library
- **Frontend**: HTML5, CSS3, JavaScript
- **Containerization**: Docker
- **Styling**: Modern CSS with gradients, backdrop filters, and responsive design

## License

This project is open source and available under the MIT License.
