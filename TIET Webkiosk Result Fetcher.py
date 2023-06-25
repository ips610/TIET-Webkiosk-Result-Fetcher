from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up the Chrome webdriver
driver = webdriver.Chrome()

# Perform login
driver.get("https://webkiosk.thapar.edu")
username = driver.find_element(By.NAME, 'MemberCode')
password = driver.find_element(By.NAME, 'Password')
login_button = driver.find_element(By.NAME, 'BTNSubmit')

username.send_keys('test') #enter your own username
password.send_keys('test') #enter your own password
login_button.click()

print("Success")

# Wait for the desired page to load after login
wait = WebDriverWait(driver, 10)
wait.until(EC.url_to_be("https://webkiosk.thapar.edu/StudentFiles/StudentPage.jsp"))

while True:
    try:
        pass  # You can perform additional actions or tests here
    except KeyboardInterrupt:
        break  # Exit the loop on keyboard interrupt (e.g., press Ctrl+C)
