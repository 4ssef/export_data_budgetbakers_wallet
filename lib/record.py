'''
==========================================================================

En este módulo se encuentra la definición de la clase Record para manipular
cada registro como un objeto.

==========================================================================

'''

# ===============================================
# Definición clase Record para las transacciones.
# ===============================================
class Record:
    def __init__(self, date, type, category, account, description, label, currency, amount):
        self.date = date
        self.type = type
        self.category = category
        self.account = account
        self.description = description
        self.label = label
        self.currency = currency
        self.amount = amount