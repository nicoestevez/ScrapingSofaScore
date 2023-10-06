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

with open('links.txt', 'r') as file:
    lineas = file.read()
    links = lineas.split("\n")
    links = list(filter(lambda x: x.strip() != '', links))

for link in links:

    driver.get(link)

    sleep(2)
    # Ir a Estadísticas
    try:
        statistics = driver.find_element(By.XPATH, "//h2[@data-tabid='statistics']")
        statistics.click()
    except Exception as e:
        print("No se encontraron las estadísticas")
        print(e)

    sleep(2)
    # Nombres equipos
    try:
        nombres = driver.find_elements(By.CSS_SELECTOR, "div.sc-fqkvVR.caoZu > span")
        local = nombres[0]
        print(local.text)
        visita = nombres[1]
        print(visita.text)
    except Exception as e:
        print("No se encontraron los nombres de los equipos")
        print(e)

    # Goles Local
    try:
        goles_local = driver.find_element(By.CSS_SELECTOR, "div.sc-fqkvVR.fNrdSX span")
        print(goles_local.text)
    except Exception as e:
        print("No se encontraron los goles del local")
        print(e)

    # Goles Visita
    try:
        goles_visita = driver.find_element(By.CSS_SELECTOR, "div.sc-fqkvVR.iNYNuv span")
        print(goles_visita.text)
    except Exception as e:
        print("No se encontraron los goles de la visita")
        print(e)

    # Stats
    try:
        stats = driver.find_elements(By.CSS_SELECTOR, "div.sc-hLBbgP.sc-eDvSVe.dSSyaL.bbcOkn")
        print("Stats: ", len(stats)) 
    except Exception as e:
        print("No se encontraron los contenedores")
        print(e)
    
    try:
        contador = 0
        for stat in stats:
            if contador == 0:
                numeros_stats_xG = stat.find_elements(By.CSS_SELECTOR, "div.sc-fqkvVR")
                xG_local = numeros_stats_xG[0].find_element(By.XPATH, ".//span")
                print("xG_local ", xG_local.text)
                label_xG = numeros_stats_xG[1].find_element(By.CSS_SELECTOR, "span.sc-jEACwC.ijsLre > div.sc-fqkvVR.sc-dcJsrY.fMzcll.fDDcoX > span")
                print("label_xG ", label_xG.text)
                xG_visita = numeros_stats_xG[3].find_element(By.XPATH, ".//span")
                print("xG_visita ", xG_visita.text)
            else:
                numeros_stats = stat.find_elements(By.CSS_SELECTOR, "div.sc-fqkvVR > span")
                for numero in numeros_stats:
                    print(numero.text)
            contador += 1
    except Exception as e:
        print("No se encontraron los stats")
        print(e)