from main import login_cms
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

# Example test
def run_test():
    enrollment = "03-134202-013"
    password = "TeenWolf849_"
    branch = "Lahore Campus"
    role = "Student"

    # Perform login
    driver = webdriver.Chrome() 
    login_cms(driver, enrollment, password)

    # Validate login
    validate_login(driver)

    # Clean up and close the browser
    driver.quit()

# Run the test
if __name__ == "__main__":
    run_test()

