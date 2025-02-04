class UserCache:
    _user_cache = set()
    
    def __init__(self):
        _prep_user_list= []
        
    def find_user_id(self, search_str: str):
        pass
    
    def get_user(self, user_id: int):
        pass
    
    def print_user_db(self):
        pass
    
    def add_user_to_cache(self):
        pass
    
    def update_cached_user(self):
        pass
    
    def remove_cached_user(self):
        pass

    def __iter__(self):
        for _user in self._user_cache:
            return _user

    def __str__(self):
        return f"{self._user_cache}"


class UserDBException(Exception):
    "A base class for UserDBExceptions"
    
class UserNotFoundException(UserDBException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.custom_kwarg = kwargs.get('custom_kwarg')


def user_management_menu_loop():
    _menu_string = """"
        ##########################################################################################################
        Benutzerverwaltung
        Menü:
        1. Benutzer anlegen
        2. Benutzer bearbeiten
        3. Benutzer löschen
        4. Benutzerliste ausgeben
        5. Zurück zum Hauptmenü
        ##########################################################################################################
    """


    # printer.Printer.clear_cli()
    _user_management = True
    while _user_management == True:
        print(_menu_string)
        
        _menu_item = input("        Bitte wählen Sie den gewünschen Menüpunkt:\n")
        if _menu_item == "1":
            pass
        elif _menu_item == "2":
            pass
        elif _menu_item == "3":
            pass
        elif _menu_item == "4":
            pass
        elif _menu_item == "5":
            _user_management = False
        else:
            print("        Ungültige Eingabe, bitte versuchen Sie es erneut")