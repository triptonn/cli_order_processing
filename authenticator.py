from pathlib import Path
from hashlib import blake2b 
import hashlib
import getpass
from os import urandom
from os import mkdir

class AuthenticatedUser:
    def __init__(self, username_hash: str, password_hash):
        _super_hash = hash(username_hash * password_hash)
        print(f"{_super_hash}")
        
        
class Authenticator:
    _salt = None
    _id_counter = 0

    def __init__(self, id = 0):
        _path = Path("./.secrets/hashing.csv")
        _path_exists = _path.exists()

        if self._salt == None and not _path_exists:
            self._id_counter += 1
            
            _directory_path = Path("./.secrets/")
            _directory_path_exists = _directory_path.exists()
            
            _salt = urandom(16)
            self._salt = _salt

            if not _directory_path_exists:
                mkdir(_directory_path)

            with open(_path, "x") as file:
                file.write("setup_id;salt\n")
                file.write(f"{self._id_counter};{_salt.hex()}\n")

        elif self._salt == None and _path_exists:
            with open(_path, "r") as file:
                lines = file.readlines()
                lines.pop()
                for line in lines:
                    line.strip("\n")
                    _str = line.split(";")
                    print(_str)
        else:
            pass

        _sec_hash = blake2b(salt=self._salt)

        print(_sec_hash, type(_sec_hash))


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
                    return hash(_username)
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
                
                
                
_authenticator = Authenticator()
