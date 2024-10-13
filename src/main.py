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

def navigate_to_assignments(driver):
  try:
    driver.get("https://lms.bahria.edu.pk/Student/Assignments.php")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".bg-gray.pad")))
    logger.info("Navigated to the assignments page successfully!")
  except Exception as e:
    logger.error("Failed to navigate to Assignments: %s", e)
    return False
  return True

def select_course(driver, index):
  try:
    course_dropdown = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "course")))
    select_course = Select(course_dropdown)
    select_course.select_by_index(index)
    select_course_name = select_course.options[index].text
    logger.info(f"Selected course at inded {index}: {select_course_name}")
    return True, select_course_name
  except Exception as e:
    logger.warning(f"Failed to select course at index {index}: {e}")
    return False, None

#def fetch_assignment_data(driver, course_name):
  try:
    # Wait for the assignment table to load
    # assignment_table = WebDriverWait(driver, 10).until(
        # EC.presence_of_element_located((By.CSS_SELECTOR, "table table-hover"))
    # )

    assignment_rows = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "tbody > tr")))
    if assignment_rows:
      logger.info(f"Found {len(assignment_rows)} assignments for course: {course_name}")
    else:
      logger.info(f"No assignments found for course: {course_name}")
      return

    # Loop through each assignment row and extract details
    for row in assignment_rows:
        try:
          assignment_no = row.find_element(By.CSS_SELECTOR, "td:nth-child(1)").text.strip()
          title = row.find_element(By.CSS_SELECTOR, "td:nth-child(2)").text.strip()

          # Extract the assignment download link if available
          assignment_link_element = row.find_element(By.CSS_SELECTOR, "td:nth-child(3) a")
          assignment_link = assignment_link_element.get_attribute("href") if assignment_link_element else "N/A"

          # Log assignment details
          logger.info(f"Assignment No: {assignment_no}, Title: {title}, Download Link: {assignment_link}")

          # Download the assignment if a link is present
          if assignment_link != "N/A":
            logger.info(f"Downloading assignment {assignment_no} from {assignment_link}")
            driver.get(assignment_link)
            time.sleep(2)  # Wait for the download to start; adjust as needed for your environment

        except Exception as e:
            logger.error(f"Error while extracting assignment data: {e}")

  except Exception as e:
      logger.error(f"Error while fetching assignment data for course {course_name}: {e}")

def process_courses(driver):
  try:
    # Find the course dropdown and initialize the select object
    course_dropdown = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "courseId")))
    select_course = Select(course_dropdown)

    # Find the total number of courses
    total_courses = len(select_course.options) -1 # because select course itself appears as a option :| nice engineering BULC ;)
    logger.info("Total courses: %s", total_courses)

    # Loop through each course and process assignments
    for i in range(1, total_courses+1):
      try:
        course_dropdown = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "courseId")))
        select_course = Select(course_dropdown)

          # select by index :)
        logger.info(f"Selected course at index {i}: {select_course.options[i].text}")
        select_course.select_by_index(i)

        time.sleep(7)
        # Time to write a function to download assignments -_-
        # fetch_assignment_data(driver, select_course.options[i].text)

      except Exception as e:
        logger.warning(f"Stale element encountered at index {i}. Retrying... Error: {e}")
        time.sleep(2)
        continue
  except Exception as e:
    logger.error(f"Error in processing courses: {e}")

def get_assignments(driver):
    # First, navigate to the assignments page
    if not navigate_to_assignments(driver):
        logger.error("Failed to navigate to the assignments page. Exiting.")
        return

    # Process each course
    process_courses(driver)

# Driver Program
if __name__ == "__main__":
  driver = webdriver.Chrome()
  enrollment = os.getenv("LMS_ENROLLMENT")
  password = os.getenv("LMS_PASSWORD")
  branch = "Lahore Campus"
  role = "Student"
  lms_name = "Go To LMS"
  try:
      login_cms(driver, enrollment, password, branch, role)
      go_to_lms(lms_name)
      get_assignments(driver)
  except Exception as e:
    logger.error(f"An error occurred: {e}")
  finally:
    driver.quit()