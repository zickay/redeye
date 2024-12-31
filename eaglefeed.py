import os
import random
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller
from faker import Faker
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize Faker
fake = Faker()

# Function to get user inputs
def get_user_inputs():
    """Prompt the user for required inputs."""
    urls = input("Enter the URLs to visit (comma-separated): ").strip().split(",")
    min_users = int(input("Enter the minimum number of users to mimic: ").strip())
    max_users = int(input("Enter the maximum number of users to mimic: ").strip())
    min_time = int(input("Enter the minimum activity time (in minutes): ").strip())
    max_time = int(input("Enter the maximum activity time (in minutes): ").strip())
    bot_behavior = input("Enter bot behavior (e.g., 'browse', 'play_media', 'both'): ").strip().lower()

    return urls, min_users, max_users, min_time, max_time, bot_behavior

# Function to setup ChromeDriver with Bright Data proxy
def setup_chrome_driver(proxy_url):
    """Setup the ChromeDriver using the Bright Data proxy."""
    chromedriver_autoinstaller.install()  # Automatically installs the correct version of ChromeDriver
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"--user-agent={fake.user_agent()}")
    options.add_argument(f"--proxy-server={proxy_url}")
    return webdriver.Chrome(service=Service(), options=options)

# Function to simulate browsing behavior
def simulate_browsing(driver, url, activity_time):
    """Simulate browsing behavior for the given time."""
    driver.get(url)
    time.sleep(2)  # Allow the page to load

    # Simulate browsing by scrolling
    scroll_pause_time = random.uniform(1, 3)  # Random pause between scrolls
    for _ in range(3):  # Scroll down 3 times
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        time.sleep(scroll_pause_time)

    # Scroll back up
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(scroll_pause_time)

# Function to simulate media playback behavior
def simulate_media_playback(driver, url, activity_time):
    """Simulate media playback behavior for the given time."""
    driver.get(url)
    time.sleep(2)  # Allow the page to load

    # Click play button (assuming a play button exists)
    try:
        play_button = driver.find_element(By.XPATH, '//button[contains(text(),"Play")]')
        play_button.click()
        time.sleep(5)  # Wait to ensure media starts playing
        print(f"Started playing media on {url}.")
    except Exception as e:
        print(f"Failed to start media playback on {url}: {e}")

    # Simulate keeping media playing for the required time
    time.sleep(activity_time)

# Main function to execute the bot's workflow
def main():
    """Main function to execute the bot's workflow."""
    # Get user inputs
    urls, min_users, max_users, min_time, max_time, bot_behavior = get_user_inputs()

    # Get proxy URL from environment variables
    proxy_url = os.getenv("BRIGHTDATA_PROXY_URL")
    if not proxy_url:
        print("Proxy URL is missing from environment variables.")
        return

    # Randomly determine the number of users to simulate
    num_users = random.randint(min_users, max_users)
    print(f"Simulating {num_users} users...")

    # Create a Chrome driver instance for each simulated user
    for user in range(1, num_users + 1):
        print(f"Starting activity for user {user}...")

        # Setup ChromeDriver with the proxy
        driver = setup_chrome_driver(proxy_url)

        try:
            # Randomly select a URL and activity time
            url = random.choice(urls)
            activity_time = random.randint(min_time, max_time) * 60  # Convert to seconds
            print(f"Visiting {url} for {activity_time // 60} minutes...")

            if bot_behavior == 'browse':
                simulate_browsing(driver, url, activity_time)
            elif bot_behavior == 'play_media':
                simulate_media_playback(driver, url, activity_time)
            elif bot_behavior == 'both':
                # Simulate browsing and media playback
                if random.choice([True, False]):
                    simulate_browsing(driver, url, activity_time)
                else:
                    simulate_media_playback(driver, url, activity_time)
            else:
                print(f"Invalid bot behavior: {bot_behavior}")

        except Exception as e:
            print(f"Error for user {user}: {e}")
        finally:
            driver.quit()

        # Random delay between users
        time.sleep(random.uniform(2, 5))

    print("Bot activity completed.")

if __name__ == "__main__":
    main()
