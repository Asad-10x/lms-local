# To add dependencies, i'll have to run `pip freeze > requirements.txt` later. 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC 
import os
import requests
import time

# # Setting up webdriver
# driver = webdriver.Chrome()

# func to login_portal
def login_cms(driver, enrollment, password, branch, role):
  driver.get("https://cms.bahria.edu.pk/Logins/Student/Login.aspx")

  # Fill out the form
  driver.find_element(By.ID, "BodyPH_tbEnrollment").send_keys(enrollment)  ## enrollment
  driver.find_element(By.ID, "BodyPH_tbPassword").send_keys(password)  ## password

  ## Dropdown for selecting institute:
  branch_dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "BodyPH_ddlInstituteID")))
  branch_dropdown.click()

  select_branch = Select(branch_dropdown)

  select_branch.select_by_visible_text(branch)

  # Dropdown for selecting role
  role_dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "BodyPH_ddlSubUserType")))

  # Use Select class to handle the <select> dropdown
  select_role = Select(role_dropdown)

  # Select the appropriate Role (Student)
  select_role.select_by_visible_text(role)

  driver.find_element(By.ID, "BodyPH_btnLogin").click()

def go_to_lms(name):
  left_pane = driver.find_element(By.ID, "sideMenuList")
  driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", left_pane)
  time.sleep(1)
  lms_link = WebDriverWait(driver, 10).until((EC.element_to_be_clickable((By.LINK_TEXT, name))))
  lms_link.click()
  # Check if a new window/tab was opened
  time.sleep(2)  # Give it some time to open the new tab
  handles = driver.window_handles
  if len(handles) > 1:
    driver.switch_to.window(handles[1])
    print("Switched to the LMS window/tab.")
    time.sleep(10)

def get_assignments(driver):
  try:
    driver.get("https://lms.bahria.edu.pk/Student/Assignments.php")
    WebDriverWait(driver, 10).until(EC.title_contains("Assignments"))
    print("Navigated to the Assignments page successfully!")
  # time.sleep(10)
  except Exception as e:
    print(f"Failed to navigate to Assignments page: {e}")

# Example usage
if __name__ == "__main__":
  driver = webdriver.Chrome()
  enrollment = "03-134202-013"
  password = "TeenWolf849_"
  branch = "Lahore Campus"
  role = "Student"
  lms_name = "Go To LMS"
  login_cms(driver, enrollment, password, branch, role)
  go_to_lms(lms_name)
  get_assignments(driver)
  driver.quit()



