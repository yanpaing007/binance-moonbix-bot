import time
import threading
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy
import selenium.common.exceptions as selenium_exceptions
from config import config

drivers = []  # Keep track of all driver instances

def human_like_delay(min_delay=1, max_delay=3):
    time.sleep(random.uniform(min_delay, max_delay))

def human_like_move_and_click(driver, element):
    try:
        # Move mouse smoothly to the element
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        human_like_delay(0.5, 1.5)  # Slight delay before clicking
        element.click()
        human_like_delay(1, 2)  # Slight delay after clicking
    except selenium_exceptions.WebDriverException as e:
        print(f"Error during human-like move and click: {e}")

def wait_and_click(driver, by, identifier, timeout, name):
    try:
        element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, identifier)))
        human_like_move_and_click(driver, element)
        print(f"Clicked {name}")
        return True
    except (selenium_exceptions.TimeoutException, selenium_exceptions.WebDriverException) as e:
        print(f"Error while clicking {identifier}:")
        return False

def open_chrome(url, profile_directory, position, size):
    global drivers
    options = Options()
    options.add_argument(f"--user-data-dir={profile_directory}")
    options.add_experimental_option("detach", True)
    if config["headless"]:
        options.add_argument("--headless")
        options.add_argument("--mute-audio")
        
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/124.0.2478.50 Version/17.0 Mobile/15E148 Safari/604.1"
    options.add_argument(f"user-agent={user_agent}")

    # Disable various features to make headless mode less detectable
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(options=options)
    drivers.append(driver)  # Add driver to the global list for cleanup
    print("..........................")

    try:
        driver.get(url)
        driver.set_window_position(*position)
        driver.set_window_size(*size)
        
        attempt = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__APP"]/div/div[1]/div/div[2]/div[2]/div[3]/div[2]')))
        remaining_attempts = int(attempt.text.split('/')[0])
        balance = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.bn-flex.Game_entry__info__15l1V > div.Game_entry__coin__33Nan'))).text
        print(f"Remaining attempts: {remaining_attempts} and Balance: {balance}")
        
        play_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "Game_entry__playBtn__1Gi2c")))

        if play_button:
            
         while True:
            attempt = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__APP"]/div/div[1]/div/div[2]/div[2]/div[3]/div[2]')))
            remaining_attempts = int(attempt.text.split('/')[0])
            while remaining_attempts > 0:
                play_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "Game_entry__playBtn__1Gi2c")))
                play_button.click()
                print("Clicked Play button.")
                print("Game Started.")
                time.sleep(1)
                
                canvas = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'canvas')))
                print("Canvas found. Starting to click...")

                end_time = time.time() + 45  # Set end time for 45 seconds
                while time.time() < end_time:
                    try:
                        # Check if the canvas is still present
                        canvas = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.TAG_NAME, 'canvas')))
                        
                        # Perform click action
                        canvas.click()
                        print("Clicked on canvas.")
                        
                        # Sleep for the specified delay before the next click
                        time.sleep(config["click_delay"])
                    except selenium_exceptions.TimeoutException:
                        print("Canvas not found, stopping clicks.")
                        break
                    
                print("Game completed,going back to main...")
                time.sleep(2)
                WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#__APP > div > div > div > svg'))).click()
                # Fetch remaining attempts again after game completes
                print("Sleeping for two seconds before fetching attempts...")
                time.sleep(2)
                attempt = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__APP"]/div/div[1]/div/div[2]/div[2]/div[3]/div[2]')))
                remaining_attempts = int(attempt.text.split('/')[0])
                balance = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.bn-flex.Game_entry__info__15l1V > div.Game_entry__coin__33Nan'))).text
                print(f"Remaining attempts: {remaining_attempts} and Balance: {balance}")
                
            print("No more attempts left. Returning to main page.")
            print("Sleeping for 40 minutes...")
            time.sleep(420)  # 40 minutes sleep

        else:
            print("Play button not found.")
            return

    except Exception as e:
        print("Error:", e)
    finally:
        human_like_delay(1)

def launch_profile(url, profile_directory, position, size, delay):
    try:
        time.sleep(delay)
        open_chrome(url, profile_directory, position, size)
    except Exception as e:
        print(f"Error in launch_profile function: {e}")
        
try:
    url = config["url"]

    profiles = []
    profile_path_base = config["profile_url"]

    window_width = 570
    window_height = 700
    window_border = 5
    window_title_bar = 45

    start = 1
    end = 2

    for i in range(start, end):
        row = (i - 1) // 3 % 2
        col = (i - 1) % 3
        position = (
            col * (window_width + window_border),
            row * (window_height + window_title_bar)
        )
        delay = (i - start) * 10  # Calculate delay based on the current iteration
        profiles.append((f"{profile_path_base}{i}", position, (window_width, window_height), delay))

    threads = []
    for profile_directory, position, size, delay in profiles:
        thread = threading.Thread(target=launch_profile, args=(url, profile_directory, position, size, delay))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    
except KeyboardInterrupt:
    print("Keyboard Interrupted")
finally:
    # Quit all active ChromeDriver instances
    for driver in drivers:
        try:
            #driver.quit()
            print("Closed Chrome session.")
        except Exception as e:
            print(f"Error closing Chrome session: {e}")

    print("Exiting...")