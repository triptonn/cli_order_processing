from pathlib import Path
from hashlib import blake2b 
import getpass

class AuthenticatedUser:
    def __init__(self, username_hash: str, password_hash):
        _super_hash = hash(username_hash * password_hash)
        print(f"{_super_hash}")
        
        
class Authenticator:
    _secret_salt = None

    def __init__(self):
        _path = Path("./.secrets/hashing.csv")        

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