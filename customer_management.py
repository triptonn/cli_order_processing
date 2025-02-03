from pathlib import Path
import os

import main
import customer
import printer

            
            
class customercache:
    _customer_cache = set()
    
    def __init__(self):
        _prep_customer_list = []
        _path = Path("./Datenbanken/kunden.csv")
        _customer_csv_exists = _path.exists()
        if _customer_csv_exists:
            try:
                with open(_path, "r") as _customerdb:
                    lines = _customerdb.readlines()
                    lines.pop(0)
                    for line in lines:
                        _prep_customer_list.append(line.strip("\n"))

                    for _listed_customer in _prep_customer_list:
                        _prep_customer = str.split(_listed_customer, sep=";")
                        _customer_id_exists = customer.Customer.customer_id_set.__contains__(int(_prep_customer[0]))
                        _customer = customer.Customer(_prep_customer[1],_prep_customer[2],_prep_customer[3],_prep_customer[4],_prep_customer[5],_prep_customer[6],_prep_customer[7],_prep_customer[0])
                        if not _customer_id_exists:
                            self._customer_cache.add(_customer)
                        else:
                            raise CustomerIDExcpetion(str(_customer), "Kunden ID wird bereits vergeben!")

            except CustomerIDExcpetion as exc:
                print(f"Caught CustomerIDException with custom_kwarg={exc.custom_kwarg}")

    def find_customer_id(self, lastname = "", name = "", company = ""):
        _lastname = ""
        _name = ""
        _company = ""

        if lastname != "": _lastname = lastname
        if name != "": _name = name
        if company != "": _company = company
        
        for _customer in self._customer_cache:
            assert type(_customer) == customer.Customer
            
            if (_customer.lastname == _lastname or _customer.name == _name) and _customer.company == _company:
                print(_customer)
                
            return _customer.customer_id
                    

    def get_customer(self, customer_id: str):
        try:
            _found = False
            _hit = None
            for _customer in self._customer_cache:
                assert type(_customer) == customer.Customer
                if customer_id == _customer.customer_id:
                    _hit = _customer.customer_id
                    _found = True
                                        

            if _found == True:
                
                return _hit
            else: raise CustomerNotFoundException
        except CustomerNotFoundException as exc:
            print(f"Caught CustomerNotFoundException with custom_kwarg={exc.custom_kwarg}")


    def add_customer_to_cache(self, customer: customer.Customer):
        self._customer_cache.add(customer)
        

    def remove_customer_from_cache(self, customer: customer.Customer):
        self._customer_cache.pop(customer)


    def update_cached_customer(self, old: customer.Customer, new: customer.Customer):
        self._customer_cache.pop(old)
        self._customer_cache.add(new)
                 

    def print_customer_db(self):
        _customer_tuple = tuple(self._customer_cache)
        _customer_list = sorted(_customer_tuple, key=lambda customer: customer.customer_id) 
        for _customer in _customer_list:
            print(_customer) 
    

    def __iter__(self):
        for _customer in self._customer_cache:
            return _customer
    

    def __str__(self):
        return f"{self._customer_cache}"
    

class CustomerDBException(Exception):
    "A base class for CustomerDBExceptions"
    

class CustomerIDExcpetion(CustomerDBException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.custom_kwarg = kwargs.get('custom_kwarg')
        
class CustomerNotFoundException(CustomerDBException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.custom_kwarg = kwargs.get('custom_kwarg')




def customer_management_loop(customer_cache: customercache):
    _customer_cache = customer_cache

    _menu_string = """
        #########################################################################################################
        Kundendatenbank
        Menü:
        1. Neuen Kunden anlegen
        2. Kunden bearbeiten
        3. Kunden löschen
        4. Kundenliste ausgeben
        5. Kundennummer finden
        6. Zurück zum Hauptmenü
        ##########################################################################################################
    """

    printer.Printer.clear_cli()

    while True:
        print(_menu_string)
        
        _menu_items = input("        Bitte wählen Sie den gewünschen Menüpunkt:\n")
        
        if _menu_items == "1":
            _name = input("        Nachname:\n")
            _lastname = input("        Vorname:\n")
            _company = input("        Firmenname:\n")
            _street = input("        Straße:\n")
            _house_number = input("        Hausnummer:\n")
            _postcode = input("        Postleitzahl:\n")
            _city = input("        Ort:\n")
            
            _customer = customer.Customer(_name, _lastname, _company, _street, _house_number, _postcode, _city)
            _customer.save_customer_to_csv()
            _customer_cache.add_customer_to_cache(_customer)


        if _menu_items == "2":
            # TODO: implement
            _customer_id = input("        Bitte geben sie die Kundenummer des zu bearbeitenden Kunden ein:\n")
            _customer_cache.update_cached_customer()
            
        if _menu_items == "3":

            # TODO: implement
            _customer_id = input("        Bitte geben sie die Kundennummer des zu löschenden Kunden ein:\n")
            
        if _menu_items == "4":
            _customer_cache.print_customer_db()

        if _menu_items == "5":
            _company = input("        Bitte geben sie den vollständigen Firmennamen ein:\n")
            _name = input("        Bitte geben sie den Nachnamen des Kundenkontakts ein:\n")
            _lastname = input("        Bitte geben sie den Vornamen des Kundenkontakts ein:\n")
            _customer_cache.find_customer_id(name=_name, vorname=_lastname, firma=_company)
           
        if _menu_items == "6":
            main.main_menu_loop()
        else:
            print("        Ungültige Eingabe, bitte versuchen Sie es erneut!")
