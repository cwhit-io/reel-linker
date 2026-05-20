#!/usr/bin/env python3
"""
Lightweight alternative using requests and BeautifulSoup.
This script attempts to fetch reel links using simple HTTP requests.
Note: This may not work if the site requires JavaScript rendering.
"""

import requests
from bs4 import BeautifulSoup
import json
import re

def get_facebook_reel_lightweight():
    """
    Attempt to fetch Facebook reel link using requests + BeautifulSoup.
    Note: This may fail due to Facebook's JavaScript-heavy rendering.
    """
    url = "https://www.facebook.com/blackhawkmin/reels/"
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        print(f"Fetching: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, "html.parser")
        
        # Look for reel links in various possible locations
        reel_links = []
        
        # Try to find reel links
        for link in soup.find_all("a", href=True):
            if "/reel/" in link["href"]:
                reel_links.append(link["href"])
        
        if reel_links:
            first_reel = reel_links[0]
            if not first_reel.startswith("http"):
                first_reel = "https://www.facebook.com" + first_reel
            print(f"✓ Facebook Reel: {first_reel}")
            return first_reel
        else:
            print("✗ No reel links found on Facebook")
            return None
            
    except Exception as e:
        print(f"✗ Error fetching Facebook reel: {e}")
        return None


def get_instagram_reel_lightweight():
    """
    Attempt to fetch Instagram reel link using requests + BeautifulSoup.
    Note: Instagram heavily uses JavaScript, so this likely won't work.
    """
    url = "https://www.instagram.com/bhawkministries/"
    
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        print(f"Fetching: {url}")
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # Instagram stores data in JSON within the page
        # Look for the __data__ or similar JSON structures
        match = re.search(r'window\._sharedData\s*=\s*({.*?});', response.text)
        
        if match:
            data = json.loads(match.group(1))
            # Navigate through the JSON structure to find reels
            # This is complex and varies, but we can try common paths
            print(f"✓ Found Instagram data (structure varies, manual parsing needed)")
            return data
        
        print("✗ Could not extract Instagram data")
        return None
        
    except Exception as e:
        print(f"✗ Error fetching Instagram reel: {e}")
        print("   (Instagram blocks requests from bots - use Selenium version instead)")
        return None


def main():
    print("=" * 60)
    print("Reel Link Scraper (Lightweight Version)")
    print("=" * 60)
    print("Note: This version may not work due to JavaScript rendering requirements")
    print()
    
    facebook_reel = get_facebook_reel_lightweight()
    print()
    instagram_reel = get_instagram_reel_lightweight()
    
    print()
    print("=" * 60)
    print("Note: For better results, use reel_scraper.py with Selenium")
    print("=" * 60)


if __name__ == "__main__":
    main()
