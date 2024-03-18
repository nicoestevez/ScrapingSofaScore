from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
WAIT_TIME = 10


def wait_visible(driver, by, value, time: float = WAIT_TIME):
    return WebDriverWait(driver, time).until(EC.visibility_of_element_located((by, value)))


def wait_clickable(driver, by, value, time: float = WAIT_TIME):
    return WebDriverWait(driver, time).until(EC.element_to_be_clickable((by, value)))


def wait_invinsible(driver, by, value, time=WAIT_TIME):
    return WebDriverWait(driver, time).until(EC.invisibility_of_element_located((by, value)))


def wait_presence(driver, by, value, time=WAIT_TIME):
    return WebDriverWait(driver, time).until(EC.presence_of_element_located((by, value)))


def wait_visible_all(driver, by, value, time=WAIT_TIME):
    return WebDriverWait(driver, time).until(EC.visibility_of_all_elements_located((by, value)))
