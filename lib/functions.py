'''
==========================================================================

Este módulo contiene todas las funciones necesarias para el funcionamiento
del archivo principal 'export_data_wallet.py

==========================================================================

'''

from selenium import webdriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from datetime import datetime, timedelta

# ===============================================
# Variables globales
# ===============================================

ACTUAL_YEAR = datetime.now().year
ACCOUNTS_SELECTOR = '#root > div > div > main > div > div._5NFnhpp7joa9CQoFA2Fw- > div._14RWKiNFwtHCO_ubRsTZ57 > div:nth-child(3) > div > div:nth-child(4)' # CSS selector de las cuentas
DATES_SELECTOR = '.MhNEgOnlVNRo3U-Ti1ZHP' # CSS selector de las fechas
DATES_XPATH = '/html/body/div/div/div/main/div/div[2]/div[2]/div' # full xpath de cada sección de los parent div de fechas
CLASSES_SELECTORS = {
    'category': '._1Q3dkM4Dh6bjIxICrBMsvZ',
    'account': '.haztXbqN9W6_Sa8X7ZjHh',
    'desc': '.qcICMAjXBzU_8kvhCu6Ir',
    'labels': '._2yWsrOsWf0KGrXIxhhDI2I > ._3qB8ZxU3QZU1r0vgpc39K_',
    'amount': '.zh61r2aVULGpP5-PnSAHX > ._2incM6fyIxbGkeydtYoltF',
    }

# ===============================================
# Retorna la lista de las cuentas del usuario.
# ===============================================
def get_accounts(driver):
    return [i.text for i in driver.find_elements(By.CSS_SELECTOR, ACCOUNTS_SELECTOR)][0].split('\n')[3:]

# ===============================================
# Retorna una lista donde cada elemento es el 
# campo correspondiente para la transacción dada
# en el argumento.
# ===============================================
def get_records(record: WebElement, driver):
    lista = []
    
    for selector in CLASSES_SELECTORS.values(): # itera sobre las clases
        # ===============================================
        # children es una lista de elementos dentro de 
        # los valores de CLASSES_SELECTORS.
        # ===============================================
        children = record.find_elements(By.CSS_SELECTOR, selector)
        
        # si no encuentra elementos para algún selector de CLASSES_SELECTOR,
        # quiere decir que ese campo está vacío, por lo que concatena 'None'
        if len(children) == 0:
            lista.append(None)
        else:
            for child in children:
                lista.append(child.text.replace('\n', ','))
    return lista

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

# ===============================================
# Retorna el monto limpio como float()
# ===============================================
def clean_amount(str_amount: str):
    return float(str_amount.replace('$', '').replace('MX', '').replace(',', ''))