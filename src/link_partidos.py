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

CANTIDAD_FECHAS = 38

options = Options()
# options.add_experimental_option("detach", True)
# options.add_argument("--headless")

service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=options)

url = "https://www.sofascore.com/tournament/football/chile/primera-division/11653#id:2577"

driver.get(url)

sleep(2)
try:
    matches = driver.find_element(By.CSS_SELECTOR, 'h2.sc-jXbUNg.gaxyfA.primary.full-width[data-tabid="matches"]')
    matches.click()
except Exception as e:
    print("No se encontraron los partidos")
    print(e)

sleep(1)
try:
    per_rounds = driver.find_element(By.CSS_SELECTOR, 'div.sc-fqkvVR.LYUxR.sc-jXbUNg.edbelf[data-tabid="2"]')
    per_rounds.click()
except Exception as e:
    print("No se encontraron las rondas")
    print(e)
sleep(1)

try:
    anterior = driver.find_element(By.CSS_SELECTOR, 'button.sc-aXZVg.dbpbvb')

    # Open links.txt file for writing
    with open('links.txt', 'a') as file:
        for i in range(CANTIDAD_FECHAS):
            
            # if i == 0:
            #     for i in range(5):
            #         sleep(1)
            #         anterior.click()

            try:
                contenedor = driver.find_element(By.CSS_SELECTOR, "div.sc-fqkvVR.fChHZS")

                a_elements = contenedor.find_elements(By.TAG_NAME, "a")
                print(f"Fecha {CANTIDAD_FECHAS - i}: ", len(a_elements))
                for a_element in a_elements:

                    # Visita el enlace
                    link = a_element.get_attribute('href')
                    # print(link)

                    if link != "https://www.sofascore.com/tournament/football/chile/primera-division/11653":
                        # Write link to file
                        file.write(link + '\n')

                sleep(1)
                anterior.click()
                sleep(1)

            except Exception as e:
                print("No se encontraron los elementos")
                print(e)

except Exception as e:
    print("No se encontro el botón anterior")
    print(e)
