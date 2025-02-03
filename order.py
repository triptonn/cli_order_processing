from pathlib import Path
from enum import Enum
import os
import customer

    
class Item:
    item_number_set = set()
    _item_number_counter = 0
    
    def __init__(self, item_name: str, unit_price: float, item_number: int = 0):
        if item_number == 0:
            Item._item_number_counter += 1
            self.item_number = Item._item_number_counter
            Item.item_number_set.add(Item._item_number_counter)
        else:
            _item_number = int(item_number)
            if not Item.item_number_set.__contains__(_item_number):
                Item.item_number_set.add(_item_number)
                if Item._item_number_counter < _item_number:
                    Item._item_number_counter = _item_number

            self.item_number = _item_number
            
        self.item_name = item_name
        self.unit_price = unit_price
        
    def save_item_to_csv(self):
        _items_csv = Path("./Datenbanken/items.csv")
        _exists = _items_csv.exists()

        if _exists:
            with open(_items_csv, "a") as file:
                file.write(f"{self.item_number};{self.item_name};{self.unit_price}\n")
                
        else:
            _db_directory = Path("./Datenbanken/")
            _db_directory_exists = _db_directory.exists()
            if not _db_directory_exists: os.mkdir("./Datenbanken/")

            with open(_items_csv, "w") as file:
                file.write("item_number;name;unit_price\n")
                file.write(f"{self.item_number};{self.item_name};{self.unit_price}\n")
                
    def update_item_in_csv(self, item_name = "", unit_price = ""):
        _item_name = item_name
        _unit_price = unit_price
        
        if _item_name == "": _item_name = self.item_name
        if _unit_price == "": _unit_price = self.unit_price
        
        _items_csv = Path("./Datenbanken/items.csv")
        _temp_items_csv = Path("./Datenbanken/temp_items.csv")
        _exists = _items_csv.exists()
        if _exists:
            with open(_items_csv, "r") as input_file, open(_temp_items_csv, "w") as output_file:
                lines = input_file.readlines()
                for line in lines:
                    if line.strip("\n") != f"{self.item_number};{self.item_name};{self.unit_price}\n":
                        output_file.write(line)
                    else:
                        output_file.write(f"{self.item_number};{self.item_name};{self.unit_price}\n")
            
            os.remove("./Datenbanken/items.csv")
            _temp_items_csv.rename("./Datenbanken/items.csv")
            
    def delete_item_form_csv(self):
        _items_csv = Path("./Datenbanken/items.csv")
        _temp_items_csv = Path("./Datenbanken/items_temp.csv")
        _exists = _items_csv.exists()
        if _exists:
            with open(_items_csv, "r") as input_csv_file, open(_temp_items_csv, "w") as output_csv_file:
                lines = input_csv_file.readlines()
                for line in lines:
                    if line.strip("\n") != f"{self.item_number};{self.item_name};{self.unit_price}":
                        output_csv_file.write(line)
            os.remove("./Datenbanken/items.csv")
            _temp_items_csv.rename("./Datenbanken/items.csv")
            

    def __repr__(self):
        return repr((self.item_number, self.item_name, self.unit_price))


    def __str__(self):
        return f"{self.item_number},{self.item_name},{self.unit_price}"


class Position:
    def __init__(self, item: Item, count: int):
        self.item = item
        self.count = count
        self.position_total = item.unit_price * count
    
    def __copy__(self):
        return Position(self.item, self.count)
        
    def __repr__(self):
        return repr((self.item, self.count, self.position_total))

    def __str__(self):
        return f"{self.item.item_number},{self.item.item_name},{self.count},{self.position_total}"


class Positions:
    def __init__(self, position_list: list):
        self._position_list = position_list

    def __str__(self):
        _len = len(self._position_list)
        _counter = 1
        _json_output = '{ "positions" : ['
        for position in self._position_list:
            _pos = position
            assert type(position) is Position
            if _counter < _len:
                _json_output += "{" + f"{_pos}" + "}," 
                _counter += 1
            else:
                _json_output += "{" + f"{_pos}" + "}"
                break

        _json_output += "]}"
        
        print(f"json output: {_json_output}")
        
        return _json_output

class OrderState(Enum):
    OPENED = "Offen"
    WIP = "InArbeit"
    DONE = "Versand"
    PAYED = "Bezahlt"
    HALT = "Pausiert"
    CLOSED = "Geschlossen"


class Order:
    order_id_set = set()
    _order_id_counter = 0
    total = 0.00
    _state = None 
    
    def __init__(self, customer: customer.Customer, positions: Positions, order_id: int = 0, state: OrderState = OrderState.OPENED):
        self._state = state
        if order_id == 0:
            Order._order_id_counter += 1
            self.order_id = Order._order_id_counter
            Order.order_id_set.add(Order._order_id_counter)
        else:
            _order_id = int(order_id)

            if not Order.order_id_set.__contains__(_order_id):
                Order.order_id_set.add(_order_id)

                if Order._order_id_counter < _order_id:
                    Order._order_id_counter = _order_id

            self.order_id = _order_id

        self._customer = customer
        self._positions = positions
        assert type(self._positions) is Positions
        print(self._positions._position_list)

        for position in self._positions._position_list:
            assert type(position) == Position            
            self.total += position.position_total
            
        self.total = round(self.total, 2)

        
    def save_order_to_csv(self):
        _orders_csv = Path("./Datenbanken/orders.csv")
        _exists = _orders_csv.exists()
        
        if _exists:
            with open(_orders_csv, "a") as file:
                file.write(f"{self.order_id};{self._customer};{self._state};{self._positions};{round(self.total)}\n")
        else:
            _directory = Path("./Datenbanken/")
            _directory_exists = _directory.exists()
            if not _directory_exists: os.mkdir("./Datenbanken/")
            with open(_orders_csv, "w") as file:
                file.write("Auftragsnummer;Kunde;Status;Positionen;Total\n")
                file.write(f"{self.order_id};{self._customer};{self._state};{self._positions};{round(self.total)}\n")
                
                
    def update_order_in_csv(self, state: OrderState, positions: Positions = None):
        _positions = positions

        if _positions != None: self._positions = _positions
        
        assert type(self._positions) is Positions

        self.total = 0.00
        for position in self._positions._position_list:
            assert type(position) is Position
            self.total += position.position_total


        


        _orders_csv = Path("./Datenbanken/orders.csv")
        _temp_orders_csv = Path("./Datenbanken/orders_temp.csv")
        _exists = _orders_csv.exists()
        if _exists:
            with open(_orders_csv, "r") as input_file, open(_temp_orders_csv, "w") as output_file:
                lines = input_file.readlines()
                for line in lines:
                    if line.strip("\n") != f"{self.order_id};{self._customer};{self._positions};{self.total}\n":
                        output_file.write(line)
                    else:
                        output_file.write(f"{self.order_id};{self._customer};{_positions};{self.total}\n")
                        
            os.remove("./Datenbanken/oders.csv")
            _temp_orders_csv.rename("./Datenbanken/orders.csv")
            
    def delete_order_in_csv(self):
        _orders_csv = Path("./Datenbanken/orders.csv")
        _temp_orders_csv = Path("./Datenbanken/orders_temp.csv")
        _exists = _orders_csv.exists()
        if _exists:
            with open(_orders_csv, "r") as input_csv_file, open(_temp_orders_csv, "w") as output_csv_file:
                lines = input_csv_file.readlines()
                for line in lines:
                    if line.strip("\n") != f"{self.order_id};{self._customer};{self._positions};{self.total}":
                        output_csv_file.write(line)
            os.remove("./Datenbanken/orders.csv")
            _temp_orders_csv.rename("./Datenbanken/orders.csv")
    
    
    def __repr__(self):
        return repr((self.order_id, self._customer, self._positions, self._position_total))

    def __str__(self):
        return f"Kunde: {self._customer}, Auftragsnummer {self.order_id}"
    