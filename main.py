import getpass

import authentication
import order_processing
import customer_management 
import user_management
import user
import printer


class MainMenu:
    def __init__(self, authenticated_user: authentication.AuthenticatedUser):
        self._initialized = False
        self._authenticated_user = authenticated_user
        
    def main_menu_loop(self, user_cache: user_management.UserCache):
        if self._initialized == False:
            customer_cache = customer_management.CustomerCache()
            item_cache = order_processing.ItemCache()
            order_cache = order_processing.OrderCache(item_cache, customer_cache)
            self._initialized = True

        menu_text = """
        ##########################################################################################################
        
        Herzlich Wilkommen
        
        Menü:                                                                          'c' um Bildschirm zu räumen
        1. Auftragsbearbeitung
        2. Kundendatenbank
        3. Benutzerverwaltung
        4. Programm beenden
        
        ##########################################################################################################
        """

        #printer.Printer.clear_cli()
        while True:
            print(menu_text)

            _menu_item = input("        Bitte wählen Sie den gewünschten Menüpunkt: ")

            if _menu_item == "1":
                order_processing.order_processing_menu_loop(customer_cache, order_cache, item_cache)

            elif _menu_item == "2":
                customer_management.customer_management_loop(customer_cache)

            elif _menu_item == "3":
                user_management.user_management_menu_loop(user_cache, self._authenticated_user)

            elif _menu_item == "4":
                print("        Das Programm wird beendet!")
                quit()
            
            elif _menu_item == "c":
                printer.Printer.clear_cli()            

                
class LoginMenu:
    _logged_in = False
    _authenticator = None
    _username_hash = None
    _password_hash = None

    def __init__(self, user_cache: user_management.UserCache):
        self._user_cache = user_cache

        if len(user_cache.user_cache) == 0:
            _lastname = "Doe"
            _name = "John"
            _username = "admin"
            _admin_otp = -1

            info_text = """
        ##########################################################################################################
        
        Herzlich Wilkommen
        
        Der User 'admin' wurde generiert. Zunächst muss ein Passwort gewählt werden...
                                                                                                              
        ##########################################################################################################
            """

            printer.Printer.clear_cli()

            print(info_text)

            self._authenticator = authentication.Authenticator(_username)
            _username_hash = self._authenticator.custom_hash(_username)
            self._username_hash = _username_hash
            
            _password = self._authenticator.set_password(_admin_otp)
            _password_hash = self._authenticator.custom_hash(_password)
            self._password_hash = _password_hash

            _admin = user.User(_lastname, _name, _username_hash.hex(), _password_hash.hex(), _admin_otp)
            _admin.save_user_to_csv()
            self._user_cache.add_user_to_cache(_admin)
            self._user = _admin
            
            
            self._logged_in = True
            _authenticated_user = self.get_authenticated_user()
            
            printer.Printer.clear_cli()

            menu = MainMenu(_authenticated_user)
            menu.main_menu_loop(user_cache)

        else:
            _user_exists = False
            while not _user_exists:
                printer.Printer.clear_cli()
                _username = getpass.getpass("        Benutzername: ")
                self._authenticator = authentication.Authenticator(_username)
                _username_hash = self._authenticator.custom_hash(_username)

                for _user in user_cache.user_cache:
                    assert type(_user) is user.User
                    if _user.username_hash != _username_hash:
                        continue 
                    else:
                        print("        ... User existiert!")
                        self._username_hash = _username_hash
                        _user_exists = True

                    # def login(self):
                    while self._logged_in == False:
                        _password = getpass.getpass("        Passwort: ")
                        _password_hash = self._authenticator.custom_hash(_password)
                        for _user in self._user_cache.user_cache:
                            assert type(_user) is user.User
                            if _user.password_hash == _password_hash:
                                print("        ... Passwort korrekt!")
                                self._user = _user
                                self._logged_in = True

                        if self._logged_in == True:
                            self._password_hash = _password_hash

    def get_authenticated_user(self):
        if self._logged_in == True:
            return authentication.AuthenticatedUser(self._user, self._username_hash, self._password_hash, self._authenticator)


if __name__ == "__main__":
    user_cache = user_management.UserCache()
    
    login_menu = LoginMenu(user_cache)
    _authenticated_user = login_menu.get_authenticated_user() 

    menu = MainMenu(_authenticated_user)
    printer.Printer.clear_cli()
    menu.main_menu_loop(user_cache)
    