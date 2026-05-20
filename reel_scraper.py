#!/usr/bin/env python3
"""
Script to fetch the first reel link from Facebook and Instagram profiles.
"""

import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions

def get_facebook_reel():
    """
    Fetch the first reel link from Facebook profile.
    """
    url = "https://www.facebook.com/blackhawkmin/reels/"
    
    try:
        # Set up Chrome options
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        driver = webdriver.Chrome(options=chrome_options)
        print(f"Opening Facebook reels page: {url}")
        driver.get(url)
        
        # Wait for reels to load
        time.sleep(3)
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href*='/reel/']"))
        )
        
        # Find the first reel link
        reel_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/reel/']")
        
        if reel_links:
            first_reel = reel_links[0].get_attribute("href")
            # Ensure it's a full URL
            if not first_reel.startswith("http"):
                first_reel = "https://www.facebook.com" + first_reel
            print(f"✓ Facebook Reel: {first_reel}")
            return first_reel
        else:
            print("✗ No reel links found on Facebook page")
            return None
            
    except Exception as e:
        print(f"✗ Error fetching Facebook reel: {e}")
        return None
    finally:
        driver.quit()


def get_instagram_reel():
    """
    Fetch the first reel link from Instagram profile.
    """
    url = "https://www.instagram.com/bhawkministries/"
    
    try:
        # Set up Chrome options
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        driver = webdriver.Chrome(options=chrome_options)
        print(f"Opening Instagram profile: {url}")
        driver.get(url)
        
        # Wait for page to load
        time.sleep(3)
        
        # Scroll down to load posts
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(2)
        
        # Look for reel links
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
        )
        
        all_links = driver.find_elements(By.TAG_NAME, "a")
        for link in all_links:
            href = link.get_attribute("href")
            if href and "/reel/" in href:
                print(f"✓ Instagram Reel: {href}")
                return href
        
        print("✗ No reel links found on Instagram profile")
        return None
        
    except Exception as e:
        print(f"✗ Error fetching Instagram reel: {e}")
        return None
    finally:
        driver.quit()


def get_youtube_short():
    """
    Fetch the latest YouTube short from the Shorts page.
    """
    url = "https://www.youtube.com/@blackhawkministrieslive/shorts"
    
    try:
        # Set up Chrome options
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        driver = webdriver.Chrome(options=chrome_options)
        print(f"Opening YouTube Shorts: {url}")
        driver.get(url)
        
        # Wait for page to load
        time.sleep(4)
        
        # Scroll down to load shorts
        driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(2)
        
        # Look for short links
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, "a"))
        )
        
        all_links = driver.find_elements(By.TAG_NAME, "a")
        for link in all_links:
            href = link.get_attribute("href")
            if href and "/shorts/" in href:
                # Ensure it's a full URL
                if not href.startswith("http"):
                    href = "https://www.youtube.com" + href
                print(f"✓ YouTube Short: {href}")
                return href
        
        print("✗ No shorts found on YouTube channel")
        return None
        
    except Exception as e:
        print(f"✗ Error fetching YouTube short: {e}")
        return None
    finally:
        driver.quit()


def main():
    """
    Main function to fetch reel links from all platforms.
    """
    print("=" * 60)
    print("Reel Link Scraper")
    print("=" * 60)
    
    facebook_reel = get_facebook_reel()
    print()
    instagram_reel = get_instagram_reel()
    print()
    youtube_short = get_youtube_short()
    
    print()
    print("=" * 60)
    print("Results:")
    print("=" * 60)
    print(f"Facebook: {facebook_reel or 'Not found'}")
    print(f"Instagram: {instagram_reel or 'Not found'}")
    print(f"YouTube: {youtube_short or 'Not found'}")
    print("=" * 60)
    
    return {
        "facebook": facebook_reel,
        "instagram": instagram_reel,
        "youtube": youtube_short
    }


if __name__ == "__main__":
    main()
