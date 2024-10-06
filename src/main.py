# To add dependencies, i'll have to run `pip freeze > requirements.txt` later. 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC 
import os
import requests
import time
import logging

# Configure the logging
logging.basicConfig(
  level=logging.INFO,
  format="%(asctime)s [%(levelname)s] %(message)s",
  handlers=[
    logging.FileHandler("lms_scrapper.log"),
    logging.StreamHandler()
  ]
)
logger = logging.getLogger(__name__)

# func to login_portal
def login_cms(driver, enrollment, password, branch, role):
  try:
    driver.get("https://cms.bahria.edu.pk/Logins/Student/Login.aspx")
    logger.info("Navigated to the CMS login page.")

    # Fill out the form
    driver.find_element(By.ID, "BodyPH_tbEnrollment").send_keys(enrollment)  ## enrollment
    driver.find_element(By.ID, "BodyPH_tbPassword").send_keys(password)  ## password
    logger.info("Entered the enrollment and password.")

    ## Dropdown for selecting institute:
    branch_dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "BodyPH_ddlInstituteID")))
    branch_dropdown.click()
    logger.info("Clicked on the branch dropdown.")
    select_branch = Select(branch_dropdown)
    logger.info("Selected the branch dropdown.")
    select_branch.select_by_visible_text(branch)
    logger.info("Selected the branch: %s", branch)
    # Dropdown for selecting role
    role_dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "BodyPH_ddlSubUserType")))

    # Use Select class to handle the <select> dropdown
    select_role = Select(role_dropdown)

    # Select the appropriate Role (Student)
    select_role.select_by_visible_text(role)
    logger.info("Selected the role: %s", role)
    driver.find_element(By.ID, "BodyPH_btnLogin").click()
    logger.info("Clicked on the login button.")
  except Exception as e:
    logger.error("Failed to login: %s", e)


def go_to_lms(name):
  try:
    left_pane = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "sideMenuList")))
    driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", left_pane)
    lms_link = WebDriverWait(driver, 10).until((EC.element_to_be_clickable((By.LINK_TEXT, name))))
    lms_link.click()
    logger.info("Clicked the go to lms link.")
    # Check if a new window/tab was opened
    handles = driver.window_handles
    if len(handles) > 1:
      driver.switch_to.window(handles[1])
      logger.info("Switched to the LMS window/tab.")
  except Exception as e:
    logger.error("Failed to navigate to LMS: %s", e)

def get_assignments(driver):
  try:
    driver.get("https://lms.bahria.edu.pk/Student/Assignments.php")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".bg-gray.pad")))
    logger.info("Navigated to the Assignments page successfully!")
    
    # Open dropdown and Select course
    course_dropdown = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "courseId")))
    select_course = Select(course_dropdown)

    # to find the total number of courses
    total_courses = len(select_course.options)
    logger.info("Total courses: %s", total_courses)
    
    # loop through all the courses
    for i in range(1, total_courses):
      select_course = Select(driver.find_element(By.ID, "courseId"))
      select_course.select_by_index(i)
      logger.info(f"Selected course at index {i}: {select_course.options[i].text}")
      
  except Exception as e:
    logger.error(f"Failed to navigate to Assignments page: {e}")

# Driver Program
if __name__ == "__main__":
  driver = webdriver.Chrome()
  enrollment = os.getenv("LMS_ENROLLMENT")
  password = os.getenv("LMS_PASSWORD")
  branch = "Lahore Campus"
  role = "Student"
  lms_name = "Go To LMS"
  login_cms(driver, enrollment, password, branch, role)
  go_to_lms(lms_name)
  get_assignments(driver)
  driver.quit()