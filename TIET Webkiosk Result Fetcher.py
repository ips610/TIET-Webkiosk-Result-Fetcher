import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, NoSuchElementException
from selenium.webdriver.support.select import Select

# Set up logging
logging.basicConfig(
    filename="logfile.txt",
    filemode="w",
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.DEBUG,
)
logger = logging.getLogger(__name__)

# Set up the Chrome webdriver
driver = webdriver.Chrome()


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

        # Prompt the user for credentials
        username_arg, password_arg = get_user_credentials()
        driver.get("https://webkiosk.thapar.edu")
        username = driver.find_element(By.NAME, "MemberCode")
        password = driver.find_element(By.NAME, "Password")
        login_button = driver.find_element(By.NAME, "BTNSubmit")

        username.send_keys(username_arg)  # enter your own username
        password.send_keys(password_arg)  # enter your own password
        login_button.click()
        driver.maximize_window()

        # Wait for the desired page to load after login
        wait = WebDriverWait(driver, 10)
        login_success = wait.until(
            EC.url_to_be("https://webkiosk.thapar.edu/StudentFiles/StudentPage.jsp")
        )
        if login_success:
            logger.info("Login successful")
            print("Success", flush=True)  # Print "Success" on the screen
            print()

            try:
                # Find the element with src="FrameLeftStudent.jsp" and click it
                frameset = driver.find_element(
                    By.XPATH, "//frame[@src='FrameLeftStudent.jsp']"
                )
                driver.switch_to.frame(frameset)

                # Find the "exam info" div element

                exam_info_div = driver.find_element(
                    By.XPATH,
                    '//div[@class="menutitle" and contains(text(),"Exam. Info.")]',
                )

                exam_info_div.click()

                span_element = exam_info_div.find_element(
                    By.XPATH, "./following-sibling::span"
                )

                a_elements = span_element.find_elements(By.TAG_NAME, "a")

                for a in a_elements:
                    print(a.text)
                print()

                option_choose = input("Enter Option Name to get details: ").lower()
                print("You have chosen: ", option_choose)
                print()
                # User will choose from the options extracted from website

                if option_choose == "exam marks":
                    driver.get(
                        "https://webkiosk.thapar.edu/StudentFiles/Exam/StudentEventMarksView.jsp"
                    )

                wait.until(
                    EC.url_to_be(
                        "https://webkiosk.thapar.edu/StudentFiles/Exam/StudentEventMarksView.jsp"
                    )
                )

                print("MARKS URL OPENED")


                #prompt user for choosing the year of marks to be displayed

                marks_year =  wait.until(EC.element_to_be_clickable((By.XPATH,"//select[@id='exam']")))
                marks_year_select = Select(marks_year)
                marks_year_options = marks_year_select.options

                for option in marks_year_options:
                    print(option.text)
                user_marks_options_choose = int(input("Choose Option: "))
                marks_year_select.select_by_index(user_marks_options_choose - 1)

                
                show_button = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, '//input[@type="submit" and @value="Show"]')
                    )
                )
                show_button.click()
                print("Button Clicked")

            except NoSuchElementException:
                print(
                    "Frame or element not found. Performing alternative action.",
                    flush=True,
                )
                # Perform alternative action or handle the situation

        else:
            raise WebDriverException("Wrong Credentials")


        while True:
            if len(driver.window_handles) == 0:
                logger.info("Key press detected. Exiting the loop.")
                print("Key press detected. Exiting the loop.", flush=True)
                break
            else:
                pass

    except WebDriverException:
        print("Wrong Credentials", flush=True)

except Exception as e:
    logger.error("An error occurred: %s" % str(e))
    print("An error occurred. Check the logs for details.", flush=True)

finally:
    # Clean up resources
    driver.quit()
    logger.info("Driver quit. Exiting the program.")
