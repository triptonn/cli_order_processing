from pathlib import Path
import os
import customer

    
class item:
    item_number_set = set()
    _item_number_counter = 0
    
    def __init__(self, item_name, unit_price, item_number = "", ):
        self.item_number = item_number
        if item_number == "":
            item._item_number_counter += 1
            self.item_number = item._item_number_counter
            item.item_number_set.add(item._item_number_counter)
            
        else:
            _item_number = int(item_number)
            if not item.item_number_set.__contains__(_item_number):
                item.item_number_set.add(_item_number)
                if item._item_number_counter < _item_number:
                    item._item_number_counter = _item_number
            self.item_number = _item_number
            
        self._item_name = item_name
        self._unit_price = unit_price
        
    def save_item_to_csv(self):
        _items_csv = Path("./Datenbanken/items.csv")
        _exists = _items_csv.exists()

        if _exists:
            with open(_items_csv, "a") as file:
                file.write(f"{self.item_number};{self._item_name};{self._unit_price}\n")
                
        else:
            _db_directory = Path("./Datenbanken/")
            _db_directory_exists = _db_directory.exists()
            if not _db_directory_exists: os.mkdir("./Datenbanken/")

            with open(_items_csv, "w") as file:
                file.write("item_number;name;unit_price\n")
                file.write(f"{self.item_number};{self._item_name};{self._unit_price}\n")
                
    def update_item_in_csv(self, item_name = "", unit_price = ""):
        _item_name = item_name
        _unit_price = unit_price
        
        if _item_name == "": _item_name = self._item_name
        if _unit_price == "": _unit_price = self._unit_price
        
        _items_csv = Path("./Datenbanken/items.csv")
        _temp_items_csv = Path("./Datenbanken/temp_items.csv")
        _exists = _items_csv.exists()
        if _exists:
            with open(_items_csv, "r") as input_file, open(_temp_items_csv, "w") as output_file:
                lines = input_file.readlines()
                for line in lines:
                    if line.strip("\n") != f"{self.item_number};{self._item_name};{self._unit_price}\n":
                        output_file.write(line)
                    else:
                        output_file.write(f"{self.item_number};{self._item_name};{self._unit_price}\n")
            
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
                    if line.strip("\n") != f"{self.item_number};{self._item_name};{self._unit_price}":
                        output_csv_file.write(line)
            os.remove("./Datenbanken/items.csv")
            _temp_items_csv.rename("./Datenbanken/items.csv")
            

    def __repr__(self):
        return repr((self.item_number, self._item_name, self._unit_price))


    def __str__(self):
        return f"Artikelnummer {self.item_number}, {self._item_name}, {self._unit_price}"




class order:
    order_id_set = set()
    _order_id_counter = 0
    order_id = 0
    
    def __init__(self, customer: customer.Customer, total: float, order_id: str, items: list,):
        self.order_id = order_id     

        if order_id == "":
            order._order_id_counter += 1
            self.order_id = order._order_id_counter
            order.order_id_set.add(order._order_id_counter)
        
        else:
            _order_id = int(order_id)
            if not order.order_id_set.__contains__(_order_id):
                order.order_id_set.add(_order_id)
                if order._order_id_counter < _order_id:
                    order._order_id_counter = _order_id
            self.order_id = _order_id
            
        self._customer = customer
        self._total = total
        self._items = items
        
    def save_order_to_csv(self):
        _orders_csv = Path("./Datenbanken/orders.csv")
        _exists = _orders_csv.exists()
        
        if _exists:
            with open(_orders_csv, "a") as file:
                file.write(f"{self.order_id};{self._customer};{self._items};{self._total}\n")
        
        else:
            os.mkdir("./Datenbanken/")
            with open(_orders_csv, "w") as file:
                file.write("Auftragsnummer;Kunde;Positionen;Total\n")
                file.write(f"{self.order_id};{self._customer};{self._items};{self._total}\n")
                
                
    def update_order_in_csv(self, items = "", total = ""):
        _items = items
        _total = total
        
        if _items == "": _items = self._items
        if _total == "": _total = self._total
        
        _orders_csv = Path("./Datenbanken/orders.csv")
        _temp_orders_csv = Path("./Datenbanken/orders_temp.csv")
        _exists = _orders_csv.exists()
        if _exists:
            with open(_orders_csv, "r") as input_file, open(_temp_orders_csv, "w") as output_file:
                lines = input_file.readlines()
                for line in lines:
                    if line.strip("\n") != f"{self.order_id};{self._customer};{self._items};{self._total}\n":
                        output_file.write(line)
                    else:
                        output_file.write(f"{self.order_id};{self._customer};{_items};{_total}\n")
                        
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
                    if line.strip("\n") != f"{self._order_id};{self._customer};{self._items};{self._total}":
                        output_csv_file.write(line)
            os.remove("./Datenbanken/orders.csv")
            _temp_orders_csv.rename("./Datenbanken/orders.csv")
    
    
    def __repr__(self):
        return repr((self.order_id, self._customer, self._items, self._total))

    def __str__(self):
        return f"Kunde: {self._customer}, Auftragsnummer {self._order_id}"
    