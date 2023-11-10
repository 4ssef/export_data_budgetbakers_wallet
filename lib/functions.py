'''
==========================================================================

Este módulo contiene todas las funciones necesarias para el funcionamiento
del archivo principal 'export_data_wallet.py

==========================================================================

'''

from selenium import webdriver as webdriver
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta

# ===============================================
# Variables globales
# ===============================================

ACTUAL_YEAR = datetime.now().year
ACCOUNTS_SELECTOR = '#root > div > div > main > div > div._5NFnhpp7joa9CQoFA2Fw- > div._14RWKiNFwtHCO_ubRsTZ57 > div:nth-child(3) > div > div:nth-child(4)' # CSS selector de las cuentas
RECORDS_SELECTOR = '._3wwqabSSUyshePYhPywONa' # CSS selector de las transacciones
DATES_SELECTOR = '.MhNEgOnlVNRo3U-Ti1ZHP' # CSS selector de las fechas
DATES_XPATH = '/html/body/div/div/div/main/div/div[2]/div[2]/div' # full xpath de cada sección de los parent div de fechas

# ===============================================
# Retorna la lista de las cuentas del usuario.
# ===============================================
def get_accounts(driver):
    return [i.text for i in driver.find_elements(By.CSS_SELECTOR, ACCOUNTS_SELECTOR)][0].split('\n')[3:]

# ===============================================
# Retorna una lista de listas donde estas últimas
# son las transacciones (records).
# ===============================================
def get_records(driver):
    return [record.text.split('\n') for record in driver.find_elements(By.CSS_SELECTOR, RECORDS_SELECTOR)]

# ===============================================
# Retorna lista de fechas de las transacciones.
# ===============================================
def get_dates(driver):
    return [date.text for date in driver.find_elements(By.CSS_SELECTOR, DATES_SELECTOR)]

# ===============================================
# Retorna la fecha de string en objeto datetime.
# ===============================================
def clean_date(date_str: str):
    date_format = '%B %d, %Y'
    
    if date_str == 'Today':
        return datetime.today().date()
    elif date_str == 'Yesterday':
        return (datetime.today() - timedelta(days = 1)).date()
    elif not(date_str[-4:].isdigit()):
        return datetime.strptime(date_str + f', {ACTUAL_YEAR}', date_format).date()
    else:
        return datetime.strptime(date_str, date_format).date()

# ===============================================
# Retorna la lista de tuples donde cada elemento 
# es un bloque de fecha. La estructura del tuple 
# es (posición de la fecha 0 a n, cantidad de 
# transacciones en esa fecha)
# ===============================================
def get_tuples_list(driver, dates):
    data = []
    for i in range(len(dates)): # itera sobre las fechas
        parent_div = driver.find_element(By.XPATH, f'{DATES_XPATH}/div[{i+2}]') # divs de divisiones por fecha
        child_divs = len(parent_div.find_elements(By.XPATH, './div')) - 1 # cantidad de divs adentro de cada bloque
        data.append((i, child_divs)) # agrega a la lista el tuple (posición fecha, cantidad de elementos dentro)
    return data