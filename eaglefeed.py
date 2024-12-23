import os
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains

# --- Configurable Variables ---
# Fetch environment variables
IP_FILE_PATH = os.getenv("IP_FILE_PATH")  # Path to proxies.txt file
CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")  # Path to ChromeDriver
RAILWAY_ENV = os.getenv("RAILWAY_PROD", "false")  # Set by Railway, 'true' in production

# Helper function to get user input
def get_user_inputs():
    websites = input("Enter the website URLs (comma-separated): ").split(",")
    min_users = int(input("Enter minimum number of users to simulate: "))
    max_users = int(input("Enter maximum number of users to simulate: "))
    min_time = int(input("Enter minimum time (in minutes) for user activity: "))
    max_time = int(input("Enter maximum time (in minutes) for user activity: "))
    task_type = input("Enter task type (Media Playback, Browsing, Both): ").lower()

    return {
        "websites": [url.strip() for url in websites],
        "min_users": min_users,
        "max_users": max_users,
        "min_time": min_time,
        "max_time": max_time,
        "task_type": task_type,
    }

# Bot functionality
def mimic_user_behavior(driver, website, duration):
    print(f"[INFO] Visiting website: {website}")
    driver.get(website)
    start_time = time.time()
    
    while time.time() - start_time < duration:
        actions = ActionChains(driver)
        actions.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(random.uniform(1, 3))
        actions.send_keys(Keys.PAGE_UP).perform()
        time.sleep(random.uniform(1, 3))

def play_media(driver, website, duration):
    print(f"[INFO] Playing media on website: {website}")
    driver.get(website)
    time.sleep(5)
    try:
        play_button = driver.find_element(By.TAG_NAME, "button")
        play_button.click()
        print(f"[INFO] Media playback started on {website}")
        time.sleep(duration)
    except Exception as e:
        print(f"[ERROR] Could not play media on {website}: {e}")

# Main bot logic
def main():
    user_inputs = get_user_inputs()
    websites = user_inputs["websites"]
    num_users = random.randint(user_inputs["min_users"], user_inputs["max_users"])
    task_type = user_inputs["task_type"]
    
    print(f"[INFO] Simulating {num_users} users for task: {task_type}")
    
    # Load proxies if available
    proxies = []
    if IP_FILE_PATH and os.path.exists(IP_FILE_PATH):
        with open(IP_FILE_PATH, "r") as f:
            proxies = [line.strip() for line in f.readlines()]
    
    for user in range(num_users):
        website = random.choice(websites)
        duration = random.randint(user_inputs["min_time"], user_inputs["max_time"]) * 60
        
        # Setup WebDriver
        options = webdriver.ChromeOptions()
        if proxies:
            proxy = random.choice(proxies)
            options.add_argument(f"--proxy-server={proxy}")
        
        driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=options)
        try:
            if task_type == "media playback":
                play_media(driver, website, duration)
            elif task_type == "browsing":
                mimic_user_behavior(driver, website, duration)
            elif task_type == "both":
                if user % 2 == 0:
                    play_media(driver, website, duration)
                else:
                    mimic_user_behavior(driver, website, duration)
        except Exception as e:
            print(f"[ERROR] Error during user simulation: {e}")
        finally:
            driver.quit()
            print(f"[INFO] User simulation complete for {website}")

if __name__ == "__main__":
    main()
