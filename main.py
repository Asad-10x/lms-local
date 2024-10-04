# To add dependencies, i'll have to run `pip freeze > requirements.txt` later. 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC 
import os
import requests
import time

# Setting up webdriver
driver = webdriver.Chrome()

# func to login_portal
def login_cms(enrollment, password):
  driver.get("https://cms.bahria.edu.pk/Logins/Student/Login.aspx")

  # Fill out the form
  driver.find_element(By.ID, "BodyPH_tbEnrollment").send_keys(enrollment)  ## enrollment
  driver.find_element(By.ID, "BodyPH_tbPassword").send_keys(password)  ## password

  ## Dropdown for selecting institute:
  branch_dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "BodyPH_ddlInstituteID")))
  branch_dropdown.click()

  select_branch = Select(branch_dropdown)

  select_branch.select_by_visible_text("Lahore Campus")

  # Dropdown for selecting role
  role_dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "BodyPH_ddlSubUserType")))

  # Use Select class to handle the <select> dropdown
  select_role = Select(role_dropdown)

  # Select the appropriate Role (Student)
  select_role.select_by_visible_text("Student")

  driver.find_element(By.ID, "BodyPH_btnLogin").click()

## Wait for page to load or give error
  time.sleep(5)

  try:
  # Assuming successful login redirects to a new URL or dashboard
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


# Example usage
enrollment = "03-134202-013"
password = "TeenWolf849_"

login_cms(enrollment, password)



