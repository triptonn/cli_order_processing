from pathlib import Path
from hashlib import blake2b 
import getpass
from os import urandom
from os import mkdir

import user_management


KEY = b'Thisisanexamplekey'


class AuthenticatedUser:
    def __init__(self, username_hash: str, password_hash):
        _super_hash = hash(username_hash * password_hash)
        
class Authenticator:
    _salt = None
    _id_counter = 0

    def __init__(self, username: str, user_cache: user_management.UserCache):
        self._username = username
        self._key = KEY
        _path = Path("./.secrets/hashing.csv")
        _path_exists = _path.exists()

        if self._salt == None and not _path_exists:
            print("        First time authenticator init")
            self._id_counter += 1
            
            _directory_path = Path("./.secrets/")
            _directory_path_exists = _directory_path.exists()
            
            _salt = urandom(16)
            print(_salt, type(_salt), len(_salt))
            self._salt = _salt
            print(_salt)

            if not _directory_path_exists:
                mkdir(_directory_path)

            with open(_path, "x") as file:
                file.write("setting_no;name;value\n")
                file.write(f"{self._id_counter};salt;{_salt.hex()}\n")
                self._id_counter += 1
                file.write(f"{self._id_counter};key;{self._key.hex()}\n")
            
            _sec_hash_provider = blake2b(key=self._key, salt=self._salt, person=bytes(self._username))
            self._sec_hash_provider = _sec_hash_provider
               
            

        elif self._salt == None and _path_exists:
            print("        Authenticator init, reading from hashing.csv")
            with open(_path, "r") as file:
                lines = file.readlines()
                lines.pop(0)
                for line in lines:
                    _prep_line = line.strip("\n")
                    _str = _prep_line.split(";")
                    if _str.__contains__("salt"):
                        print("Now processing salt", self._salt)
                        self._salt = bytes.fromhex(_str[1])
                        _sec_hash_provider = blake2b(salt=self._salt)
                        self._sec_hash_provider = _sec_hash_provider
                    elif _str.__cotains__("key"):
                        print("Now processing key")
                        pass

        else:
            print("        Authenticator init, already initialized")
            pass


    def set_username(self, user_id: int = 0):
        _username = getpass.getpass("        Benutzernamen vergeben (Achtung! Doppelte Eingabe notwendig): ")
        _username_set = False
        _username_equal = False
        while not _username_set:
            while not _username_equal:
                _username_control = getpass.getpass("        Erneut eingeben: ")
                if _username == _username_control:
                    _username_set = True
                    _username_equal = True      
                    return 
                elif _username_control == "abbruch":
                    break

    def set_password(self, user_id: int = 0):
        if user_id == -1:
            _password = getpass.getpass("        Erster Login :-) Wilkommen! Bitte ändere das 'admin' Passwort!\n        (Auchtung, das Passwort muss gleich noch einmal eingegeben werden!) \n        Passwort: ")
        else:
            _password = getpass.getpass("        Passwortänderung! (Achtung! Doppelte Eingabe notwendig): ")

        _password_set = False
        _password_equal = False
        while not _password_set:
            while not _password_equal:
                _password_control = getpass.getpass("        Erneut eingeben ('abbruch' um es neu zu versuchen): ")
                if _password == _password_control:
                    _password_set = True
                    _password_equal = True
                    return hash(_password)
                elif _password_control == "abbruch":
                    break