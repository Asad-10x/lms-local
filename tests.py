from main import login_cms
from main import get_assignments
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
import time

# This file is for unit testing of main.py

# The first module I built is CMS_Login and the code segment for it's testing is:
def validate_login(driver):
    try:
        # Wait for the page to load
        dashboard_url = "https://cms.bahria.edu.pk/Sys/Student/Dashboard.aspx"  # Replace with actual post-login URL
        WebDriverWait(driver, 10).until(EC.url_to_be(dashboard_url))
        print("Login successful! Redirected to the dashboard.")
    except:
        try:
            # If login fails, check for the error message in the alert div
            error_message = driver.find_element(By.CSS_SELECTOR, ".alert-danger").text
            print(f"Login failed: {error_message}")
        except Exception as e:
            print("Login failed, and no error message found. Exception:", str(e))

def go_to_lms(driver, name):
    try:
        left_pane = driver.find_element(By.ID, "sideMenuList")
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", left_pane)
        time.sleep(1)
        # Wait for the LMS link to be clickable and then click it
        lms_link = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, name)))
        lms_link.click()
        print("Navigated to the LMS successfully!")
        time.sleep(10);
    except Exception as e:
        print(f"Failed to navigate to LMS: {e}")
    # Check if a new window/tab was opened
    time.sleep(2)  # Give it some time to open the new tab
    handles = driver.window_handles
    if len(handles) > 1:
      driver.switch_to.window(handles[1])
      print("Switched to the LMS window/tab.")
      time.sleep(10)

def test_get_assignments(driver):
    try:
        get_assignments(driver)
        # Wait for the title or specific element of Assignments page to confirm navigation
        WebDriverWait(driver, 10).until(EC.title_contains("Assignments"))
        print("Navigated to the Assignments page successfully!")
    except Exception as e:
        print(f"Failed to navigate to Assignments: {e}")


# Example test
def run_test():
    enrollment = "03-134202-013"
    password = "TeenWolf849_"
    branch = "Lahore Campus"
    role = "Student"
    lms_name = "Go To LMS"

    # Perform login
    driver = webdriver.Chrome() 
    login_cms(driver, enrollment, password, branch, role)

    # Validate login
    validate_login(driver)

    # Go To LMS
    go_to_lms(driver, lms_name)

    # Go to Assignments
    test_get_assignments(driver)

    # Clean up and close the browser
    driver.quit()

# Run the test
if __name__ == "__main__":
    run_test()

