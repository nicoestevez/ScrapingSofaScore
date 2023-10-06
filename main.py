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
options.add_experimental_option("detach", True)
# options.add_argument("--headless")

service = Service(executable_path='/usr/bin/chromedriver')

driver = webdriver.Chrome(service=service, options=options)

driver.get("https://www.sofascore.com/es/torneo/futbol/chile/primera-division/11653#48017")

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

    fieldnames = ["Fecha", "Local", "Visita", "Goles Local", "Goles Visita", "Estado"]

    with open('partidos.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Escribir la cabecera del archivo CSV
        writer.writeheader()

        for i in range(2):
            sleep(1)
            anterior.click()
            sleep(1)

            try:
                contenedor = driver.find_element(By.CSS_SELECTOR, "div.sc-hLBbgP.sYIUR > div.list-wrapper > div.sc-hLBbgP.hBOvkB")

                a_elements = contenedor.find_elements(By.TAG_NAME, "a")
                for a_element in a_elements:

                    info_partido = {}

                    spans = a_element.find_elements(By.XPATH, ".//span[@class='sc-bqWxrE djnTzK']")
                    for span in spans:
                        # print("Fecha:", span.text)
                        info_partido["Fecha"] = span.text

                    divs_bwUmPO = a_element.find_elements(By.XPATH, ".//div[@class='sc-bqWxrE bwUmPO']")
                    for div in divs_bwUmPO:
                        # print("Local: ", div.text)
                        info_partido["Local"] = div.text

                    divs_gfgVOU = a_element.find_elements(By.XPATH, ".//div[@class='sc-bqWxrE gfgVOU']")
                    if len(divs_gfgVOU) == 2:
                        # print("Local: ", divs_gfgVOU[1].text)
                        info_partido["Local"] = divs_gfgVOU[1].text
                        # print("Visita: ", divs_gfgVOU[0].text)
                        info_partido["Visita"] = divs_gfgVOU[0].text
                    else:
                        for div in divs_gfgVOU:
                            # print("Visita: ", div.text)
                            info_partido["Visita"] = div.text

                    spans_hVtlqB = a_element.find_elements(By.XPATH, ".//div[@class='sc-hLBbgP sc-eDvSVe ixrGKC bMwHQt sc-44b07523-2 htIhet score-box']//span[@class='sc-bqWxrE hVtlqB currentScore']")
                    for span in spans_hVtlqB:
                        # print("Goles Local: ", span.text)
                        info_partido["Goles Local"] = span.text

                    spans_UgLMb = a_element.find_elements(By.XPATH, ".//span[@class='sc-bqWxrE UgLMb currentScore']")
                    if len(spans_UgLMb) == 2:
                        # print("Goles Local: ", spans_UgLMb[1].text)
                        info_partido["Goles Local"] = spans_UgLMb[1].text
                        # print("Goles Visita: ", spans_UgLMb[0].text)
                        info_partido["Goles Visita"] = spans_UgLMb[0].text
                    else:
                        for span in spans_UgLMb:
                            # print("Goles Visita: ", span.text)
                            info_partido["Goles Visita"] = span.text

                    estados = a_element.find_elements(By.XPATH, ".//div[@class='sc-hLBbgP sc-eDvSVe dLAlmH hyKYsT sc-44b07523-2 htIhet score-box']//span[@class='sc-bqWxrE hVtlqB currentScore']")
                    for estado in estados:
                        # print("Estado: ", estado.text)
                        info_partido["Estado"] = estado.text

                    writer.writerow(info_partido)

                    # Visita el enlace
                    link = a_element.get_attribute('href')
                    print(link)


            except Exception as e:
                print("No se encontraron los elementos")
                print(e)

except Exception as e:
    print("No se encontro el botón anterior")
    print(e)
