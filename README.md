# Reel Link Scraper

A Python script to fetch the latest reel/short links from Facebook, Instagram, and YouTube profiles.

Includes:
- **CLI Script** (`reel_scraper.py`) - Command-line scraper
- **Web API** (`api_server.py`) - Flask REST API for programmatic access
- **Docker Container** - Lightweight containerized deployment with web API

## Quick Start

### Option 1: Command Line

```bash
pip install -r requirements.txt
sudo apt-get install chromium-chromedriver
python reel_scraper.py
```

### Option 2: Web API (Docker)

```bash
docker-compose up -d
```

The API will be available at `http://localhost:5000`

### Option 3: Web API (Manual)

```bash
pip install -r requirements.txt
python api_server.py
```

## API Endpoints

When running the API server, you can access:

- **`GET /`** - API documentation and available endpoints
- **`GET /health`** - Health check
- **`GET /api/reels`** - Fetch all reel links
- **`GET /api/facebook`** - Fetch Facebook reel
- **`GET /api/instagram`** - Fetch Instagram reel
- **`GET /api/youtube`** - Fetch YouTube short

## API Usage Examples

### Get all reels:
```bash
curl http://localhost:5000/api/reels
```

### Get Facebook reel:
```bash
curl http://localhost:5000/api/facebook
```

### Get Instagram reel:
```bash
curl http://localhost:5000/api/instagram
```

### Get YouTube short:
```bash
curl http://localhost:5000/api/youtube
```

## Docker Setup

### Build and run with Docker Compose:

```bash
cd /home/blackhawk/reel-linker
docker-compose up -d
```

### Check logs:
```bash
docker-compose logs -f reel-scraper
```

### Stop the container:
```bash
docker-compose down
```

### Build manually:
```bash
docker build -t reel-scraper .
docker run -p 5000:5000 reel-scraper
```

## OpenAI Skill Integration

See `openai_skill.json` for OpenAI Actions schema. The API is unauthenticated and ready to be integrated as an OpenAI custom action.

Example skill registration:
- **API URL**: `http://your-server:5000`
- **Authentication**: None
- **Endpoints**: GET /api/reels, /api/facebook, /api/instagram, /api/youtube
