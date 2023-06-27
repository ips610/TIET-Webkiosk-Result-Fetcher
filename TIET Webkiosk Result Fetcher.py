from selenium import webdriver
from selenium.webdriver.common.by import By
import time

max_attempts = 5
current_attempt = 1
desired_url = "https://webkiosk.thapar.edu/StudentFiles/StudentPage.jsp"

# Set up the Chrome webdriver
driver = webdriver.Chrome()

while current_attempt <= max_attempts:
    # Perform login
    driver.get("https://webkiosk.thapar.edu")
    username = driver.find_element(By.NAME, 'MemberCode')
    password = driver.find_element(By.NAME, 'Password')
    login_button = driver.find_element(By.NAME, 'BTNSubmit')

    username.send_keys(102203274)  # enter your own username
    password.send_keys(54321)  # enter your own password
    login_button.click()

    time.sleep(10)  # Add a small delay to allow the page to load

    if driver.current_url == desired_url:
        print("Success")

        # to perform further tasks on the opened webpage 
        while True:
            try:
                pass  # You can perform additional actions or tests here
            except KeyboardInterrupt:
                break  # Exit the loop on keyboard interrupt (e.g., press Ctrl+C)

        break
    
    current_attempt += 1
    print(f"Attempt {current_attempt} failed. Retrying...")


# Clean up
driver.quit()
