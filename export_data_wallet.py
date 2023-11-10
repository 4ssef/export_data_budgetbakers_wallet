import os
import lib.functions as f
from lib.record import Record
from selenium import webdriver as webdriver
from selenium.webdriver.common.by import By
from pathlib import Path
from dotenv import load_dotenv
from time import sleep
from pprint import pprint

load_dotenv()

# ===============================================
# Varibales de ruta de acceso.
# ===============================================

PROJECT_PATH = Path(__file__).resolve().parent

# ===============================================
# Variables globales.
# ===============================================

URL = 'https://web.budgetbakers.com/records'
EMAIL = os.getenv('BUDGETBAKERS_WALLET_EMAIL')
PASSWORD = os.getenv('BUDGETBAKERS_WALLET_PASSWORD')
BASE_CSS_SELECTOR = '#root > div > div > section > div > form >'
RECORD_DATA = ['date', 'type', 'category', 'account', 'description', 'label', 'amount']

# ===============================================
# Inicializa instancia del webdriver.
# ===============================================

options = webdriver.EdgeOptions()
options.add_argument('--headless=new') # ejecuta el webdriver minimizadamente
options.add_experimental_option('prefs', {'intl.accept_languages': 'es'}) # ejecuta el driver con español como lenguaje preferido
driver = webdriver.Edge(options = options)

# ===============================================
# Prepara la página para extracción de los
# registros.
# ===============================================

driver.get(URL)
sleep(6)
driver.find_element(By.CSS_SELECTOR, f'{BASE_CSS_SELECTOR} div:nth-child(1) > div > input[type=email]').send_keys(EMAIL) # escribe el correo
driver.find_element(By.CSS_SELECTOR, f'{BASE_CSS_SELECTOR} div:nth-child(2) > div > input[type=password]').send_keys(PASSWORD) # escribe la password
driver.find_element(By.CSS_SELECTOR, f'{BASE_CSS_SELECTOR} button').click() # click en log in
sleep(6)

script = "window.scrollTo(0, document.body.scrollHeight);"

# scrollea la página hasta que no hayan fechas nuevas
while True:
    old_dates = len(f.get_dates(driver)) # cantidad de fechas originales
    driver.execute_script(script) # scroll hasta el final
    new_dates = len(f.get_dates(driver)) # cantidad de fechas después de scrollear
    
    if old_dates == new_dates:
        break

# ===============================================
# Extracción de los registros.
# ===============================================

records = f.get_records(driver) # lista de transacciones
dates = [f.clean_date(date) for date in f.get_dates(driver)] # lista de fechas limpias
tuples = f.get_tuples_list(driver, dates) # lista de tuples

# ===============================================
# Construye el objeto Record.
# ===============================================

count = 0

for t in range(len(tuples)):
    for record in records:
        # define campos de las transacciones
        date = dates[t] # fecha
        _type = None
        cat = record[0] # categoría
        acc = record[1] # cuenta principal
        desc = None
        labels = None
        amount = record[-1] # monto
        
        # condición para salir del 2do for anidado
        if count == tuples[t][1]:
            count = 0
            break
        
        transaction = Record(date, _type, cat, acc, desc, labels, amount)
        
        count += 1