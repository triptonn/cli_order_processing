"""Module holding customer class"""

import os
from pathlib import Path


class Customer:
    """
    Data class of the Customer object

    Attributes
    ----------
    customer_id : int
        Unique identifier
    lastname : str
        Lastname of contact
    name : str
        Firstname of contact
    company : str
        Company name
    street : str
        Street name
    house_number : str
        House number
    postcode : str
        Postcode
    city : str
        City
    """

    customer_id_set = set()
    _customer_id_counter = 0

    def __init__(
        self,
        lastname: str,
        name: str,
        company: str,
        street: str,
        house_number: str,
        postcode: str,
        city: str,
        customer_id: int = 0,
    ):
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
        self.street = street
        self.house_number = house_number
        self.postcode = postcode
        self.city = city

    def print_address(self):
        """Method prints information about the customer to the screen"""
        _str = (
            f"Kunde: {self.customer_id}: {self.street} "
            f"{self.house_number}, {self.postcode} {self.city}"
        )
        return _str

    def save_customer_to_csv(self):
        """Saves customer object information as string to csv file"""
        _customer_csv = Path("./Datenbanken/kunden.csv")
        _exists = _customer_csv.exists()

        if _exists:
            with open(_customer_csv, "a", encoding="UTF-8") as file:
                file.write(
                    f"{self.customer_id};"
                    f"{self.name};"
                    f"{self.name};"
                    f"{self.company};"
                    f"{self.street};"
                    f"{self.house_number};"
                    f"{self.postcode};"
                    f"{self.city}\n"
                )
        else:
            os.mkdir("./Datenbanken/")
            with open(_customer_csv, "w", encoding="UTF-8") as file:
                file.write(
                    "Kundennummer;Name;Vorname;Firma;Strasse;Hausnummer;Postleitzahl;Ort\n"
                )
                file.write(
                    f"{self.customer_id};{self.name};{self.name};{self.company};{self.street};{self.house_number};{self.postcode};{self.city}\n"
                )

    def update_customer_in_csv(
        self,
        lastname="",
        name="",
        company="",
        street="",
        house_number="",
        postcode="",
        city="",
    ):
        _lastname = lastname
        _name = name
        _company = company
        _street = street
        _house_number = house_number
        _postcode = postcode
        _city = city

        if _lastname == "":
            _lastname = self.name
        if _name == "":
            _name = self.name
        if _company == "":
            _company = self.company
        if _street == "":
            _street = self.street
        if _house_number == "":
            _house_number = self.house_number
        if _postcode == "":
            _postcode = self.postcode
        if _city == "":
            _city = self.city

        _customer_csv = Path("./Datenbanken/kunden.csv")
        _temp_customer_csv = Path("./Datenbanken/kunden_temp.csv")
        _exists = _customer_csv.exists()
        if _exists:
            with open(_customer_csv, "r", encoding="UTF-8") as input_file, open(
                _temp_customer_csv, "w", encoding="UTF-8"
            ) as output_file:
                lines = input_file.readlines()
                for line in lines:
                    if (
                        line.strip("\n")
                        != f"{self.customer_id};{self.name};{self.name};{self.company};{self.street};{self.house_number};{self.postcode};{self.city}"
                    ):
                        output_file.write(line)
                    else:
                        output_file.write(
                            f"{self.customer_id};{_lastname};{_name};{_company};{_street};{_house_number};{_postcode};{_city}\n"
                        )

            os.remove("./Datenbanken/kunden.csv")
            _temp_customer_csv.rename("./Datenbanken/kunden.csv")

    def delete_customer_from_csv(self):
        _customer_csv = Path("./Datenbanken/kunden.csv")
        _temp_customer_csv = Path("./Datenbanken/kunden_temp.csv")
        _exists = _customer_csv.exists()
        if _exists:
            with open(_customer_csv, "r", encoding="UTF-8") as input_csv_file, open(
                _temp_customer_csv, "w", encoding="UTF-8"
            ) as output_csv_file:
                lines = input_csv_file.readlines()
                for line in lines:
                    if (
                        line.strip("\n")
                        != f"{self.customer_id};{self.lastname};{self.name};{self.company};{self.street};{self.house_number};{self.postcode};{self.city}"
                    ):
                        output_csv_file.write(line)
            os.remove("./Datenbanken/kunden.csv")
            _temp_customer_csv.rename("./Datenbanken/kunden.csv")

    def output_print(self):
        return f"{self.customer_id};{self.lastname};{self.name};{self.company};{self.street};{self.house_number};{self.postcode};{self.city}"

    def __repr__(self):
        # return repr((self.customer_id, self.lastname, self.name, self.company, self._street, self._house_number, self._postcode, self._city))
        return repr((self.customer_id))

    def __str__(self):
        # return f"Kunde {self.customer_id}: {self.company}, Kontakt: {self.lastname}, {self.name}"
        return f"{self.customer_id}"
