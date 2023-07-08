import logging
import stdiomask
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
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")  # Run Chrome in headless mode (without GUI)
# driver = webdriver.Chrome(options=chrome_options)
driver = webdriver.Chrome()


def get_user_credentials():
    # global exit_flag

    # Prompt the user for the username
    print("Enter your username:")
    username = input()

    # Prompt the user for the password
    password = stdiomask.getpass("Enter your password: \n", mask="*")

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

                    # prompt user for choosing the year of marks to be displayed

                    marks_year = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//select[@id='exam']"))
                    )
                    marks_year_select = Select(marks_year)
                    marks_year_options = marks_year_select.options

                    for option in marks_year_options:
                        print(option.text)
                    user_marks_options_choose = int(input("Choose Option: "))
                    user_marks_options_choose_text = marks_year_select.select_by_index(
                        user_marks_options_choose - 1
                    )

                    show_button = wait.until(
                        EC.element_to_be_clickable(
                            (By.XPATH, '//input[@type="submit" and @value="Show"]')
                        )
                    )
                    show_button.click()
                    print("Button Clicked")

                    table = wait.until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//table[@id='table-1']")
                        )
                    )

                    # Find all the table rows except the first row (heading row)
                    rows = table.find_elements(By.XPATH, ".//tr")

                    # Iterate through the rows and print their cell values
                    with open("marks.txt", "w") as file1:
                        # Iterate over rows (excluding the heading row) and extract cell data
                        for row in rows[1:]:
                            cells = row.find_elements(By.TAG_NAME, "td")

                            # Extract the cell data
                            exam_code = cells[1].text.lstrip()
                            subject_code = cells[2].text.lstrip()
                            event_subevent = cells[3].text.lstrip()
                            full_marks = cells[4].text.lstrip()
                            obtained_marks = cells[5].text.lstrip()
                            weightage = cells[6].text.lstrip()
                            effective_marks = cells[7].text.lstrip()
                            status = cells[8].text.lstrip()

                            # Format and print the marks
                            print(f"Exam Code: {exam_code}")
                            print(f"Subject (Code): {subject_code}")
                            print(f"Event/Subevent: {event_subevent}")
                            print(f"Full Marks: {full_marks}")
                            print(f"Obtained Marks: {obtained_marks}")
                            print(f"Weightage: {weightage}")
                            print(f"Effective Marks: {effective_marks}")
                            print(f"Status: {status}")
                            print()

                            # Format the marks
                            formatted_marks = (
                                f"Exam Code: {exam_code}\n"
                                f"Subject (Code): {subject_code}\n"
                                f"Event/Subevent: {event_subevent}\n"
                                f"Full Marks: {full_marks}\n"
                                f"Obtained Marks: {obtained_marks}\n"
                                f"Weightage: {weightage}\n"
                                f"Effective Marks: {effective_marks}\n"
                                f"Status: {status}\n\n"
                            )

                            # Write the formatted marks to the text file
                            file1.write(formatted_marks)

                elif option_choose == "cgpa" or option_choose == "sgpa":
                    driver.get(
                        "https://webkiosk.thapar.edu/StudentFiles/Exam/StudCGPAReport.jsp"
                    )

                    wait.until(
                        EC.url_to_be(
                            "https://webkiosk.thapar.edu/StudentFiles/Exam/StudCGPAReport.jsp"
                        )
                    )

                    print("CGPA URL OPENED")

                    table = wait.until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//table[@id='table-1']")
                        )
                    )

                    # Find all the table rows except the first row (heading row)
                    rows = table.find_elements(By.XPATH, ".//tr")

                    # Iterate through the rows and print their cell values
                    with open("cgpa.txt", "w") as file2:
                        # Iterate over rows (excluding the heading row) and extract cell data
                        for row in rows[1:]:
                            cells = row.find_elements(By.TAG_NAME, "td")

                            # Extract the cell data
                            exam_code = cells[0].text.lstrip()
                            course_credit = cells[1].text.lstrip()
                            earned_credit = cells[2].text.lstrip()
                            points_secured = cells[3].text.lstrip()
                            sgpa = cells[4].text.lstrip()
                            cgpa = cells[5].text.lstrip()

                            # Format and print the cgpa information
                            print(f"Exam Code: {exam_code}")
                            print(f"Course Credits: {course_credit}")
                            print(f"Earned Credits: {earned_credit}")
                            print(f"Points Secured: {points_secured}")
                            print(f"SGPA: {sgpa}")
                            print(f"CGPA: {cgpa}")
                            print()

                            # Format the cg info
                            formatted_cg_info = (
                                f"Exam Code: {exam_code}\n"
                                f"Subject (Code): {course_credit}\n"
                                f"Event/Subevent: {earned_credit}\n"
                                f"Full Marks: {points_secured}\n"
                                f"Obtained Marks: {sgpa}\n"
                                f"Weightage: {cgpa}\n\n"
                            )

                            # Write the formatted cg info to the text file
                            file2.write(formatted_cg_info)

                elif option_choose == "exam grades":
                    driver.get(
                        "https://webkiosk.thapar.edu/StudentFiles/Exam/StudentEventGradesView.jsp"
                    )

                    wait.until(
                        EC.url_to_be(
                            "https://webkiosk.thapar.edu/StudentFiles/Exam/StudentEventGradesView.jsp"
                        )
                    )

                    print("Exam Grades URL OPENED")

                    table = wait.until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//table[@id='table-1']")
                        )
                    )

                    # Find all the table rows except the first row (heading row)
                    rows = table.find_elements(By.XPATH, ".//tr")

                    # Iterate through the rows and print their cell values
                    with open("grades.txt", "w") as file3:
                        # Iterate over rows (excluding the heading row) and extract cell data
                        for row in rows[1:]:
                            cells = row.find_elements(By.TAG_NAME, "td")

                            # Extract the cell data
                            subject = cells[0].text.lstrip()
                            exam_code = cells[1].text.lstrip()
                            marks_obtained = cells[2].text.lstrip()
                            max_marks = cells[3].text.lstrip()
                            grade_awarded = cells[4].text.lstrip()

                            # Format and print the cgpa information
                            print(f"Subject: {subject}")
                            print(f"Exam Code: {exam_code}")
                            print(f"Marks Obtained: {marks_obtained}")
                            print(f"Max. Marks: {max_marks}")
                            print(f"Grade Awarded: {grade_awarded}")

                            print()

                            # Format the cg info
                            formatted_grades = (
                                f"Subject: {subject}\n"
                                f"Exam Code: {exam_code}\n"
                                f"Marks Obtained: {marks_obtained}\n"
                                f"Max. Marks: {max_marks}\n"
                                f"Grade Awarded: {grade_awarded}\n\n"
                            )

                            # Write the formatted cg info to the text file
                            file3.write(formatted_grades)

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
                logger.info("You have closed the window. Program Stopped !")
                print("You have closed the window. Program Stopped !", flush=True)
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
