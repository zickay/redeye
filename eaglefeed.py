import os
import random
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import chromedriver_autoinstaller
from faker import Faker

# Initialize Faker
fake = Faker()

def get_user_inputs():
    """Prompt the user for required inputs."""
    urls = input("Enter the URLs to visit (comma-separated): ").strip().split(",")
    min_users = int(input("Enter the minimum number of users to mimic: ").strip())
    max_users = int(input("Enter the maximum number of users to mimic: ").strip())
    min_time = int(input("Enter the minimum activity time (in minutes): ").strip())
    max_time = int(input("Enter the maximum activity time (in minutes): ").strip())
    proxies_path = input("Enter the path to the proxies file: ").strip()
    return urls, min_users, max_users, min_time, max_time, proxies_path

def setup_chrome_driver():
    """Automatically installs and sets up ChromeDriver."""
    chromedriver_autoinstaller.install()  # Automatically installs the correct version of ChromeDriver
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"--user-agent={fake.user_agent()}")
    return webdriver.Chrome(service=Service(), options=options)

def load_proxies(proxies_path):
    """Load proxies from the specified file."""
    if not os.path.exists(proxies_path):
        raise FileNotFoundError(f"Proxies file not found at: {proxies_path}")
    with open(proxies_path, "r") as file:
        return [line.strip() for line in file.readlines() if line.strip()]

def set_proxy(options, proxy):
    """Configure Chrome options to use a specific proxy."""
    options.add_argument(f"--proxy-server={proxy}")

def mimic_user_activity(driver, url, activity_time):
    """Simulate user activity on the specified URL."""
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

def main():
    """Main function to execute the bot's workflow."""
    # Get user inputs
    urls, min_users, max_users, min_time, max_time, proxies_path = get_user_inputs()

    # Load proxies
    proxies = load_proxies(proxies_path)
    if not proxies:
        print("No proxies found. Exiting.")
        return

    # Randomly determine the number of users to simulate
    num_users = random.randint(min_users, max_users)
    print(f"Simulating {num_users} users...")

    # Create a Chrome driver instance for each simulated user
    for user in range(1, num_users + 1):
        print(f"Starting activity for user {user}...")

        # Randomly assign a proxy
        proxy = random.choice(proxies)
        print(f"Using proxy: {proxy}")

        # Setup ChromeDriver with the proxy
        options = Options()
        set_proxy(options, proxy)
        driver = setup_chrome_driver()

        try:
            # Randomly select a URL and activity time
            url = random.choice(urls)
            activity_time = random.randint(min_time, max_time) * 60  # Convert to seconds
            print(f"Visiting {url} for {activity_time // 60} minutes...")

            # Mimic user activity
            mimic_user_activity(driver, url, activity_time)
        except Exception as e:
            print(f"Error for user {user}: {e}")
        finally:
            driver.quit()

        # Random delay between users
        time.sleep(random.uniform(2, 5))

    print("Bot activity completed.")

if __name__ == "__main__":
    main()
