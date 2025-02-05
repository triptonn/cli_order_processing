from pathlib import Path
import copy

import authentication
import user


class UserCache:
    user_cache = set()
    
    def __init__(self):
        _prep_user_list= []
        _path = Path("./Datenbanken/user.csv")
        _user_csv_exists = _path.exists()
        if _user_csv_exists:
            try:
                with open(_path, "r") as _userdb:
                    lines = _userdb.readlines()
                    lines.pop(0)
                    for line in lines:
                        _prep_user_list.append(line.strip("\n"))
                        
                    for _listed_user in _prep_user_list:
                        _prep_user = str.split(_listed_user, sep=";")
                        _user_id_exists = user.User._user_id_set.__contains__(int(_prep_user[0]))
                        _user = user.User(_prep_user[1],_prep_user[2],_prep_user[3],_prep_user[4],int(_prep_user[0]))
                        if not _user_id_exists:
                            print(f"DEBUG: User {_user.admin_output_print()} added to cache")
                            self.user_cache.add(_user)
                        else:
                            raise UserIDException(str(_user), "User ID ist bereits vergeben!")
                        
            except UserIDException as exc:
                print(f"Caught UserIDException with custom_kwarg={exc.custom_kwarg}")
        
    def find_user_id(self, search_str: str):
        _search_str = copy.copy(search_str)
        _possible_hits = []
        for u in self.user_cache:
            assert type(u) is user.User

            if u._firstname.find(_search_str) >= 0:
                _possible_hits.append[u]
                
            if u._lastname.find(_search_str) >= 0:
                _possible_hits.append[u]
                
        for h in _possible_hits:
            assert type(h) is user.User
            print(h)
                
    def get_user(self, user_id: int):
        try:
            for _user in self.user_cache:
                assert type(_user) is user.User
                if user_id == _user._user_id:
                    return copy.copy(_user)
            else: raise UserNotFoundException(f"User {user_id} not found in cache!")
        except UserNotFoundException as exc:
            print(f"DEBUG: _user_cache: {self.user_cache}, {type(self.user_cache)}")
        return None
    

    def print_user_db(self):
        for _user in self.user_cache:
            assert type(_user) is user.User
        _user_tuple = tuple(self.user_cache)
        
        _user_list = sorted(_user_tuple, key=lambda user: user._user_id)
        for _user in _user_list:
            assert type(_user) is user.User
            print(_user.output_print())
    
    def add_user_to_cache(self, user: user.User):
        self.user_cache.add(user)
    
    def update_cached_user(self, old: user.User, new: user.User):
        self.user_cache.remove(old)
        self.user_cache.add(new)
    
    def remove_cached_user(self, user: user.User):
        self.user_cache.remove(user)

    def __iter__(self):
        for _user in self.user_cache:
            return _user

    def __str__(self):
        return f"{self.user_cache}"


class UserDBException(Exception):
    "A base class for UserDBExceptions"
    
class UserNotFoundException(UserDBException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.custom_kwarg = kwargs.get('custom_kwarg')
        
class UserIDException(UserDBException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.custom_kwarg = kwargs.get('custom_kwarg')


def user_management_menu_loop(user_cache: UserCache):
    _menu_string = """
        ##########################################################################################################
        Benutzerverwaltung
        Menü:
        1. Benutzer anlegen
        2. Benutzer bearbeiten
        3. Benutzer löschen
        4. Benutzerliste ausgeben
        5. Benutzernummer finden
        6. Zurück zum Hauptmenü
        ##########################################################################################################
    """


    # printer.Printer.clear_cli()
    _user_management = True
    while _user_management == True:
        print(_menu_string)
        
        _menu_item = input("        Bitte wählen Sie den gewünschen Menüpunkt: ")
        if _menu_item == "1":
            _lastname = input("        Nachname: ")
            _name = input("        Vorname: ")
            
            _user_name_hash = authentication.Authenticator.set_username() 
            _password_hash = authentication.Authenticator.set_password()
                    
            _user = user.User(_lastname, _name, _user_name_hash, _password_hash)
            _user.save_user_to_csv()
            user_cache.add_user_to_cache(_user)

        elif _menu_item == "2":
            pass
        elif _menu_item == "3":
            pass
        elif _menu_item == "4":
            user_cache.print_user_db()

        elif _menu_item == "5":
            pass
        elif _menu_item == "6":
            _user_management = False
        else:
            print("        Ungültige Eingabe, bitte versuchen Sie es erneut")