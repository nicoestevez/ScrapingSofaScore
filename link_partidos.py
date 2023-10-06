import os
import csv
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

options = Options()
# options.add_experimental_option("detach", True)
# options.add_argument("--headless")

service = Service(executable_path='/usr/bin/chromedriver')

driver = webdriver.Chrome(service=service, options=options)

url = "https://www.sofascore.com/tournament/football/chile/primera-division/11653"

driver.get(url)

sleep(2)
try:
    matches = driver.find_element(By.XPATH, '//h2[@data-tabid="matches"]')
    matches.click()
except Exception as e:
    print("No se encontraron los partidos")
    print(e)

sleep(1)
try:
    per_rounds = driver.find_element(By.XPATH, '//div[@data-tabid="2"][@d="inline-block"][@class="sc-hLBbgP bJbFuC sc-pyfCe gjBXhT secondary "]')
    per_rounds.click()
except Exception as e:
    print("No se encontraron las rondas")
    print(e)
sleep(1)

try:
    anterior = driver.find_element(By.CLASS_NAME, 'gvEXzS')

    # Open links.txt file for writing
    with open('links.txt', 'w') as file:
        for i in range(18):
            sleep(1)
            anterior.click()
            sleep(1)

            try:
                contenedor = driver.find_element(By.CSS_SELECTOR, "div.sc-hLBbgP.sYIUR > div.list-wrapper > div.sc-hLBbgP.hBOvkB")

                a_elements = contenedor.find_elements(By.TAG_NAME, "a")
                for a_element in a_elements:

                    # Visita el enlace
                    link = a_element.get_attribute('href')
                    print(link)

                    if link != url:
                        # Write link to file
                        file.write(link + '\n')

            except Exception as e:
                print("No se encontraron los elementos")
                print(e)

except Exception as e:
    print("No se encontro el botón anterior")
    print(e)
