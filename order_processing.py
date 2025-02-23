"""Caches and menus of the order processing module"""

import copy
import traceback
from pathlib import Path

import customer_management
import printer
from order_repository import Item, Order, OrderState, Position


class ItemCache:
    """Cache to hold Item objects

    Raises:
        ItemNumberException: _description_
        ItemNotFoundException: _description_

    Returns:
        _type_: _description_
    """

    _item_cache: set[Item] = set()

    def __init__(self) -> None:
        _prep_item_list: list[str] = []
        _path = Path("./Datenbanken/items.csv")
        _item_csv_exists = _path.exists()
        if _item_csv_exists:
            try:
                with open(_path, "r", encoding="UTF-8") as _itemdb:
                    lines = _itemdb.readlines()
                    lines.pop(0)
                    for line in lines:
                        _prep_item_list.append(line.strip("\n"))

                    for _listed_item in _prep_item_list:
                        _prep_item = str.split(_listed_item, sep=";")

                        _item_number_exists = Item.item_number_set.__contains__(
                            int(_prep_item[0])
                        )
                        _item = Item(
                            _prep_item[1],
                            float(_prep_item[2]),
                            int(_prep_item[0]),
                        )
                        if not _item_number_exists:
                            self._item_cache.add(_item)
                        else:
                            raise ItemNumberException(
                                str(_item), "Itemnummer is bereits vergeben!"
                            )

            except ItemNumberException as exc:
                print(
                    f"Caught ItemNumberException with "
                    f"custom_kwarg={exc.custom_kwarg}"
                )
            except ValueError as exc:
                print(f"Caugh ValueError while initializing item cache: {exc.args}")

    def find_item_number(self, item_name: str) -> int | None:
        """Method to find the item number by name of the item"""

        if item_name == "":
            return None

        for item in self._item_cache:
            assert isinstance(item, Item)
            if item.item_name == item_name:
                return item.item_number
            return None

    def get_item(self, item_number: int) -> Item | None:
        """Method used to return the item object by its item number"""

        if item_number is None:
            return None

        try:
            for item in self._item_cache:
                assert isinstance(item, Item)
                if item.item_number == item_number:
                    # TODO: Copy cool here?
                    return copy.copy(item)

        except ItemNotFoundException:
            print("Caught ItemNotFoundException: Item {item_number} not found")
        return None

    def add_item_to_cache(self, item: Item) -> None:
        """Method used to add an item to the item cache"""
        self._item_cache.add(item)

    def remove_item_from_cache(self, item: Item) -> None:
        """Method used to remove an item from the item cache"""
        self._item_cache.pop(item)

    def update_cached_item(self, old: Item, new: Item) -> None:
        """Method used to update an item residing in the item cache"""
        self._item_cache.pop(old)
        self._item_cache.add(new)

    def print_item_cache(self) -> None:
        """Method used to print out the content of the item cache"""
        _item_tuple = tuple[Item](self._item_cache)
        _item_list = sorted(_item_tuple, key=lambda i: i.item_number)
        print("")
        for _item in _item_list:
            print("       ", _item)

    def __iter__(self):
        for _item in self._item_cache:
            return _item

    def __str__(self):
        return f"        {self._item_cache}"


class PositionCache:
    """
    Class for caching position objects

    Parameters
    ----------
    item_cache : ItemCache

    Attributes
    ----------
    position_cache : PositionCache
    """

    position_cache = set()

    def __init__(self, item_cache: ItemCache):
        assert isinstance(item_cache, ItemCache)

        _path = Path("./Datenbanken/positions.csv")
        _position_csv_exists = _path.exists()
        if _position_csv_exists:
            try:
                lines = self._read_csv(_path)
                _prep_position_str_list = self._remove_eol_from_str_list(lines)
                _position_value_list = self._convert_str_list_to_position_values(
                    _prep_position_str_list
                )

                print(f"_position_value_list: {_position_value_list}")

                for position_value in _position_value_list:
                    _position_id = position_value[0]
                    _position_number = position_value[1]
                    _order_id = position_value[2]
                    _item = item_cache.get_item(position_value[3])
                    _count = position_value[4]
                    _position = Position(
                        item=_item,
                        count=_count,
                        order_id=_order_id,
                        position_number=_position_number,
                        position_id=_position_id,
                    )
                    self.add_position_to_cache(_position)
            except AssertionError as err:
                print(
                    "Caught an AssertionError on ItemCache object during "
                    f"PositionCache initialization: {err}"
                )

    def get_positions(self, order_id: int) -> list[Position]:
        """
        Gets all positions of an order provided the order id

        Paramaters
        ----------
        order_id : int

        Returns
        -------
        list(Position) ordered by the position_number
        """
        _hits = []
        for pos in self.position_cache:
            assert isinstance(pos, Position)
            if pos.order_id == order_id:
                _hits.append(pos)
        return _hits

    def add_position_to_cache(self, position: Position) -> None:
        """
        Adds a position object to cache

        Parameters
        ----------
        position : Position
        """
        self.position_cache.add(position)

    def update_position_in_cache(
        self,
        old_position: Position,
        new_position: Position,
    ) -> None:
        """
        Swaps a position object in the cache for an updated position object

        Parameters
        ----------
        old_positon : Position
        new_position : Position
        """

        self.position_cache.remove(old_position)
        self.position_cache.add(new_position)

    def remove_position_from_cache(self, position: Position) -> None:
        """
        Removes a position object from cache

        Parameters
        ----------
        position : Position
        """

        self.position_cache.remove(position)

    def _read_csv(self, path: Path) -> list[str]:
        """Reads lines from a csv file at provided Path -> list(str)"""
        _path = path
        with open(_path, "r", encoding="UTF-8") as _positiondb:
            lines = _positiondb.readlines()
            lines.pop(0)
            return lines

    def _remove_eol_from_str_list(self, lines: list[str]) -> list[str]:
        """Removes eol from each str in list -> list(str)"""
        _eol_removed_str_list = []
        for line in lines:
            _eol_removed_str_list.append(line.strip("\n"))
        return _eol_removed_str_list

    def _convert_str_list_to_position_values(
        self,
        position_string_list: [str],
    ) -> list[list[str]]:
        """
        Returns a list of lists of value strings, describing a Position object
        """

        _position_values = []
        for _listed_position in position_string_list:
            _prep_position = str.split(_listed_position, sep=";")
            print(f"_prep_position: {_prep_position}")
            if isinstance(_prep_position, list):
                _position_values.append(_prep_position)
            else:
                raise StringToPositionConversionException

        return _position_values


class PositionCacheException(Exception):
    """Base ItemCache exception class"""


class PositionCacheInitializationException(PositionCacheException):
    """Catches exceptions during initialization of the item cache"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.custom_kwarg = kwargs.get("custom_kwarg")


class StringToPositionConversionException(PositionCacheException):
    """Catches exceptions during str to position value conversion"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.custom_kwarg = kwargs.get("custom_kwarg")


class OrderCache:
    """
    Handles the order cache of the application. Initializes by
    reading all order saved in the orders.csv file. Depends on
    the other application caches regarding the order feature.

    Attributes
    ----------
    item_cache : ItemCache

    customer_cache : CustomerCache

    position_cache : PositionCache

    _order_cache : set(Order)
    """

    _order_cache = set()

    def __init__(
        self,
        item_cache: ItemCache,
        customer_cache: customer_management.CustomerCache,
        position_cache: PositionCache,
    ):
        self._item_cache = item_cache
        self._customer_cache = customer_cache
        self._position_cache = position_cache

        _path = Path("./Datenbanken/orders.csv")
        _order_csv_exists = _path.exists()
        if _order_csv_exists:
            try:
                lines = self._read_csv(_path)
                _prep_order_str_list = self._remove_eol_from_str_list(lines)
                _order_value_list = self._convert_str_to_order_values(
                    _prep_order_str_list,
                )

                # TODO: Loop through list of order values, generate order positions and build the list of order positions
                print(f"_order_values: {_order_value_list}")

                _position_number = 0
                for order_value in _order_value_list:
                    print(
                        f"order id: {order_value[0]};"
                        f"customer: {order_value[1]};"
                        f"order state: {order_value[2]}"
                    )

                    # TODO: Order ID needs to be checked earlier, before Order is created
                    _order_id_exists = int(order_value[0]) in Order.order_id_set

                    print(
                        f"_order_id_exists (before Order creation): {_order_id_exists}"
                    )

                    _position_number += 1
                    _order_id = int(order_value[0])
                    _positions = position_cache.get_positions(
                        int(order_value[0]),
                    )
                    _customer = customer_cache.get_customer(int(order_value[1]))
                    _order_state = order_value[2]

                    print(
                        f"_positions: {_positions}, "
                        f"_customer: {_customer}, "
                        f"_order_state: {_order_state}"
                    )

                    _order = Order(
                        customer=_customer,
                        positions=_positions,
                        state=_order_state,
                        order_id=_order_id,
                    )

                    print(
                        f"_order_id_exists: {_order_id_exists}, "
                        f"{_order.order_id} in {Order.order_id_set}"
                    )

                    if not _order_id_exists:
                        self._order_cache.add(_order)
                    else:
                        raise OrderIDException(
                            str(_order), "Order ID ist bereits vergeben!"
                        )

            except OrderIDException as exc:
                print(f"Caught OrderIDException with custom_kwarg={exc.custom_kwarg}")

            except AssertionError as err:
                print(
                    "Caught AssertionError during order cache "
                    f"initialization: {err, err.__traceback__.tb_lineno}"
                )
            except IndexError as err:
                print(
                    "Caught IndexError during order cache "
                    f"initialization: {err, err.__traceback__.tb_lineno}"
                )

    def find_order(self, customer: str = ""):
        """Method to find a order by the customer name"""

        _customer = ""
        if customer != "":
            _customer = customer

        for _order in self._order_cache:
            assert isinstance(_order, Order)
            if _order.customer_id == _customer:
                print(_order)

    def _read_csv(self, path: Path):
        _path = path
        with open(_path, "r", encoding="UTF-8") as _orderdb:
            lines = _orderdb.readlines()
            lines.pop(0)
            return lines

    def _remove_eol_from_str_list(self, lines: list[str]):
        _eol_removed_str_list = []
        for line in lines:
            _eol_removed_str_list.append(line.strip("\n"))
        return _eol_removed_str_list

    def _convert_str_to_order_values(self, order_string_list: list[str]):
        _order_values = []
        for _listed_order in order_string_list:
            _prep_order = str.split(_listed_order, sep=";")
            _order_state = self._convert_str_to_orderstate(_prep_order[2])
            _prep_order[2] = _order_state
            if isinstance(_prep_order, list):
                _order_values.append(_prep_order)
            else:
                raise StringToOrderConversionException

        return _order_values

    def _convert_str_to_orderstate(
        self,
        order_state_str: str,
    ) -> OrderState | None:
        _order_state_str = order_state_str

        print(f"_order_str_state: {_order_state_str}")
        try:
            match _order_state_str:
                case "Offen":
                    _order_state = OrderState.OPENED
                case "Pausiert":
                    _order_state = OrderState.HALT
                case "InArbeit":
                    _order_state = OrderState.WIP
                case "Versand":
                    _order_state = OrderState.DONE
                case "Bezahlt":
                    _order_state = OrderState.PAYED
                case "Geschlossen":
                    _order_state = OrderState.CLOSED
                case _:
                    raise OrderStateException

            return _order_state

        except OrderStateException:
            print(
                "Caught an OrderStateException: Order state "
                f"read from csv is invalid: {_order_state_str}"
            )
            return None

    def _rebuild_order_positions(
        self,
        item_cache: ItemCache,
        position_cache: PositionCache,
        position_values: list,
    ):
        _position_values = position_values
        _order_positions = []
        for pos in _position_values:
            # TODO: Whats up here?
            if pos in position_cache.position_cache:
                _position = Position(
                    item_cache.get_item(int(pos[1])),
                    int(pos[2]),
                    int(pos[0]),
                )
                _order_positions.append(_position)

        return _order_positions

    def get_order(self, order_id: int):
        """Method used to get the order object by its order id"""

        for _order in self._order_cache:
            assert isinstance(_order, Order)
            if _order.order_id == order_id:
                return _order
            return None

    def add_order_to_cache(self, order: Order) -> None:
        """Method to add an order object to the order cache"""
        self._order_cache.add(order)

    def remove_order_from_cache(self, order: Order) -> None:
        """Method to remove an order object from the order cache"""
        self._order_cache.remove(order)

    def update_cached_order(self, old: Order, new: Order) -> None:
        """Method to update an order object residing inside the order cache"""
        self._order_cache.remove(old)
        self._order_cache.add(new)

    def print_order_db(self) -> None:
        """
        Method used to print the content of the order cache to the console
        """

        _order_tuple = tuple[Order](self._order_cache)
        print(f"_order_tuple: {_order_tuple}")

        _sorted_order_list = sorted(_order_tuple, key=lambda o: o.order_id)
        print(f"_order_list: {_sorted_order_list}")

        print("")
        for _order in _sorted_order_list:
            print("        ", _order, sep="")

    def __iter__(self):
        for _order in self._order_cache:
            return _order

    def __str__(self):
        return f"        {self._order_cache}"


class OrderDBException(Exception):
    """A base class for OderDBExceptions"""


class ItemNumberException(OrderDBException):
    """Exception to catch invalid item numbers"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.custom_kwarg = kwargs.get("custom_kwarg")


class ItemNotFoundException(OrderDBException):
    """Exception catching situations where no matching item object is found"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.custom_kwarg = kwargs.get("custom_kwarg")


class OrderIDException(OrderDBException):
    """Exception catching invalid order id"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.custom_kwarg = kwargs.get("custom_kwarg")


class OrderStateException(OrderDBException):
    """Exception catching invalid order state"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.custom_kwarg = kwargs.get("custom_kwarg")


class StringToOrderConversionException(OrderDBException):
    """Exception catching exceptions while converting strings to Order objects"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.custom_kwarg = kwargs.get("custom_kwarg")


def order_processing_menu_loop(
    customer_cache: customer_management.CustomerCache,
    order_cache: OrderCache,
    item_cache: ItemCache,
):
    """Function running the menu loop of the order processing feature"""

    _menu_string = """
        ##########################################################################################################

        Auftragsbearbeitung

        Menü:                                                                          'c' um Bildschirm zu räumen
        1. Auftrag anlegen
        2. Auftrag bearbeiten
        3. Auftrag löschen
        4. Aufträge ausgeben
        5. Warenverwaltung
        6. Zurück zum Hauptmenü

        ##########################################################################################################
    """

    _order_processing = True
    while _order_processing is True:
        print(_menu_string)
        _menu_item = input(
            "        Bitte wählen sie den gewünschten Menüpunkt: ",
        )

        if _menu_item == "1":
            _customer_string = input("        Kundenname:")
            _customer_id = customer_cache.find_customer_id(
                company=_customer_string,
            )
            _customer = customer_cache.get_customer(_customer_id)
            if _customer is None:
                continue

            _temp_order = Order(_customer, [])
            _temp_order_id = _temp_order.order_id
            _temp_order.positions = get_order_positions(
                item_cache,
                _temp_order_id,
            )

            if _temp_order.positions is None:
                print(
                    "        Fehler: Positionen konnten nicht erstellt werden",
                )
            else:
                if _customer:

                    _order = Order(_customer, _positions)
                    _order.save_order_to_csv()
                    order_cache.add_order_to_cache(_order)
                    print("        Auftrag erfolgreich erstellt")
                else:
                    print("        Fehler: Kunde nicht gefunden")

        elif _menu_item == "2":
            _local_item_number = input(
                "        Bitte geben sie die "
                "Auftragsnummer des zu bearbeitenden Auftrags ein:"
            )

            _unmodified_order = order_cache.get_order(int(_local_item_number))

            if _unmodified_order is None:
                pass
            else:
                # TODO: Fix function parameters
                _new_positions = get_order_positions(item_cache)

                if _new_positions is None:
                    print("        Fehler: Positionen konnten nicht erzeugt werden")
                else:
                    _new_order = Order(
                        customer=_unmodified_order.customer_id,
                        positions=_new_positions,
                        order_id=_unmodified_order.order_id,
                        state=_unmodified_order.state,
                    )
                    order_cache.update_cached_order(_unmodified_order, _new_order)
                    _unmodified_order.delete_order_in_csv()
                    _new_order.save_order_to_csv()

        elif _menu_item == "3":
            _local_item_number = input(
                "        Bitte geben sie die Auftragsnummer"
                " des zu löschenden Auftrags ein:"
            )
            _order_to_delete = order_cache.get_order(int(_local_item_number))
            if _order_to_delete is None:
                pass
            else:
                assert isinstance(_order_to_delete, Order)
                order_cache.remove_order_from_cache(_order_to_delete)
                _order_to_delete.delete_order_in_csv()

        elif _menu_item == "4":
            order_cache.print_order_db()

        elif _menu_item == "5":
            item_management_menu_loop(item_cache=item_cache)

        elif _menu_item == "6":
            _order_processing = False

        elif _menu_item == "c":
            printer.Printer.clear_cli()


def get_order_positions(item_cache: ItemCache, order_id: int) -> list[Position]:
    """Function to build the positions object when creating an order"""
    _order_id: int = order_id
    _order_number_counter: int = 1
    _adding_positions: bool = True
    _position_value_str_int: list[(str, int, int)] = []
    _positions: list[Position] = []
    while _adding_positions:
        _count = None
        _position_valid = True

        _item_name_or_number_str = input(
            "        Itemname oder -nummer"
            " ('fertig' um die Eingabe von"
            " Positionen zu beenden): "
        )

        if _item_name_or_number_str == "fertig":
            print("        Keine weiteren Items.")
            break

        _count_str = input("        Stück: ")
        try:
            _count = int(_count_str)
        except ValueError as exc:
            print(exc)
            continue

        if _item_name_or_number_str != "" and _position_valid:
            _position_value_str_int.append(
                [_item_name_or_number_str, _count, _order_number_counter],
            )
        else:
            print(
                "        Position lässt sich aus den Angaben nicht erzeugen!",
            )
            continue
        _order_number_counter += 1

    for _position_value in _position_value_str_int:
        try:
            item_number = int(_position_value[0])
            item = item_cache.get_item(item_number)
        except ValueError:
            item_name = _position_value[0]
            item_number = item_cache.find_item_number(item_name)
            item = item_cache.get_item(item_number)

        if item is not None:
            print(f"Item data: {_position_value}")
            position = Position(
                item_cache.get_item(int(_position_value[0])),
                _position_value[1],
                _position_value[2],
                _order_id,
            )

            position.save_position_to_csv()
            _positions.append(position)
        else:
            print(f"        Warnung: Item '{_position_value[0]}' nicht gefunden")

    if _positions:
        return _positions

    print("        Fehler: Keine gültigen Positionen eingegeben")


def item_management_menu_loop(item_cache: ItemCache):
    """Function running the menu loop of the item management feature"""

    _menu_string = """
        ##########################################################################################################

        Warenverwaltung

        Menü:                                                                          'c' um Bildschirm zu räumen
        1. Ware anlegen
        2. Ware bearbeiten
        3. Ware löschen
        4. Warenliste ausgeben
        5. Zurück zur Auftragsbearbeitung

        ##########################################################################################################
    """

    _item_management = True
    while _item_management is True:
        print(_menu_string)
        _menu_item = input("        Bitte wählen Sie den gewünschten Menüpunkt: ")
        if _menu_item == "1":
            _name = input("        Bitte geben sie den Namen der Ware ein: ")
            _unit_price = input("        Bitte geben sie den Stückpreis der Ware ein: ")
            _item = Item(item_name=_name, unit_price=_unit_price)
            _item.save_item_to_csv()
            item_cache.add_item_to_cache(_item)

        elif _menu_item == "2":
            _item_number = input(
                "        Bitte geben sie die Artikelnummer des Artikels an: "
            )
            _old_item = item_cache.get_item(int(_item_number))
            print(f"        Bisheriger Stückpreis: {_old_item.unit_price}")
            _new_unit_price = input(
                "        Bitte geben sie den neuen Stückpreis ein: "
            )
            _new_item = Item(
                _old_item.item_name, _new_unit_price, _old_item.item_number
            )
            item_cache.update_cached_item(_old_item, _new_item)
            print("        Artikel wurde aktualisiert!")

        elif _menu_item == "3":
            _item_number = input(
                "        Bitte geben sie die Artikelnummer des zu "
                "löschenden Artikels ein: "
            )
            _item = item_cache.get_item(int(_item_number))
            _item.delete_item_form_csv()
            item_cache.remove_item_from_cache(_item)
            print("        Artikel wurde erfolgreich aus dem System gelöscht!")

        elif _menu_item == "4":
            item_cache.print_item_cache()

        elif _menu_item == "5":
            _item_management = False

        elif _menu_item == "c":
            printer.Printer.clear_cli()
