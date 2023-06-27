import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pynput import keyboard

# Set up logging
logging.basicConfig(
    filename='logfile.txt',
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)

# Set up the Chrome webdriver
driver = webdriver.Chrome()

# Flag to indicate if the program should exit
exit_flag = False


def on_key_press(key):
    global exit_flag
    exit_flag = True
    return False


try:
    # Perform login
    driver.get("https://webkiosk.thapar.edu")
    username = driver.find_element(By.NAME, "MemberCode")
    password = driver.find_element(By.NAME, "Password")
    login_button = driver.find_element(By.NAME, "BTNSubmit")

    username.send_keys("test")  # enter your own username
    password.send_keys("test")  # enter your own password
    login_button.click()

    logger.info("Login successful")
    print("Success", flush=True)  # Print "Success" on the screen

    # Wait for the desired page to load after login
    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_to_be("https://webkiosk.thapar.edu/StudentFiles/StudentPage.jsp"))

    # Start listening for key press events
    with keyboard.Listener(on_press=on_key_press) as listener:
        while True:
            if exit_flag or len(driver.window_handles) == 0:
                logger.info("Key press detected. Exiting the loop.")
                print("Key press detected. Exiting the loop.", flush=True)
                break

            # You can perform additional actions or tests here

finally:
    # Clean up resources
    driver.quit()
    logger.info("Driver quit. Exiting the program.")