from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Edge()
driver.get("https://project-locomate.netlify.app")

try:
    element = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "element_id"))
    )
    # Interagissez avec l'élément ici
finally:
    driver.quit()
