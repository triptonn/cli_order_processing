import getpass
import copy

import authentication
import order_processing
import customer_management 
import user_management
import user


class MainMenu:
    def __init__(self):
        self._initialized = False

    def main_menu_loop(self, user_cache: user_management.UserCache):
        if self._initialized == False:
            
            customer_cache = customer_management.CustomerCache()
            item_cache = order_processing.ItemCache()
            order_cache = order_processing.OrderCache(item_cache, customer_cache)
            self._initialized = True

        menu_text = """
            ##########################################################################################################
            Herzlich Wilkommen
            Menü:
            1. Auftragsbearbeitung
            2. Kundendatenbank
            3. Benutzerverwaltung
            4. Programm beenden
            ##########################################################################################################
        """

        #printer.Printer.clear_cli()
        while True:
            print(menu_text)

            _menu_item = input("Bitte wählen Sie den gewünschten Menüpunkt.\n")

            if _menu_item == "1":
                order_processing.order_processing_menu_loop(customer_cache, order_cache, item_cache)

            if _menu_item == "2":
                customer_management.customer_management_loop(customer_cache)

            if _menu_item == "3":
                user_management.user_management_menu_loop(user_cache)

            if _menu_item == "4":
                print("Das Programm wird beendet!")
                quit()
            else:
                print("Ungültige Eingabe, bitte versuchen Sie es erneut!")
                
class LoginMenu:
    _logged_in = False
    _authenticator = None

    def __init__(self, user_cache: user_management.UserCache):
        self._user_cache = user_cache

        # on first login
        if len(user_cache.user_cache) == 0:
            _lastname = "Doe"
            _name = "John"
            _username = "admin"
            _initial_password = "12345678"
            _admin_otp = -1

            self._authenticator = authentication.Authenticator(_username, user_cache)

            _admin = user.User(_lastname, _name, _username, _initial_password, _admin_otp)
           
        # on subsequent logins



    def login(self):
        while self._logged_in == False:
            _username = getpass.getpass("        Benutzername: ")
            _password = getpass.getpass("        Passwort: ")
            
            for _user in self._user_cache.user_cache:
                assert type(_user) is user.User
                
                _user.username_hash                

                print(_user, type(_user))

                print(f"saved username_hash: {_user.username_hash} == {hash(_username)}\nsaved password_hash: {_user.password_hash} == {hash(_password)}\nresult: {_user.username_hash == hash(_username) and _user.password_hash == hash(_password)}")
                if _user.username_hash == hash(_username) and _user.password_hash == hash(_password):
                    self._logged_in = True
                    return authentication.AuthenticatedUser(hash(_username), hash(_password))        
    

if __name__ == "__main__":
    user_cache = user_management.UserCache()
    
    # DEBUG: comment these three lines to deactivate login
    # login_menu = LoginMenu(user_cache)
    # _authenticated_user = login_menu.login() 

    # menu = MainMenu(_authenticated_user)
    menu = MainMenu()
    menu.main_menu_loop(user_cache)
    