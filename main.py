import getpass
import copy

import authenticator
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
        self._authenticator = authenticator.Authenticator()
        self._user_cache = user_cache
        

        # on first login
        if len(user_cache.user_cache) == 0:
            _name_admin = "admin"
            _initial_pw = "12345678"
            _admin_otp = -1

            _admin = user.User("admin", "admin", _name_admin, _initial_pw, 1)
            user_cache.add_user_to_cache(_admin)
            
            _password_reset = False
            while not _password_reset:
                _new_password_hash = authenticator.Authenticator.set_password(_admin_otp)
                if _new_password_hash == None:
                    pass
                else:
                    _old_admin = copy.copy(_admin)
                    _admin.reset_password(hash(_initial_pw), _new_password_hash)
                    print("        'admin' Benutzerpasswort neu vergeben! Bitte gut verwahren!")
                    _admin.save_user_to_csv()
                    user_cache.update_cached_user(_old_admin, _admin)
                    _passwort_reset = True

    def login(self):
        while self._logged_in == False:
            _username = getpass.getpass("        Benutzername: ")
            _password = getpass.getpass("        Passwort: ")
            
            print(_username, _password)
            
            
            
            print(f"self._user_cache is not User type: ", self._user_cache, type(self._user_cache), self._user_cache.user_cache, type(self._user_cache.user_cache))
            for _user in self._user_cache.user_cache:
                assert type(_user) is user.User
                
                _user.username_hash                

                print(_user, type(_user))

                print(f"saved username_hash: {_user.username_hash} == {hash(_username)}\nsaved password_hash: {_user.password_hash} == {hash(_password)}\nresult: {_user.username_hash == hash(_username) and _user.password_hash == hash(_password)}")
                if _user.username_hash == hash(_username) and _user.password_hash == hash(_password):
                    self._logged_in = True
                    return authenticator.AuthenticatedUser(hash(_username), hash(_password))        
    

if __name__ == "__main__":
    _user_cache = user_management.UserCache()
    
    # DEBUG: comment these three lines to deactivate login
    # print(hash(_user_cache))
    # login_menu = LoginMenu(_user_cache)
    # _authenticated_user = login_menu.login() 
    # menu = MainMenu(_authenticated_user)

    menu = MainMenu()
    print(hash(_user_cache))
    menu.main_menu_loop(_user_cache)
    