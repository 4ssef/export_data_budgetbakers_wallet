'''
==========================================================================

Este módulo contiene todas las funciones necesarias para el funcionamiento
del archivo principal 'export_data_wallet.py

==========================================================================

'''

from selenium import webdriver as webdriver
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta

ACTUAL_YEAR = datetime.now().year

# ===============================================
# Retorna la lista de las cuentas del usuario.
# ===============================================
def get_accounts(driver):
    selector = '#root > div > div > main > div > div._5NFnhpp7joa9CQoFA2Fw- > div._14RWKiNFwtHCO_ubRsTZ57 > div:nth-child(3) > div > div:nth-child(4)'
    return [i.text for i in driver.find_elements(By.CSS_SELECTOR, selector)][0].split('\n')[3:]

# ===============================================
# Retorna una lista de listas donde estas últimas
# son las transacciones (records).
# ===============================================
def get_records(driver):
    selector = '._3wwqabSSUyshePYhPywONa' # CSS selector de las transacciones
    return [record.text.split('\n') for record in driver.find_elements(By.CSS_SELECTOR, selector)]

# ===============================================
# Retorna lista de fechas de las transacciones.
# ===============================================
def get_dates(driver):
    selector = '.MhNEgOnlVNRo3U-Ti1ZHP' # CSS selector de las fechas en Wallet
    return [date.text for date in driver.find_elements(By.CSS_SELECTOR, selector)]

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
    xpath = '/html/body/div/div/div/main/div/div[2]/div[2]/div'
    for i in range(len(dates)): # itera sobre las fechas
        parent_div = driver.find_element(By.XPATH, f'{xpath}/div[{i+2}]') # divs de divisiones por fecha
        child_divs = len(parent_div.find_elements(By.XPATH, './div')) - 1 # cantidad de divs adentro de cada bloque
        data.append((i, child_divs)) # agrega a la lista el tuple (posición fecha, cantidad de elementos dentro)
    return data