from pathlib import Path
import copy
import order
import customer_management
            

class ItemCache:
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
                        _item_number_exists = order.Item.item_number_set.__contains__(int(_prep_item[0]))
                        _item = order.Item(_prep_item[1], float(_prep_item[2]), int(_prep_item[0]))
                        if not _item_number_exists:
                            self._item_cache.add(_item)
                        else:
                            raise ItemNumberException(str(_item), "Itemnummer is bereits vergeben!")

            except ItemNumberException as exc:
                print(f"Caught ItemNumberException with custom_kwarg={exc.custom_kwarg}")
            except ValueError as exc:
                print(f"Caugh ValueError while initializing item cache: {exc.args}")
            
    
    def find_item_number(self, item_name: str):
        if item_name == "":
            return None
        
        for item in self._item_cache:
            assert type(item) is order.Item
            if item.item_name == item_name:
                return item.item_number

    def get_item(self, item_number: int):
        if item_number == None:
            return None

        try:
            for item in self._item_cache:
                assert type(item) == order.Item
                if item.item_number == item_number:
                    return copy.copy(item)

            raise ItemNotFoundException(f"Item with number {item_number} not found")

        except ItemNotFoundException as exc:
            print(f"Caught ItemNotFoundException: Item {item_number} not found")
        except Exception as err:
            print(f"Unexpected Error while getting item: {err}")

        return None


    def add_item_to_cache(self, item: order.Item):
        self._item_cache.add(item)
        
    
    def remove_item_from_cache(self, item: order.Item):
        self._item_cache.pop(item)
        
    
    def update_cached_item(self, old: order.Item, new: order.Item):
        self._item_cache.pop(old)
        self._item_cache.add(new)
        
        
    def print_item_db(self):
        print(f"DEBUG: {self._item_cache}")
        _item_tuple = tuple(self._item_cache)
        _item_list = sorted(_item_tuple, key=lambda item: item.item_number)
        for _item in _item_list:
            print(_item)
            
            
    def __iter__(self):
        for _item in self._item_cache:
            return _item
        
        
    def __str__(self):
        return f"        {self._item_cache}"






class OrderCache:
    _order_cache = set()
    
    def __init__(self, item_cache: ItemCache, customer_cache: customer_management.CustomerCache):
        _prep_order_str_list = []
        _path = Path("./Datenbanken/orders.csv")
        _order_csv_exists = _path.exists()
        if _order_csv_exists:
            try:
                with open(_path, "r") as _orderdb:
                    lines = _orderdb.readlines()
                    lines.pop(0)
                    for line in lines:
                        _prep_order_str_list.append(line.strip("\n"))

                    for _listed_order in _prep_order_str_list:
                        _order_positions = []
                        _order_position_values = []
                        _prep_order = str.split(_listed_order, sep=";")
                        _order_id_exists = order.Order.order_id_set.__contains__(int(_prep_order[0]))

                        _order_state = None
                        match _prep_order[2]:
                            case "Offen":
                                _order_state = order.OrderState.OPENED
                            case "Pausiert":
                                _order_state = order.OrderState.HALT
                            case "InArbeit":
                                _order_state = order.OrderState.WIP
                            case "Versand":
                                _order_state = order.OrderState.DONE
                            case "Bezahlt":
                                _order_state = order.OrderState.PAYED
                            case "Geschlossen":
                                _order_state = order.OrderState.CLOSED
                            case _:
                                pass

                        _prep_positions = str.split(_prep_order[3], sep="},{")
                        _prep_positions_index_zero_correct = str.split(_prep_positions[0], sep="[{")
                        _index_zero_correction = _prep_positions_index_zero_correct[1] # first position
                        _first_position_values = tuple(str.split(_index_zero_correction, sep=","))

                        _order_position_values.append(_first_position_values)

                        _middle_indices = _prep_positions[1:len(_prep_positions) - 1]
                        
                        for pos in _middle_indices:
                            _pos = tuple(str.split(str.strip(pos, "'"), sep=","))
                            _order_position_values.append(_pos)
                        
                        _prep_positions_last_index_correction = str.split(_prep_positions[len(_prep_positions) - 1], sep="}")
                        _last_index_correction = str.strip(_prep_positions_last_index_correction[0], "'")
                        _last_position_values = tuple(str.split(_last_index_correction, sep=","))

                        _order_position_values.append(_last_position_values)

                        for pos in _order_position_values:
                            _position = order.Position(item_cache.get_item(int(pos[0])), int(pos[1]))
                            _order_positions.append(_position)

                        _order = order.Order(customer_cache.get_customer(int(_prep_order[1])),order.Positions(_order_positions),_prep_order[0],_order_state)

                        if not _order_id_exists:
                            self._order_cache.add(_order)
                        else:
                            raise OrderIDException(str(_order), "Order ID ist bereits vergeben!")

            except OrderIDException as exc:
                print(f"Caught OrderIDException with custom_kwarg={exc.custom_kwarg}")
            except AssertionError as err:
                print(f"Caught AssertionError during order cache initialization: {err, err.with_traceback()}")
            except Exception as exc:
                print(f"Unknown Exception caught during order cache initialization: {exc, exc.with_traceback()}")
                
    
    def find_order(self, customer = ""):
        _customer = ""
        if customer != "": _customer = customer
        
        for _order in self._order_cache:
            assert type(_order) == order.Order
            
            if (_order._customer == _customer):
                print(_order)
                
                
    def add_order_to_cache(self, order: order.Order):
        self._order_cache.add(order)
        
    def remove_order_from_cache(self, order: order.Order):
        self._order_cache.pop(order)
        
    def update_cached_order(self, old: order.Order, new: order.Order):
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
    
class ItemNumberException(OrderDBException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.custom_kwarg = kwargs.get('custom_kwarg')


class ItemNotFoundException(OrderDBException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.custom_kwarg = kwargs.get('custom_kwarg')
            
    
    
class OrderIDException(OrderDBException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.custom_kwarg = kwargs.get('custom_kwarg')
            
        
        


def order_processing_menu_loop(customer_cache: customer_management.CustomerCache, order_cache: OrderCache, item_cache: ItemCache):
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
    #printer.Printer.clear_cli()
    _order_processing = True
    while _order_processing == True:
        print(_menu_string)
        _menu_item = input("        Bitte wählen sie den gewünschten Menüpunkt:")

        if _menu_item == "1":
            _customer_string = input("        Kundenname:")
            _customer_id = customer_cache.find_customer_id(company=_customer_string)
            _customer = customer_cache.get_customer(_customer_id)
            if _customer == None:
                continue

            _adding_positions = True
            _position_value_str_int = []
            _positions = []

            while _adding_positions:
                _count = None
                _position_valid = True

                _item_name_or_number_str = input("        Itemname oder -nummer ('fertig' um die Eingabe von Positionen zu beenden):")
                if _item_name_or_number_str == "fertig":
                    print("        Keine weiteren Items.")
                    break

                _count_str = input("        Stück:")
                try:
                    _count = int(_count_str)
                except ValueError as exc:
                    exc.add_note("        Die eingegebene Stückzahl ist ungültig!")
                    print(exc, exc.__notes__)
                    continue
                
                if _item_name_or_number_str != "" and _position_valid:
                    _position_value_str_int.append([_item_name_or_number_str, _count])
                else:
                    print("        Position lässt sich aus den Angaben nicht erzeugen!")
                    continue

            for _position_value in _position_value_str_int:
                try:
                    item_number = int(_position_value[0])
                    item = item_cache.get_item(item_number)
                except ValueError:
                    item_name = _position_value[0]
                    item_number = item_cache.find_item_number(item_name)
                    item = item_cache.get_item(item_number)
                    
                if item is not None:
                    position = order.Position(item, _position_value[1])
                    _positions.append(position)
                else:
                    print(f"        Warnung: Item '{_position_value[0]}' nicht gefunden")
                    
            if _positions:
                if _customer:
                    _order = order.Order(
                        customer=_customer,
                        positions=order.Positions(_positions)
                    )
                    _order.save_order_to_csv()
                    order_cache.add_order_to_cache(_order)
                    print("        Auftrag erfolgreich erstellt")
                else:
                    print("        Fehler: Kunde nicht gefunden")
            else:
                print("        Fehler: Keine gültigen Positionen eingegeben")

        elif _menu_item == "2":
            _local_item_number = input("        Bitte geben sie die Auftragsnummer des zu bearbeitenden Auftrags ein!\n")
            _new_items_string = []
            while True:
                _item_name_or_number_str = input("        Itemname oder -nummer ('fertig' um die Eingabe von Positionen zu beenden):\n")
                _count_str = input("        Stückzahl:\n")
                if _item_name_or_number_str != "":
                    _new_items_string.append(_item_name_or_number_str)
                else: break
            _positions = []
            for _item_string in _new_items_string:
                _local_item_number = order.Item.find_item(_item_string)
                _positions.append(item_cache.get_item(_local_item_number))
            _new_total = input("        Neues Total:\n")
            _new_order = order.Order(positions=_positions, total=float(_new_total))
            order_cache.update_cached_order(order_cache.get_order(_local_item_number), _new_order)
        elif _menu_item == "3":
            _local_item_number = input("        Bitte geben sie die Auftragsnummer des zu löschenden Auftrags ein:\n")
            order_cache.remove_order_from_cache(order_cache.get_order(_local_item_number))
        elif _menu_item == "4":
            order_cache.print_order_db()
        elif _menu_item == "5":
            item_management_menu_loop(item_cache=item_cache)
        elif _menu_item == "6":
            _order_processing = False
        else:
            print("        Ungültige Eingabe, bitte versuchen Sie es erneut!")
            
            
def item_management_menu_loop(item_cache: ItemCache):
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
    #printer.Printer.clear_cli()
    _item_management = True
    while _item_management == True:
        print(_menu_string)
        _menu_item = input("        Bitte wählen Sie den gewünschten Menüpunkt:\n")
        if _menu_item == "1":
            _name = input("        Bitte geben sie den Namen der Ware ein:\n")
            _unit_price = input("        Bitte geben sie den Stückpreis der Ware ein:\n")
            _item = order.Item(item_name=_name, unit_price=_unit_price)
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
            _item_management = False
        else: print("        Ungültige Eingabe, bitte versuchen sie es erneut!")
