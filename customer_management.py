from pathlib import Path
import copy

import customer
            
            
class CustomerCache:
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
                        _customer = customer.Customer(_prep_customer[1],_prep_customer[2],_prep_customer[3],_prep_customer[4],_prep_customer[5],_prep_customer[6],_prep_customer[7],int(_prep_customer[0]))
                        if not _customer_id_exists:
                            self._customer_cache.add(_customer)
                        else:
                            raise CustomerIDExcpetion(str(_customer), "Kunden ID ist bereits vergeben!")

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
                    

    def get_customer(self, customer_id: int):
        try:
            for _customer in self._customer_cache:
                assert type(_customer) == customer.Customer
                if customer_id == _customer.customer_id:
                    return copy.copy(_customer)
            else: raise CustomerNotFoundException(f"Customer {customer_id} not found in cache!")
        except CustomerNotFoundException as exc:
            # print(f"Caught CustomerNotFoundException: {self._customer_cache},\n{exc, exc.args, exc.with_traceback()}")
            print(self._customer_cache, type(self._customer_cache))
        return None


    def add_customer_to_cache(self, customer: customer.Customer):
        self._customer_cache.add(customer)
        

    def remove_customer_from_cache(self, customer: customer.Customer):
        self._customer_cache.remove(customer)


    def update_cached_customer(self, old: customer.Customer, new: customer.Customer):
        self._customer_cache.remove(old)
        self._customer_cache.add(new)
                 

    def print_customer_db(self):
        for _customer in self._customer_cache:
            assert type(_customer) == customer.Customer
        _customer_tuple = tuple(self._customer_cache)

        _customer_list = sorted(_customer_tuple, key=lambda customer: customer._customer_id) 
        for _customer in _customer_list:
            assert type(_customer) is customer.Customer
            print(_customer.output_print())

        print("")
    

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




def customer_management_loop(customer_cache: CustomerCache):
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

    #printer.Printer.clear_cli()
    _customer_management = True
    while _customer_management == True:
        print(_menu_string)
        
        _menu_items = input("        Bitte wählen Sie den gewünschen Menüpunkt: ")
        
        if _menu_items == "1":
            _name = input("        Nachname: ")
            _lastname = input("        Vorname: ")
            _company = input("        Firmenname: ")
            _street = input("        Straße: ")
            _house_number = input("        Hausnummer: ")
            _postcode = input("        Postleitzahl: ")
            _city = input("        Ort: ")
            
            _customer = customer.Customer(_name, _lastname, _company, _street, _house_number, _postcode, _city)
            _customer.save_customer_to_csv()
            _customer_cache.add_customer_to_cache(_customer)


        elif _menu_items == "2":
            _customer_id = input("        Bitte geben sie die Kundenummer des zu bearbeitenden Kunden ein: ")

            _unmodified_customer = _customer_cache.update_cached_customer(int(_customer_id))
            
            if _unmodified_customer == None:
                pass
            else:
                assert type(_unmodified_customer) is customer.Customer
                
                _lastname = input("        Nachname: ")
                _name = input("        Vorname: ")
                _company = input("        Firmenname: ")
                _street = input("        Straße: ")
                _house_number = input("        Hausnummer: ")
                _postcode = input("        Postleitzahl: ")
                _city = input("        Ort: ")
                
                _new_customer = customer.Customer(
                    _lastname if _lastname != _unmodified_customer.lastname else _unmodified_customer.lastname,
                    _name if _name != _unmodified_customer.name else _unmodified_customer.name,
                    _company if _company != _unmodified_customer.company else _unmodified_customer.company,
                    _street if _street != _unmodified_customer._street else _unmodified_customer._street,
                    _house_number if _house_number != _unmodified_customer._house_number else _unmodified_customer._house_number,
                    _postcode if _postcode != _unmodified_customer._postcode else _unmodified_customer._postcode,
                    _city if _city != _unmodified_customer._city else _unmodified_customer._city,
                    _unmodified_customer.customer_id
                    )
                
                customer_cache.update_cached_customer(_unmodified_customer, _new_customer)
                _unmodified_customer.delete_customer_from_csv()
                _new_customer.save_customer_to_csv()
            

        elif _menu_items == "3":
            _customer_id = input("        Bitte geben sie die Kundennummer des zu löschenden Kunden ein: ")
            _customer_to_delete = customer_cache.get_customer(int(_customer_id))
            if _customer_to_delete == None:
                print(f"Zu löschender Kunde {_customer_id} konnte nicht gefunden werden!")
            else:
                assert type(_customer_to_delete) == customer.Customer
                customer_cache.remove_customer_from_cache(_customer_to_delete)
                _customer_to_delete.delete_customer_from_csv()
            
        elif _menu_items == "4":
            _customer_cache.print_customer_db()

        elif _menu_items == "5":
            _company = input("        Bitte geben sie den vollständigen Firmennamen ein: ")
            _name = input("        Bitte geben sie den Nachnamen des Kundenkontakts ein: ")
            _lastname = input("        Bitte geben sie den Vornamen des Kundenkontakts ein: ")
            _customer_id = _customer_cache.find_customer_id(name=_name, vorname=_lastname, firma=_company)

            if _customer_id == None:
                print("        Kunde konnte nicht gefudnen werden!")
            else:
                print(f"        Der gesuchte Kunde hat die Kundennummer {_customer_id}")
           
        elif _menu_items == "6":
            _customer_management = False
        else:
            print("        Ungültige Eingabe, bitte versuchen Sie es erneut!")
