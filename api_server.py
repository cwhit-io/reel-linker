#!/usr/bin/env python3
"""
Web API for Reel Link Scraper
Exposes reel scraping functionality via REST endpoints.
"""

import sys
import time
import json
from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions

app = Flask(__name__)

def get_facebook_reel():
    """Fetch the first reel link from Facebook profile."""
    url = "https://www.facebook.com/blackhawkmin/reels/"
    
    try:
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        
        time.sleep(3)
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href*='/reel/']"))
        )
        
        reel_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/reel/']")
        
        if reel_links:
            first_reel = reel_links[0].get_attribute("href")
            if not first_reel.startswith("http"):
                first_reel = "https://www.facebook.com" + first_reel
            driver.quit()
            return first_reel
        
        driver.quit()
        return None
            
    except Exception as e:
        print(f"Error fetching Facebook reel: {e}")
        return None


def get_instagram_reel():
    """Fetch the first reel link from Instagram profile."""
    url = "https://www.instagram.com/bhawkministries/"
    
    try:
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        
        time.sleep(3)
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(2)
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
        )
        
        all_links = driver.find_elements(By.TAG_NAME, "a")
        for link in all_links:
            href = link.get_attribute("href")
            if href and "/reel/" in href:
                driver.quit()
                return href
        
        driver.quit()
        return None
        
    except Exception as e:
        print(f"Error fetching Instagram reel: {e}")
        return None


def get_youtube_short():
    """Fetch the latest YouTube short from the Shorts page."""
    url = "https://www.youtube.com/@blackhawkministrieslive/shorts"
    
    try:
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        
        time.sleep(4)
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(2)
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
        )
        
        all_links = driver.find_elements(By.TAG_NAME, "a")
        for link in all_links:
            href = link.get_attribute("href")
            if href and "/shorts/" in href:
                if not href.startswith("http"):
                    href = "https://www.youtube.com" + href
                driver.quit()
                return href
        
        driver.quit()
        return None
        
    except Exception as e:
        print(f"Error fetching YouTube short: {e}")
        return None


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({"status": "healthy"}), 200


@app.route('/api/reels', methods=['GET'])
def get_all_reels():
    """
    Fetch all reel links.
    GET /api/reels
    """
    try:
        facebook = get_facebook_reel()
        instagram = get_instagram_reel()
        youtube = get_youtube_short()
        
        return jsonify({
            "success": True,
            "data": {
                "facebook": facebook,
                "instagram": instagram,
                "youtube": youtube
            }
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/facebook', methods=['GET'])
def get_facebook():
    """
    Fetch Facebook reel link.
    GET /api/facebook
    """
    try:
        reel = get_facebook_reel()
        if reel:
            return jsonify({
                "success": True,
                "platform": "facebook",
                "url": reel
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": "No reel found"
            }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/instagram', methods=['GET'])
def get_instagram():
    """
    Fetch Instagram reel link.
    GET /api/instagram
    """
    try:
        reel = get_instagram_reel()
        if reel:
            return jsonify({
                "success": True,
                "platform": "instagram",
                "url": reel
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": "No reel found"
            }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/youtube', methods=['GET'])
def get_youtube():
    """
    Fetch YouTube short link.
    GET /api/youtube
    """
    try:
        short = get_youtube_short()
        if short:
            return jsonify({
                "success": True,
                "platform": "youtube",
                "url": short
            }), 200
        else:
            return jsonify({
                "success": False,
                "error": "No short found"
            }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/', methods=['GET'])
def index():
    """API documentation endpoint."""
    return jsonify({
        "name": "Reel Link Scraper API",
        "version": "1.0.0",
        "endpoints": {
            "GET /health": "Health check",
            "GET /api/reels": "Fetch all reel links (Facebook, Instagram, YouTube)",
            "GET /api/facebook": "Fetch Facebook reel link",
            "GET /api/instagram": "Fetch Instagram reel link",
            "GET /api/youtube": "Fetch YouTube short link"
        },
        "example": "curl http://localhost:5000/api/reels"
    }), 200


if __name__ == '__main__':
    # Run on all interfaces, port 5000
    app.run(host='0.0.0.0', port=5000, debug=False)
