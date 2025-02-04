from pathlib import Path
import os


class Customer:
    customer_id_set = set()
    _customer_id_counter = 0
    
    def __init__(self, lastname: str, name: str, company: str, street: str, house_number: str, postcode: str, city: str, customer_id: int = 0):
        self.customer_id = customer_id

        if customer_id == 0:
            Customer._customer_id_counter += 1
            self.customer_id = Customer._customer_id_counter
            Customer.customer_id_set.add(self._customer_id_counter)
        
        else:
            _customer_id = customer_id
            if not Customer.customer_id_set.__contains__(_customer_id):
                Customer.customer_id_set.add(_customer_id)
                if Customer._customer_id_counter < _customer_id:
                    Customer._customer_id_counter = _customer_id 
            self.customer_id = _customer_id 

        self.lastname = lastname
        self.name = name
        self.company = company
        self._street = street
        self._house_number = house_number
        self._postcode = postcode
        self._city = city

    def print_address(self):
        return f"Kunde: {self.customer_id}: {self._street} {self._house_number}, {self._postcode} {self._city}"
    
    def save_customer_to_csv(self):
        _customer_csv = Path("./Datenbanken/kunden.csv")
        _exists = _customer_csv.exists()
        
        if _exists:
            with open(_customer_csv, "a") as file:
                file.write(f"{self.customer_id};{self.name};{self.name};{self.company};{self._street};{self._house_number};{self._postcode};{self._city};\n")

        else:
            os.mkdir("./Datenbanken/")
            with open(_customer_csv, "w") as file:
                file.write("Kundennummer;Name;Vorname;Firma;Strasse;Hausnummer;Postleitzahl;Ort\n")
                file.write(f"{self.customer_id};{self.name};{self.name};{self.company};{self._street};{self._house_number};{self._postcode};{self._city};\n")

        
                
    def update_customer_in_csv(self, lastname = "", name = "", company = "", street = "", house_number = "", postcode = "", city = ""):
        _lastname = lastname
        _name = name
        _company = company
        _street = street
        _house_number = house_number
        _postcode = postcode
        _city = city
        
        if _lastname == "": _lastname = self.name
        if _name == "": _name = self.name
        if _company == "": _company = self.company
        if _street == "": _street = self._street
        if _house_number == "": _house_number = self._house_number
        if _postcode == "": _postcode = self._postcode
        if _city == "": _city = self._city
        
        _customer_csv = Path("./Datenbanken/kunden.csv")
        _temp_customer_csv = Path("./Datenbanken/kunden_temp.csv")
        _exists = _customer_csv.exists()
        if _exists:
            with open(_customer_csv, "r") as input_file, open(_temp_customer_csv, "w") as output_file:
                lines = input_file.readlines()
                for line in lines:
                    if line.strip("\n") != f"{self.customer_id};{self.name};{self.name};{self.company};{self._street};{self._house_number};{self._postcode};{self._city}":
                        output_file.write(line)
                    else:
                        output_file.write(f"{self.customer_id};{_lastname};{_name};{_company};{_street};{_house_number};{_postcode};{_city}\n")

            os.remove("./Datenbanken/kunden.csv")
            _temp_customer_csv.rename("./Datenbanken/kunden.csv")
                
    def delete_customer_from_csv(self):
        _customer_csv = Path("./Datenbanken/kunden.csv")
        _temp_customer_csv = Path("./Datenbanken/kunden_temp.csv")
        _exists = _customer_csv.exists()
        if _exists:
            with open(_customer_csv, "r") as input_csv_file, open(_temp_customer_csv, "w") as output_csv_file:
                lines = input_csv_file.readlines()
                for line in lines:
                    if line.strip("\n") != f"{self.customer_id};{self.lastname};{self.name};{self.company};{self._street};{self._house_number};{self._postcode};{self._city}":
                        output_csv_file.write(line)
            os.remove("./Datenbanken/kunden.csv")
            _temp_customer_csv.rename("./Datenbanken/kunden.csv")
            
    
    def __repr__(self):
        # return repr((self.customer_id, self.lastname, self.name, self.company, self._street, self._house_number, self._postcode, self._city))
        return repr((self.customer_id))
    
        
    def __str__(self):
        # return f"Kunde {self.customer_id}: {self.company}, Kontakt: {self.lastname}, {self.name}"
        return f"{self.customer_id}"