import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pynput import keyboard
from selenium.common.exceptions import WebDriverException

# Set up logging
logging.basicConfig(
    filename="logfile.txt",
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)

# Set up the Chrome webdriver
driver = webdriver.Chrome()

# Flag to indicate if the program should exit
# exit_flag = False


def on_key_press(key):
    global exit_flag
    exit_flag = True
    return False

def get_user_credentials():
    # global exit_flag

    # Prompt the user for the username
    print("Enter your username:")
    username = input()

    # Prompt the user for the password
    print("Enter your password:")
    password = input()

    # Set the exit flag to True to exit the listener
    # exit_flag = True

    return username, password


try:
    # Perform login
    try:

        # Start listening for key press events
        with keyboard.Listener(on_press=on_key_press) as listener:
        # Prompt the user for credentials
            username_arg, password_arg = get_user_credentials()
            driver.get("https://webkiosk.thapar.edu")
            username = driver.find_element(By.NAME, "MemberCode")
            password = driver.find_element(By.NAME, "Password")
            login_button = driver.find_element(By.NAME, "BTNSubmit")

            username.send_keys(username_arg)  # enter your own username
            password.send_keys(password_arg)  # enter your own password
            login_button.click()

            

            # Wait for the desired page to load after login
            wait = WebDriverWait(driver, 10)
            login_success = wait.until(
                EC.url_to_be("https://webkiosk.thapar.edu/StudentFiles/StudentPage.jsp")
            )
            if login_success:
                logger.info("Login successful")
                print("Success", flush=True)  # Print "Success" on the screen
            else:
                raise WebDriverException("Wrong Credentials")
                
        
            # Start listening for key press events
            with keyboard.Listener(on_press=on_key_press) as listener:
                while True:
                    if len(driver.window_handles) == 0:
                        logger.info("Key press detected. Exiting the loop.")
                        print("Key press detected. Exiting the loop.", flush=True)
                        break

                # You can perform additional actions or tests here

    except WebDriverException:
        print("Wrong Credentials", flush=True)

finally:
    # Clean up resources
    driver.quit()
    logger.info("Driver quit. Exiting the program.")