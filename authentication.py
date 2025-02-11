from pathlib import Path
import getpass
from os import urandom
from os import mkdir

import scrypt

import user_repository
import printer


class Authenticator:
    '''Class managing authentication to the application'''

    _username = None
    _salt = None
    _N = 8
    _p = 323
    _r = 627
    _id_counter = 0

    def __init__(self, username: str):
        self._username = username
        _path = Path("./.secrets/hashing.csv")
        _path_exists = _path.exists()

        if self._salt is None and not _path_exists:
            self._id_counter += 1

            _directory_path = Path("./.secrets/")
            _directory_path_exists = _directory_path.exists()

            _salt = urandom(16)
            self._salt = _salt

            if not _directory_path_exists:
                mkdir(_directory_path)

            with open(_path, "x", encoding="UTF-8") as file:
                file.write("setting_no;name;value\n")
                file.write(f"{self._id_counter};salt;{_salt.hex()}\n")


        elif self._salt is None and _path_exists:
            with open(_path, "r", encoding="UTF-8") as file:
                lines = file.readlines()
                lines.pop(0)
                for line in lines:
                    _prep_line = line.strip("\n")
                    _str = _prep_line.split(";")
                    if _str.__contains__("salt"):
                        self._salt = bytes.fromhex(_str[2])


    def custom_hash(self, value: str):
        '''Method using to create custom hash values for passwords using scrypt'''
        assert isinstance(value, str)
        _hashed_value =  scrypt.hash(password=value, salt=self._salt + str.encode(self._username), N=self._N, r=self._r, p=self._p)
        return _hashed_value

    def set_username(self):
        '''Method used to create the username for a new user'''

        _username = getpass.getpass("        Benutzernamen vergeben: ")
        _username_set = False
        _username_equal = False

        while not _username_set:
            print("        Um den Versuch abzubrechen tippe 'abbruch'...")
            while not _username_equal:
                _username_control = getpass.getpass("        Benutzernamen erneut eingeben: ")
                _username_set = True
                if _username == _username_control:
                    _username_equal = True
                    return _username
                elif _username_control == "abbruch":
                    break
                printer.Printer.clear_cli()

    def set_password(self, user_id: int = 0):
        '''Method used to create or reset the password for user'''
        if user_id == -1:
            _password = getpass.getpass("        Erster Login :-) Wilkommen! Bitte vergib das 'admin' Passwort: ")
        elif user_id > 0:
            _password = getpass.getpass(f"        Das neue Passwort für den Benutzer {user_id} lautet: ")
        else:
            _password = getpass.getpass("        Wähle ein Passwort für den neuen Benutzer: ")

        _password_set = False
        _password_equal = False
        while not _password_set:
            print("        Um den Versuch abzubrechen tippe 'abbruch'...")
            while not _password_equal:
                _password_control = getpass.getpass("        Passwort erneut eingeben: ")
                _password_set = True
                if _password == _password_control:
                    print("        Passwortvergabe erfolgreich!")
                    _password_equal = True
                    return _password
                elif _password_control == "abbruch":
                    break
                printer.Printer.clear_cli()


class AuthenticatedUser:
    '''Class to carry authentication state and information to the granted access rights for the authenticated user'''

    _random_key = urandom(32)
    _salt = urandom(16)
    _N = 4
    _p = 236
    _r = 678

    def __init__(self, user: user_repository.User, username_hash: bytes, password_hash: bytes, authenticator: Authenticator):
        self._user = user
        self._user_key = username_hash[32:]
        self._authenticator = authenticator

        self._super_hash = scrypt.hash(self._random_key + password_hash, self._salt, N=self._N, p=self._p, r=self._r, buflen=32)

    # TODO: this object will carry the user rights granted to the user when the user is authenticated
