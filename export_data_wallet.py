import os
import lib.functions as f
import pandas as pd
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
RECORDS_SELECTOR = '._3wwqabSSUyshePYhPywONa > ._3oJhqSCX8H5S0i6pA59f9k' # CSS selector de las transacciones
RECORDS_DATA = ['date', 'type', 'category', 'account', 'description', 'label', 'currency', 'amount']

#region WEBSCRAPING

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

web_records = driver.find_elements(By.CSS_SELECTOR, RECORDS_SELECTOR)

records = [f.get_records(record, driver) for record in web_records]
dates = [f.clean_date(date) for date in f.get_dates(driver)] # lista de fechas limpias
tuples = f.get_tuples_list(driver, dates) # lista de tuples

# ===============================================
# Finaliza instancia del webdriver y proceso 
# webscraping.
# ===============================================

driver.close()

#endregion WEBSCRAPING

# ===============================================
# Construye el objeto Record.
# ===============================================

count = 0
aux = 0 # auxiliar para ver donde quedó el 2do for
all_records = []

for t in range(len(tuples)):
    for record in range(aux, len(records)):
        # condición para salir del 2do for anidado
        if count == tuples[t][1]:
            count = 0
            break

        # define campos de las transacciones
        date = dates[t] # fecha
        cat = records[record][0] # categoría
        acc = records[record][1] # cuenta principal
        desc = records[record][2] # descripción
        labels = records[record][3] # lista de labels
        amount = records[record][4] # monto
        # asigna la moneda
        if 'MX$' in amount:
            currency = 'MXN'
        elif '$' in amount:
            currency = 'USD'
        # asigna el tipo
        if '-' in amount:
            _type = 'Expense'
        else:
            _type = 'Income'
        amount = f.clean_amount(amount)
        
        tr = Record(date, _type, cat, acc, desc, labels, currency, amount)
        
        data = {
            'date': tr.date,
            'type': tr.type,
            'category': tr.category,
            'account': tr.account,
            'description': tr.description,
            'label': tr.label,
            'currency': tr.currency,
            'amount': tr.amount
        }
        
        all_records.append(data)
        
        aux += 1
        count += 1
        
dataframe = pd.DataFrame.from_dict(all_records)
dataframe.to_excel('file_name.xlsx', index = False)