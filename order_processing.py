from pathlib import Path
import main
import order
import customer_management
import printer
            

class ordercache:
    _order_cache = set()
    
    def __init__(self):
        _prep_order_list = []
        _path = Path("./Datenbanken/order.csv")
        _order_csv_exists = _path.exists()
        if _order_csv_exists:
            try:
                with open(_path, "r") as _orderdb:
                    lines = _orderdb.readlines()
                    lines.pop(0)
                    for line in lines:
                        _prep_order_list.append(line.strip("\n"))

                    for _listed_order in _prep_order_list:
                        _prep_order = str.split(_listed_order, sep=";")
                        _order_id_exists = order.order.order_id_set.__contains__(int(_prep_order[0]))
                        _order = order.order(_prep_order[1],_prep_order[3],_prep_order[0],_prep_order[2])
                        if not _order_id_exists:
                            self._order_cache.add(_order)
                        else:
                            raise OrderIDException(str(_order), "Order ID ist bereits vergeben!")

            except OrderIDException as exc:
                print(f"Caught OrderIDException with custom_kwarg={exc.custom_kwarg}")
            
    
    def find_order(self, customer = ""):
        _customer = ""
        if customer != "": _customer = customer
        
        for _order in self._order_cache:
            assert type(_order) == order.order
            
            if (_order._customer == _customer):
                print(_order)
                
                
    def add_order_to_cache(self, order: order.order):
        self._order_cache.add(order)
        
    def remove_order_from_cache(self, order: order.order):
        self._order_cache.pop(order)
        
    def update_cached_order(self, old: order.order, new: order.order):
        self._order_cache.pop(old)
        self._order_cache.add(new)
        
    def print_order_db(self):
        _order_tuple = tuple(self._order_cache)
        _order_list = sorted(_order_tuple, key=lambda order: order.order_id)
        for _order in _order_list:
            print(_order)
            
    def __iter__(self):
        for _order in self._order_cache:
            return _order
        
    def __str__(self):
        return f"        {self._order_cache}"
            
            
class OrderDBException(Exception):
    "A base class for OderDBExceptions"
    
    
class OrderIDException(OrderDBException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.custom_kwarg = kwargs.get('custom_kwarg')


class itemcache:
    _item_cache = set()
    
    def __init__(self):
        _prep_item_list = []
        _path = Path("./Datenbanken/items.csv")
        _item_csv_exists = _path.exists()
        if _item_csv_exists:
            try:
                with open(_path, "r") as _itemdb:
                    lines = _itemdb.readlines()
                    lines.pop(0)
                    for line in lines:
                        _prep_item_list.append(line.strip("\n"))

                    for _listed_item in _prep_item_list:
                        _prep_item = str.split(_listed_item, sep=";")
                        _item_number_exists = order.item.item_number_set.__contains__(int(_prep_item[0]))
                        _item = order.item(_prep_item[1], _prep_item[2], _prep_item[0])
                        if not _item_number_exists:
                            self._item_cache.add(_item)
                        else:
                            raise ItemNumberException(str(_item), "Itemnummer is bereits vergeben!")

            except ItemNumberException as exc:
                print(f"Caught ItemNumberException with custom_kwarg={exc.custom_kwarg}")
            
    
    def find_item_number(self, item_name = ""):
        _item_name = ""
        if item_name == "": _item_name = item_name
        
        for _item in self._item_cache:
            assert type(_item) == order.item
            
            if _item._item_name == _item_name:
                print(_item)
                
            return _item.item_number
        
    
    def get_item(self, item_number: str):
        try:
            _found = False
            _hit = None
            for _item in self._item_cache:
                assert type(_item) == order.item
                if item_number == _item.item_number:
                    _hit = _item.item_number
                    _found = True

            if _found == True:
                return _hit
            else: raise ItemNotFoundException
        except ItemNotFoundException as exc:
            print(f"Caught ItemNotFoundException with custom_kwarg={exc.custom_kwarg}")
            

    def add_item_to_cache(self, item: order.item):
        self._item_cache.add(item)
        
    
    def remove_item_from_cache(self, item: order.item):
        self._item_cache.pop(item)
        
    
    def update_cached_item(self, old: order.item, new: order.item):
        self._item_cache.pop(old)
        self._item_cache.add(new)
        
        
    def print_item_db(self):
        _item_tuple = tuple(self._item_cache)
        _item_list = sorted(_item_tuple, key=lambda item: item.item_number)
        for _item in _item_list:
            print(_item)
            
            
    def __iter__(self):
        for _item in self._item_cache:
            return _item
        
        
    def __str__(self):
        return f"        {self._item_cache}"
            
            
class ItemNumberException(OrderDBException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.custom_kwarg = kwargs.get('custom_kwarg')


class ItemNotFoundException(OrderDBException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.custom_kwarg = kwargs.get('custom_kwarg')



def order_processing_menu_loop(customer_cache: customer_management.customercache, order_cache: ordercache, item_cache: itemcache):
    _menu_string = """
        ##########################################################################################################
        Auftragsbearbeitung
        Menü:
        1. Auftrag anlegen
        2. Auftrag bearbeiten
        3. Auftrag löschen
        4. Aufträge ausgeben
        5. Warenverwaltung
        6. Zurück zum Hauptmenü
        ##########################################################################################################
    """

    printer.Printer.clear_cli()

    while True:
        print(_menu_string)

        _menu_item = input("        Bitte wählen sie den gewünschten Menüpunkt:\n")

        if _menu_item == "1":
            _customer_string = input("        Customer name:\n")
            _customer_id = customer_cache.find_customer_id(company=_customer_string)

            _item_strings = []
            while True:
                item_name_or_number = input("        Itemname oder -nummer:\n")
                if item_name_or_number != "":
                    _item_strings.append(item_name_or_number)
                else: break
                
            _items = []
            
            for _item_string in _item_strings:
                _item_number = item_cache.find_item_number(_item_string)
                _items.append(item_cache.get_item(_item_number))
                
            print(f"Items: {_items}")
            
            _total = float(input("        Total:\n"))
            
            _order = order.order(customer_cache.get_customer(_customer_id), _total, _items)
            _order.save_order_to_csv()
            order_cache.add_order_to_cache(_order)
            
        if _menu_item == "2":
            _item_number = input("        Bitte geben sie die Itemnummer des zu bearbeitenden Items ein!\n")
            _new_items_string = []
            while True:
                item_name_or_number = input("        Itemname oder -nummer:\n")
                if item_name_or_number != "":
                    _new_items_string.append(item_name_or_number)
                else: break
            
            _items = []
            
            for _item_string in _new_items_string:
                _item_number = order.item.find_item(_item_string)
                _items.append(item_cache.get_item(_item_number))

            _new_total = input("        Neues Total:\n")

            _new_order = order.order(items=_items, total=float(_new_total))
            order_cache.update_cached_order(order_cache.get_order(_item_number), _new_order)
            
        if _menu_item == "3":
            _item_number = input("        Bitte geben sie die Auftragsnummer des zu löschenden Auftrags ein:\n")
            order_cache.remove_order_from_cache(order_cache.get_order(_item_number))
            
        if _menu_item == "4":
            order_cache.print_order_db()
            
        if _menu_item == "5":
            item_management_menu_loop(item_cache=item_cache)

        if _menu_item == "6":
            main.main_menu_loop()
        else:
            print("        Ungültige Eingabe, bitte versuchen Sie es erneut!")
            
            
def item_management_menu_loop(item_cache: itemcache):
    _menu_string = """
        ##########################################################################################################
        Auftragsbearbeitung
        Menü:
        1. Ware anlegen
        2. Ware bearbeiten
        3. Ware löschen
        4. Warenliste ausgeben
        5. Zurück zum Hauptmenü
        ##########################################################################################################
    """

    printer.Printer.clear_cli()
    
    while True:
        print(_menu_string)
        
        _menu_item = input("        Bitte wählen Sie den gewünschten Menüpunkt:\n")
        
        if _menu_item == "1":
            _name = input("        Bitte geben sie den Namen der Ware ein:\n")
            _unit_price = input("        Bitte geben sie den Stückpreis der Ware ein:\n")

            _item = order.item(item_name=_name, unit_price=_unit_price)
            _item.save_item_to_csv()
            item_cache.add_item_to_cache(_item)

        if _menu_item == "2":
            # TODO: implement
            print("da")
            
        if _menu_item == "3":
            # TODO: implement
            print("dub")
            
        if _menu_item == "4":
            item_cache.print_item_db()
            
        if _menu_item == "5":
            main.main_menu_loop()
        else: print("        Ungültige Eingabe, bitte versuchen sie es erneut!")
   
