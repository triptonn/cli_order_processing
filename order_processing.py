"""Caches and menus of the order processing module"""

import copy
from pathlib import Path

import customer_management
import printer
from customer_repository import Customer
from order_repository import Item, Order, OrderState, Position


# TODO: Doc string ItemCache
class ItemCache:
    """
    Cache to hold Item objects

    Attributes:
        [set][[Item]]:

    Raises:
        [ItemNotFoundException]: Exception catching situations
        where no matching item object is found in the cache.
        [ItemNumberException]:
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
                                **{
                                    "item_number": _prep_item[0],
                                    "item_name": _prep_item[1],
                                }
                            )

            except ItemNumberException as exc:
                print(
                    f"Caught ItemNumberException with "
                    f"{exc.item_name}: Item number {exc.item_number} "
                    "is already taken!"
                )
            except ValueError as exc:
                print(f"Caugh ValueError while initializing item cache: {exc}")

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
                    return copy.copy(item)
                raise ItemNotFoundException(**{"item_number": item_number})

        except ItemNotFoundException as exc:
            print(
                f"Caught ItemNotFoundException: Item {exc.item_number} not found in the cache."
            )
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
            print(_item)

    def __iter__(self):
        for _item in self._item_cache:
            return _item

    def __str__(self):
        return f"{self._item_cache}"


def item_management_menu_loop(item_cache: ItemCache):
    """Function running the menu loop of the item management feature"""

    _menu_string = """
 ###############################################################################

 Warenverwaltung

 Menü:                                               'c' um Bildschirm zu räumen
 1. Ware anlegen
 2. Ware bearbeiten
 3. Ware löschen
 4. Warenliste ausgeben
 5. Zurück zur Auftragsbearbeitung

 ################################################################################
"""

    _item_management = True
    while _item_management is True:
        print(_menu_string)
        _menu_item = input("Bitte wählen Sie den gewünschten Menüpunkt: ")
        if _menu_item == "1":
            _name = input("Bitte geben sie den Namen der Ware ein: ")
            _unit_price = input("Bitte geben sie den Stückpreis der Ware ein: ")
            _item = Item(item_name=_name, unit_price=_unit_price)
            _item.save_item_to_csv()
            item_cache.add_item_to_cache(_item)

        elif _menu_item == "2":
            _item_number = input("Bitte geben sie die Artikelnummer des Artikels an: ")
            _old_item = item_cache.get_item(int(_item_number))
            print(f"        Bisheriger Stückpreis: {_old_item.unit_price}")
            _new_unit_price = input("Bitte geben sie den neuen Stückpreis ein: ")
            _new_item = Item(
                _old_item.item_name, _new_unit_price, _old_item.item_number
            )
            item_cache.update_cached_item(_old_item, _new_item)
            print("Artikel wurde aktualisiert!")

        elif _menu_item == "3":
            _item_number = input(
                "Bitte geben sie die Artikelnummer des zu löschenden Artikels ein: "
            )
            _item = item_cache.get_item(int(_item_number))
            _item.delete_item_form_csv()
            item_cache.remove_item_from_cache(_item)
            print("Artikel wurde erfolgreich aus dem System gelöscht!")

        elif _menu_item == "4":
            item_cache.print_item_cache()

        elif _menu_item == "5":
            _item_management = False

        elif _menu_item == "c":
            printer.Printer.clear_cli()


class ItemCacheException(Exception):
    """A base class for ItemCache exceptions"""


class ItemNumberException(ItemCacheException):
    """Exception to catch invalid item numbers"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.item_number = kwargs.get("item_number")
        self.item_name = kwargs.get("item_name")


class ItemNotFoundException(ItemCacheException):
    """
    Exception catching situations where no matching
    item object is found in the cache.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.item_number = kwargs.get("item_number")


##############################################################################
#
# Order Processing
#
##############################################################################


class PositionCache:
    """
    Caches Position objects read from a file.

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
                    if _item is None:
                        raise ItemNotFoundException(
                            **{"item_number": position_value[3]}
                        )
                    _count = position_value[4]
                    _position = Position(
                        item=_item,
                        count=_count,
                        order_id=_order_id,
                        position_number=_position_number,
                        position_id=_position_id,
                    )
                    print(f"{_position}")
                    if _position is None or isinstance(_position, Position):
                        raise PositionCacheInitializationException(
                            **{"position": _position}
                        )
                    self.add_position_to_cache(_position)
            except ItemNotFoundException as exc:
                print(
                    f"Caught an ItemNotFoundException on item number {exc.item_number}"
                )

            except PositionCacheInitializationException as exc:
                print(
                    f"Caught PositionCacheInitializationException on Position {exc.position}"
                )

            except AssertionError as err:
                print(
                    "Caught an AssertionError on ItemCache object during "
                    f"PositionCache initialization: {err}"
                )

    def get_positions(self, order_id: int) -> list[Position]:
        """
        Gets all positions of an order provided the order id

        Parameters
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
        self.position = kwargs.get("position")


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

    _order_cache: set[Order] = set()

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

        if not _order_csv_exists:
            pass
        try:
            lines = self._read_csv(_path)
            _prep_order_str_list = self._remove_eol_from_str_list(lines)
            _order_value_list = self._convert_str_to_order_values(
                _prep_order_str_list,
            )

            _position_number = 0
            for order_value in _order_value_list:
                _order_id_exists = int(order_value[0]) in Order.order_id_set

                _position_number += 1
                _order_id = int(order_value[0])
                _positions = position_cache.get_positions(
                    int(order_value[0]),
                )
                _customer = customer_cache.get_customer(int(order_value[1]))
                _order_state = order_value[2]

                _order = Order(
                    customer=_customer,
                    positions=_positions,
                    state=_order_state,
                    order_id=_order_id,
                )

                if not _order_id_exists:
                    self._order_cache.add(_order)
                else:
                    raise OrderIDException(
                        "Order ID ist bereits vergeben!",
                        **{"order_id": _order_id},
                    )

        except OrderIDException as exc:
            print(f"Caught OrderIDException on order {exc.order_id}")

        except AssertionError as err:
            print(f"Caught AssertionError during order cache initialization: {err}")
        except IndexError as err:
            print(f"Caught IndexError during order cache initialization: {err}")

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
            _order_state = self.convert_str_to_orderstate(_prep_order[2])
            _prep_order[2] = _order_state
            if isinstance(_prep_order, list):
                _order_values.append(_prep_order)
            else:
                raise StringToOrderConversionException

        return _order_values

    def convert_str_to_orderstate(
        self,
        order_state_str: str,
    ) -> OrderState | None:
        """
        Receives str value and returns the relevant
        order state. If no order state can be matched
        None is returned

        Parameters
        ----------
        order_state_str : [str]

        Returns
        -------
        result : [OrderState] | [None]
        """
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

    def get_order(self, order_id: int) -> Order | None:
        """
        Finds Order object for provided order id in
        the OrderCache and returns it.

        Parameters
        ----------
        order_id : [int]

        Returns
        -------
        result : [Order] | [None]
        """
        try:
            for _order in self._order_cache:
                if isinstance(_order, Order):
                    if _order.order_id == order_id:
                        return _order
                else:
                    raise OrderCacheTypeException(
                        **{
                            "order_id": f"{order_id}",
                            "caught_object": f"{_order}",
                            "object_type": f"{type(_order)}",
                        }
                    )

        except OrderCacheTypeException as exc:
            print(
                f"Caught OrderCacheTypeException in order {exc.order_id}: "
                f"{exc.caught_object} ({exc.object_type}) is not a valid "
                "OrderCache type"
            )

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

    def print_order_detail(self, order_id: int = 0) -> bool:
        decided = False
        _id = None

        while not decided:
            if order_id == 0:
                try:
                    print("                          ?")
                    _string = input("Bitte Auftragsnummer eingeben oder (a)bbruch: ")
                    if _string == "a" or _string == "abbruch" or _string == "(a)bbruch":
                        return False
                    _id = int(_string)
                    decided = True
                except TypeError:
                    print("Eingabe ist kein gültiger Integer Wert!")
            else:
                if order_id > 0 and isinstance(order_id, int):
                    _id = order_id
                    decided = True
                else:
                    raise OrderNotFoundException(*{order_id})

        _order = self.get_order(_id)
        if _order is None:
            print("Order id could not be found!")
            return False

        print(
            f"Order {_order.order_id} / {_order.customer.company}:\n"
            "PosNr, Artikelname, Menge, Summe"
        )
        _total: float = 0.00
        print(f"{self._position_cache.position_cache}, {_order.order_id}")
        for pos in self._position_cache.get_positions(_order.order_id):
            _line_total = pos.item.unit_price * pos.count
            _total += _line_total
            print(
                f"{pos.position_number}: {pos.item.item_name}"
                f", {pos.count}, {_line_total}"
            )

        print(f"Gesamt: {_total} EUR")

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


class OrderCacheException(Exception):
    """A base class for OrderCache exceptions"""


class OrderIDException(OrderCacheException):
    """Exception catching invalid order id."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.order_id = kwargs.get("order_id")


class OrderNotFoundException(OrderCacheException):
    """Exception catching if an Order object can't be found in the cache"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.order_id = kwargs.get("order_id")


class OrderStateException(OrderCacheException):
    """Exception catching invalid order state"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.order_state = kwargs.get("order_state")


class OrderCacheTypeException(OrderCacheException):
    """Exception catching wrong types in the OrderCache"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.order_id = kwargs.get("order_id")
        self.caught_object = kwargs.get("caught_object")
        self.object_type = kwargs.get("object_type")


class StringToOrderConversionException(OrderCacheException):
    """Exception catching exceptions while converting strings to Order objects"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.custom_kwarg = kwargs.get("custom_kwarg")


def order_processing_menu_loop(
    customer_cache: customer_management.CustomerCache,
    order_cache: OrderCache,
    position_cache: PositionCache,
    item_cache: ItemCache,
):
    """Function running the menu loop of the order processing feature"""

    _menu_string = """
###############################################################################

Auftragsbearbeitung

Menü:                                               'c' um Bildschirm zu räumen
1. Auftrag anlegen
2. Auftrag bearbeiten
3. Auftrag löschen
4. Auftragsdetails ausgeben
5. Aufträge ausgeben
6. Warenverwaltung
7. Zurück zum Hauptmenü

###############################################################################
"""

    _order_processing = True
    while _order_processing is True:
        print(_menu_string)
        _menu_item = input(
            "Bitte wählen sie den gewünschten Menüpunkt: ",
        )

        if _menu_item == "1":
            result: bool = create_order(
                item_cache,
                customer_cache,
                order_cache,
            )
            if result is False:
                continue

        elif _menu_item == "2":
            result: bool = modify_order(
                item_cache,
                position_cache,
                order_cache,
            )

        elif _menu_item == "3":
            _local_item_number = input(
                "Bitte geben sie die Auftragsnummer" " des zu löschenden Auftrags ein:"
            )
            _order_to_delete = order_cache.get_order(int(_local_item_number))
            if _order_to_delete is None:
                pass
            else:
                assert isinstance(_order_to_delete, Order)
                for pos in _order_to_delete.positions:
                    position_cache.remove_position_from_cache(pos)
                    pos.remove_position_from_csv()
                order_cache.remove_order_from_cache(_order_to_delete)
                _order_to_delete.delete_order_in_csv()

        elif _menu_item == "4":
            order_cache.print_order_detail()

        elif _menu_item == "5":
            order_cache.print_order_db()

        elif _menu_item == "6":
            item_management_menu_loop(item_cache=item_cache)

        elif _menu_item == "7":
            _order_processing = False

        elif _menu_item == "c":
            printer.Printer.clear_cli()


def create_order(
    item_cache: ItemCache,
    customer_cache: customer_management.CustomerCache,
    order_cache: OrderCache,
) -> bool:
    """
    Creates new Order object
    """
    _customer_string = input("Kundenname: ")
    _customer_id = customer_cache.find_customer_id(
        company=_customer_string,
    )
    _customer: Customer = customer_cache.get_customer(_customer_id)
    if _customer is None:
        return False

    _order = Order(_customer, [])
    _temp_order_id = _order.order_id
    _order.positions = get_order_positions(
        item_cache,
        _temp_order_id,
    )

    if _order.positions is None:
        print(
            "Fehler: Positionen konnten nicht erstellt werden",
        )
        return False

    if isinstance(_order, Order):
        _order.save_order_to_csv()
        order_cache.add(_order)
        print("Auftrag erfolgreich erstellt")
        return True

    print("Fehler: Kunde nicht gefunden")
    return False


def modify_order(
    item_cache: ItemCache,
    position_cache: PositionCache,
    order_cache: OrderCache,
) -> bool:
    """
    Manages modifying an Order object and returns the result
    as a boolean value.

    Parameters
    ----------
    item_cache : ItemCache

    position_cache : PositionCache

    order_cache : OrderCache

    Returns
    -------
    bool
    """
    _local_item_number = input(
        "Bitte geben sie die " "Auftragsnummer des zu bearbeitenden Auftrags ein: "
    )
    print(
        f"entry: {_local_item_number}, intified: {int(_local_item_number), type(int(_local_item_number))}"
    )
    _old_order = order_cache.get_order(int(_local_item_number))
    assert isinstance(_old_order, Order)

    print(f"_unmodified_order: {_old_order}")

    _new_positions = None
    _new_order_state = None

    _modify_positions = input("Do you need to modify order positions? (Y/n) ") == "Y"
    _modify_state = input("Do you need to modify the order state? (Y/n) ") == "Y"

    print(
        f"You selected the following options:\n"
        f"Modify order positions: {_modify_positions}\n"
        f"Modify order state: {_modify_state}"
    )
    try:
        if (
            _modify_positions is False and _modify_state is False
        ) or _old_order is None:
            raise ModifyOrderException(
                **{
                    "old_order": _old_order,
                    "old_order_type": type(_old_order),
                }
            )
    except ModifyOrderException as exc:
        print(
            f"Caught ModifyOrderException for order {exc.old_order} "
            f"({exc.old_order_type})\nEither there is a problem with "
            "the old Order object or there seems to be nothing to change."
        )
        return False

    if _modify_state is True:
        _new_state_str = input(
            "(Offen, InArbeit, Versandt, Bezahlt, Pausiert,"
            " Geschlossen)\nPlease enter the updated order state: "
        )
        _new_order_state = order_cache.convert_str_to_orderstate(
            _new_state_str,
        )
        if _new_order_state is None:
            return False

    if _modify_positions is True:
        _new_positions = get_order_positions(
            item_cache,
            _old_order.order_id,
        )

        if _new_positions is None or _new_positions == []:
            print(
                "Fehler: Neue Positionen konnten nicht erzeugt werden",
            )
            return False

        _isfinal: bool = (
            input(
                "Do you really want to overwrite the exisiting "
                "order positions? (Y/n): "
            )
            == "Y"
        )
        if not _isfinal:
            return False

    _new_order = Order(
        customer=_old_order.customer,
        positions=(
            (
                _new_positions
                if _modify_positions is True
                else position_cache.get_positions(_old_order.order_id)
            )
        ),
        order_id=_old_order.order_id,
        state=(_new_order_state if _modify_state is True else _old_order.state),
        modify=True,
    )

    remove_old_positions_from_position_cache(
        position_cache,
        _old_order.positions,
    )

    order_cache.update_cached_order(_old_order, _new_order)
    _old_order.delete_order_in_csv()
    _new_order.save_order_to_csv()

    return True


def get_order_positions(
    item_cache: ItemCache,
    order_id: int,
) -> list[Position] | None:
    """
    Builds the list of Position object's when creating an order.
    Returns either a [list][[Position]] or [None].

    Parameters
    ----------
    item_cache : [ItemCache]
    order_id : [int]

    Returns
    -------
    positions : [list][[Position]] | [None]
    """
    _order_id: int = order_id
    _adding_positions: bool = True
    _position_number_counter: int = 1
    _positions: list[Position] = []
    while _adding_positions:
        _item_str = get_item_name_or_number()
        if _item_str == "fertig":
            print("Keine weiteren Items.")
            break

        _count: int | None = get_item_count()
        if _count is None:
            continue

        if _item_str == "":
            print(
                "Position lässt sich nicht aus den Angaben erzeugen!",
            )
            continue

        try:
            item_number: int = int(_item_str)
            print(f"Item {_position_number_counter} is integer...")
        except ValueError:
            print(f"Item {_position_number_counter} is str...")
            item_name = _item_str
            item_number = item_cache.find_item_number(item_name)
            if item_number is None:
                print(
                    f"Item {_position_number_counter} is not valid... try again...",
                )
                continue

        _item: Item | None = item_cache.get_item(item_number)
        try:
            assert isinstance(_item, Item)
        except AssertionError:
            print(
                f"Item {_position_number_counter} ",
                "is not valid... try again...",
            )
            continue

        _position_item: Item | None = _item
        if isinstance(_position_item, Item):
            print(f"Item data: {_item}")
            _position = Position(
                _position_item,
                _count,
                _order_id,
                _position_number_counter,
            )
            print(f"Position: {_position}")
            _position.save_position_to_csv()
            _positions.append(_position)
        else:
            print(f"Warnung: '{_item}' nicht gefunden" "... Bitte nochmal versuchen...")
            continue

        _position_number_counter += 1

    print(f"_positions: {_positions}")

    _is_valid = True
    for pos in _positions:
        if not isinstance(pos, Position):
            _is_valid = False

    if not _is_valid:
        print(
            "Fehler: Keine gültigen Positionen eingegeben! "
            "Bitte starten sie den Vorgang von Neuem."
        )
        return None

    return _positions


def remove_old_positions_from_position_cache(
    position_cache: PositionCache,
    old_positions: list[Position],
) -> None:
    """
    Removes the old Position objects of the modified order
    from the position cache and from the positions.csv.

    Parameters
    ----------
    position_cache : [PositionCache]
    old_positions : [list][[Position]]
    """
    try:
        for pos in old_positions:
            if not isinstance(pos, Position):
                raise RemovePositionException(
                    **{
                        "pos": pos,
                        "old_positions": old_positions,
                    }
                )
            pos.remove_position_from_csv()
            position_cache.remove_position_from_cache(pos)
    except RemovePositionException as exc:
        print(
            "Caught RemovePositionException while trying to remove "
            f"old Position object {exc.pos} from {exc.old_positions}"
        )


def get_item_name_or_number() -> str:
    """
    Asks user for input of an item name or item number for this position -> str
    """
    _item_name_or_number_str = input(
        "Itemname oder -nummer"
        " ('fertig' um die Eingabe von"
        " Positionen zu beenden): "
    )
    return _item_name_or_number_str


def get_item_count() -> int | None:
    """
    Asks user for input of an item count for this position.
    Needs to be a valid integer.

    Returns
    -------
    _count : [int] | [None]
    """
    _count = None
    _count_str = input("        Stück: ")
    try:
        _count = int(_count_str)
        return _count
    except ValueError:
        print("Value is not a valid integer... try again...")
        return None


class OrderProcessingException(Exception):
    """Base exception class for exceptions during order processing"""


class RemovePositionException(OrderProcessingException):
    """
    Exception catching problems during the removal of
    the old positions of a modified Order object.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.pos = kwargs.get("pos")
        self.old_positions = kwargs.get("old_positions")


class ModifyOrderException(OrderProcessingException):
    """
    Exception catching problems during the modification
    of a modified Order object.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.old_order = kwargs.get("old_order")
        self.old_order_type = kwargs.get("old_order_type")
