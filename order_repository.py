""" Data classes neccessary for order processing module"""

from pathlib import Path
from typing import List
from enum import Enum
import os

import customer_repository

class Item:
    '''Class holding the different items sold by the company'''

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
        '''Method saving the information of the item to a csv file'''

        _items_csv = Path("./Datenbanken/items.csv")
        _exists = _items_csv.exists()

        if _exists:
            with open(_items_csv, "a", encoding="UTF-8") as file:
                file.write(f"{self.item_number};{self.item_name};{self.unit_price}\n")

        else:
            _db_directory = Path("./Datenbanken/")
            _db_directory_exists = _db_directory.exists()
            if not _db_directory_exists:
                os.mkdir("./Datenbanken/")

            with open(_items_csv, "w", encoding="UTF-8") as file:
                file.write("item_number;name;unit_price\n")
                file.write(f"{self.item_number};{self.item_name};{self.unit_price}\n")

    def update_item_in_csv(self, item_name = "", unit_price = ""):
        '''Method updating the item information in the csv file'''

        _item_name = item_name
        _unit_price = unit_price

        if _item_name == "":
            _item_name = self.item_name
        if _unit_price == "":
            _unit_price = self.unit_price

        _items_csv = Path("./Datenbanken/items.csv")
        _temp_items_csv = Path("./Datenbanken/temp_items.csv")
        _exists = _items_csv.exists()
        if _exists:
            with (
                open(_items_csv, "r", encoding="UTF-8") as input_file,
                open(_temp_items_csv, "w", encoding="UTF-8") as output_file
                ):
                lines = input_file.readlines()
                for line in lines:
                    if line.strip("\n") != (f"{self.item_number};"
                                            f"{self.item_name};{self.unit_price}\n"):
                        output_file.write(line)
                    else:
                        output_file.write(f"{self.item_number}"
                                          f";{self.item_name};{self.unit_price}\n")

            os.remove("./Datenbanken/items.csv")
            _temp_items_csv.rename("./Datenbanken/items.csv")

    def delete_item_form_csv(self):
        '''Method deleting item information from the csv file'''

        _items_csv = Path("./Datenbanken/items.csv")
        _temp_items_csv = Path("./Datenbanken/items_temp.csv")
        _exists = _items_csv.exists()
        if _exists:
            with (
                open(_items_csv, "r", encoding="UTF-8") as input_csv_file,
                open(_temp_items_csv, "w", encoding="UTF-8") as output_csv_file,
            ):
                lines = input_csv_file.readlines()
                for line in lines:
                    if line.strip("\n") != (f"{self.item_number}"
                                            f";{self.item_name};{self.unit_price}"):
                        output_csv_file.write(line)

            os.remove("./Datenbanken/items.csv")
            _temp_items_csv.rename("./Datenbanken/items.csv")


    def __repr__(self):
        return repr((self.item_number, self.item_name, self.unit_price))


    def __str__(self):
        return f"{self.item_number},{self.item_name},{self.unit_price}"


class Position:
    '''Class holding all order positions'''
    position_number = 0
    position_id_counter = 0
    line_total = 0

    def __init__(self, item: Item, count: int, order_id: int):
        self.position_id_counter += 1
        self.position_id = self.position_id_counter
        self._order_id = order_id

        self.item = item
        self.count = count
        self.line_total = item.unit_price * count

    def save_position_to_csv(self):
        '''Method saving position information to a csv'''

        _positions_csv = Path("./Datenbanken/positions.csv")
        _exists = _positions_csv.exists()

        if _exists:
            with open(_positions_csv, "a", encoding="UTF-8") as file:
                file.write(f"{self.position_id};{self._order_id};{self.position_number}"
                           f";{self.item.item_number};{self.count}\n")

        else:
            _db_directory = Path("./Datenbanken/")
            _db_directory_exists = _db_directory.exists()
            if not _db_directory_exists:
                os.mkdir("./Datenbanken/")

            with open(_positions_csv, "w", encoding="UFT-8") as file:
                file.write("position_id;order_id;position_number;item_number;count\n")
                file.write(f"{self.position_id};{self._order_id};{self.position_number}"
                           f";{self.item.item_number};{self.count}\n")

    def update_position_in_csv(self, item: Item = None, count: int = None):
        """Method to update the position information inside the csv file"""

        if item is not None:
            self.item = item

        if count is not None:
            self.count = count

        assert isinstance(self.item, Item)
        assert isinstance(self.count, int)

        _positions_csv = Path("./Datenbanken/positions.csv")
        _temp_positions_csv = Path("./Datenbanken/positions_temp.csv")
        _exists = _positions_csv.exists()
        if _exists:
            with (
                open(_positions_csv, "r", encoding="UTF-8") as input_file,
                open(_temp_positions_csv, "w", encoding="UTF-8") as output_file,
            ):
                lines = input_file.readlines()
                for line in lines:
                    if line.strip("\n") != (f"{self.position_id};{self._order_id};"
                                            f"{self.item};{self.count}"):
                        output_file.write(line)
                    else:
                        output_file.write(f"{self.position_id};{self._order_id};"
                                          f"{self.item};{self.count}")
            os.remove("./Datenbanken/positions.csv")
            _temp_positions_csv.rename("./Datenbanken/positions.csv")

    def delete_position_in_csv(self):
        '''Method deleting position information from csv file'''

        _positions_csv = Path("./Datenbanken/positions.csv")
        _temp_positions_csv = Path("./Datenbanken/positons_temp.csv")
        _exists = _positions_csv.exists()
        if _exists:
            with (
                open(_positions_csv, "r", encoding="UTF-8") as input_file,
                open(_temp_positions_csv, "w", encoding="UTF-8") as output_file,
            ):
                lines = input_file.readlines()
                for line in lines:
                    if line.strip("\n") != (f"{self.position_id};{self._order_id};"
                                            f"{self.item};{self.count}"):
                        output_file.write(line)
            os.remove("./Datenbanken/positions.csv")
            _temp_positions_csv.rename("./Datenbanken/positions.csv")

    def __copy__(self):
        return Position(self.item, self.count, self._order_id)

    def __repr__(self):
        return repr((self.item.item_number, self.count))

    def __str__(self):
        return f"{self.position_id},{self.item.item_number},{self.count}"


class OrderState(Enum):
    '''Enum providing the allowed order states'''

    OPENED = "Offen"
    WIP = "InArbeit"
    DONE = "Versand"
    PAYED = "Bezahlt"
    HALT = "Pausiert"
    CLOSED = "Geschlossen"


class Order:
    '''Class holding the information of a order'''

    order_id_set = set()
    _order_id_counter = 0
    _total_before_discount = 0.00
    total = 0
    state = None

    default_quantity_discount_qualifier = 100.00
    default_quantity_discount = 0.1

    def __init__(
        self,
        customer: customer_repository.Customer,
        positions: List[Position],
        order_id: int = 0,
        state: OrderState = OrderState.OPENED):

        self.state = state

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

        self.customer = customer
        self._positions = positions

        for position in self._positions:
            assert isinstance(position, Position)
            self._total_before_discount += position.line_total

        self._total_before_discount = round(self._total_before_discount, 2)

        if self._total_before_discount >= self.default_quantity_discount_qualifier:
            self.total = self._total_before_discount * self.default_quantity_discount
        else:
            self.total = self._total_before_discount

    def save_order_to_csv(self):
        '''Method used to save order information to csv file'''

        _orders_csv = Path("./Datenbanken/orders.csv")
        _exists = _orders_csv.exists()

        if _exists:
            with open(_orders_csv, "a", encoding="UTF-8") as file:
                file.write(f"{self.order_id};{self.customer};{self.state.value}\n")
        else:
            _directory = Path("./Datenbanken/")
            _directory_exists = _directory.exists()
            if not _directory_exists:
                os.mkdir("./Datenbanken/")
            with open(_orders_csv, "w", encoding="UTF-8") as file:
                file.write("order_id;customer;state\n")
                file.write(f"{self.order_id};{self.customer};{self.state.value}\n")

    def update_order_in_csv(self, state: OrderState = None, positions: List[Position] = None):
        '''Method used to update order information in the csv file'''

        _positions = positions

        if state is not None:
            self.state = state

        if _positions is not None:
            self._positions = _positions

        assert isinstance(self.state, OrderState)
        assert isinstance(self._positions, List[Position])

        self._total_before_discount = 0.00
        for position in self._positions:
            assert isinstance(position, Position)
            self._total_before_discount += position.line_total

        _orders_csv = Path("./Datenbanken/orders.csv")
        _temp_orders_csv = Path("./Datenbanken/orders_temp.csv")
        _exists = _orders_csv.exists()
        if _exists:
            with open(_orders_csv, "r", encoding="UTF-8") as input_file:
                with open(_temp_orders_csv, "w", encoding="UTF-8") as output_file:
                    lines = input_file.readlines()
                    for line in lines:
                        if line.strip("\n") != (f"{self.order_id}"
                                                f";{self.customer};{self.state.value}\n"):
                            output_file.write(line)
                        else:
                            output_file.write(f"{self.order_id}"
                                              f";{self.customer};{self.state.value}\n")

            os.remove("./Datenbanken/oders.csv")
            _temp_orders_csv.rename("./Datenbanken/orders.csv")

    def delete_order_in_csv(self):
        '''Method deleting order information from the csv file'''

        _orders_csv = Path("./Datenbanken/orders.csv")
        _temp_orders_csv = Path("./Datenbanken/orders_temp.csv")
        _exists = _orders_csv.exists()
        if _exists:
            with open(_orders_csv, "r", encoding="UTF-8") as input_csv_file:
                with open(_temp_orders_csv, "w", encoding="UTF-8") as output_csv_file:
                    lines = input_csv_file.readlines()
                    for line in lines:
                        if line.strip("\n") != (f"{self.order_id}"
                                                f";{self.customer};{self.state.value}"):
                            output_csv_file.write(line)
            os.remove("./Datenbanken/orders.csv")
            _temp_orders_csv.rename("./Datenbanken/orders.csv")

    def __repr__(self):
        return repr((
            self.order_id,
            self.customer,
            self.state,
            self._positions,
            self._total_before_discount))

    def __str__(self):
        return (f"Nummer: {self.order_id}, Kunde: {self.customer}, "
                f"Status: {self.state.value}, Positionen: {self._positions},"
                f" Total: {self._total_before_discount}")
