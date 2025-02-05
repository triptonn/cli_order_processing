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
        return repr((self.item.item_number, self.count))

    def __str__(self):
        return f"{self.item.item_number},{self.count}"


class Positions:
    def __init__(self, position_list: list):
        self._position_list = position_list

    def __str__(self):
        _len = len(self._position_list)
        _counter = 1
        _output_str = '{['
        for position in self._position_list:
            _pos = position
            assert type(position) is Position
            if _counter < _len:
                _output_str += "{" + f"{_pos}" + "}," 
                _counter += 1
            else:
                _output_str += "{" + f"{_pos}" + "}"
                break

        _output_str += "]}"
        return _output_str


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
    _total_before_discount = 0.00
    total = 0
    _state = None
    
    default_quantity_discount_qualifier = 100.00
    default_quantity_discount = 0.1
    
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

        for position in self._positions._position_list:
            assert type(position) == Position            
            self._total_before_discount += position.position_total
            
        self._total_before_discount = round(self._total_before_discount, 2)
        
        if self._total_before_discount >= self.default_quantity_discount_qualifier:
            self.total = self._total_before_discount * self.default_quantity_discount
        else:
            self.total = self._total_before_discount
        
    def save_order_to_csv(self):
        _orders_csv = Path("./Datenbanken/orders.csv")
        _exists = _orders_csv.exists()
        
        if _exists:
            with open(_orders_csv, "a") as file:
                file.write(f"{self.order_id};{self._customer};{self._state.value};{self._positions}\n")
        else:
            _directory = Path("./Datenbanken/")
            _directory_exists = _directory.exists()
            if not _directory_exists: os.mkdir("./Datenbanken/")
            with open(_orders_csv, "w") as file:
                file.write("Auftragsnummer;Kunde;Status;Positionen\n")
                file.write(f"{self.order_id};{self._customer};{self._state.value};{self._positions}\n")
                
    def update_order_in_csv(self, state: OrderState = None, positions: Positions = None):
        _positions = positions
        
        if state != None: self._state = state 

        if _positions != None: self._positions = _positions
       
        assert type(self._state) is OrderState
        assert type(self._positions) is Positions

        self._total_before_discount = 0.00
        for position in self._positions._position_list:
            assert type(position) is Position
            self._total_before_discount += position.position_total

        _orders_csv = Path("./Datenbanken/orders.csv")
        _temp_orders_csv = Path("./Datenbanken/orders_temp.csv")
        _exists = _orders_csv.exists()
        if _exists:
            with open(_orders_csv, "r") as input_file, open(_temp_orders_csv, "w") as output_file:
                lines = input_file.readlines()
                for line in lines:
                    if line.strip("\n") != f"{self.order_id};{self._customer};{self._state.value};{self._positions}\n":
                        output_file.write(line)
                    else:
                        output_file.write(f"{self.order_id};{self._customer};{self._state.value};{_positions}\n")
                        
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
                    if line.strip("\n") != f"{self.order_id};{self._customer};{self._state.value};{self._positions}":
                        output_csv_file.write(line)
            os.remove("./Datenbanken/orders.csv")
            _temp_orders_csv.rename("./Datenbanken/orders.csv")
    
    def __repr__(self):
        return repr((self.order_id, self._customer, self._state, self._positions, self._total_before_discount))

    def __str__(self):
        return f"Nummer: {self.order_id}, Kunde: {self._customer}, Status: {self._state.value}, Positionen: {self._positions}, Total: {self._total_before_discount}"
    