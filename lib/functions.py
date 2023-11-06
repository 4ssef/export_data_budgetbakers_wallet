'''
==========================================================================

Este módulo contiene todas las funciones necesarias para el funcionamiento
del archivo principal 'export_data_wallet.py

==========================================================================

'''

from selenium import webdriver as webdriver
from selenium.webdriver.common.by import By
from datetime import datetime

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
# Definición clase Record para las transacciones.
# ===============================================
class Record:
    def __init__(self, date, type, category, account, description, label, amount):
        self.date = date
        self.type = type
        self.category = category
        self.account = account
        self.description = description
        self.label = label
        self.amount = amount

# ===============================================
# Retorna lista de fechas de las transacciones.
# ===============================================
def get_dates(driver):
    selector = '.MhNEgOnlVNRo3U-Ti1ZHP' # CSS selector de las fechas en Wallet
    return [date.text for date in driver.find_elements(By.CSS_SELECTOR, selector)]

# ===============================================
# Agrega el año en caso de ser el actual y
# retorna la fecha en objeto datetime.
# ===============================================
def clean_date(date_str: str):
    date_format = '%B %d, %Y'
    
    # si los últimos 4 caracteres no son digitos,
    # retorna agrega el año actual
    if date_str[-4:].isdigit():
        return datetime.strptime(date_str, date_format)
    else:
        return datetime.strptime(date_str + f', {ACTUAL_YEAR}', date_format)