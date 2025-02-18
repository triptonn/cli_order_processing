"""Main module of the application"""

import getpass

import authentication
import order_processing
import customer_management
import user_management
import user_repository
import printer


class MainMenu:
    """Class containing the main menu loop"""

    customer_cache = None
    item_cache = None
    position_cache = None
    order_cache = None

    def __init__(self, authenticated_user: authentication.AuthenticatedUser):
        self._initialized = False
        self._authenticated_user = authenticated_user

    def main_menu_loop(self, _user_cache: user_management.UserCache):
        """Method implementing the main menu loop"""

        if self._initialized is False:
            self.customer_cache = customer_management.CustomerCache()
            self.item_cache = order_processing.ItemCache()
            self.position_cache = order_processing.PositionCache(
                self.item_cache,
            )
            self.order_cache = order_processing.OrderCache(
                self.item_cache,
                self.position_cache,
                self.customer_cache,
            )
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

        while True:
            print(menu_text)

            _menu_item = input("        Bitte wählen Sie den gewünschten Menüpunkt: ")

            if _menu_item == "1":
                order_processing.order_processing_menu_loop(
                    self.customer_cache, self.order_cache, self.item_cache
                )

            elif _menu_item == "2":
                customer_management.customer_management_loop(self.customer_cache)

            elif _menu_item == "3":
                user_management.user_management_menu_loop(
                    _user_cache, self._authenticated_user
                )

            elif _menu_item == "4":
                print("        Das Programm wird beendet!")
                quit()

            elif _menu_item == "c":
                printer.Printer.clear_cli()


class LoginMenu:
    """Class facilitating the login process"""

    _logged_in = False
    _authenticator = None
    _username_hash = None
    _password_hash = None

    def __init__(self, _user_cache: user_management.UserCache):
        self._user_cache = _user_cache

        if len(_user_cache.user_cache) == 0:
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

            _admin = user_repository.User(
                _lastname, _name, _username_hash.hex(), _password_hash.hex(), _admin_otp
            )
            _admin.save_user_to_csv()
            self._user_cache.add_user_to_cache(_admin)
            self._user = _admin

            self._logged_in = True
            _authenticated_user = self.get_authenticated_user()

            _menu = MainMenu(_authenticated_user)
            _menu.main_menu_loop(_user_cache)

        else:
            _user_exists = False
            while not _user_exists:
                printer.Printer.clear_cli()
                _username = getpass.getpass("        Benutzername: ")
                self._authenticator = authentication.Authenticator(_username)
                _username_hash = self._authenticator.custom_hash(_username)

                for _user in _user_cache.user_cache:
                    assert isinstance(_user, user_repository.User)
                    if _user.username_hash != _username_hash:
                        continue
                    else:
                        print("        ... User existiert!")
                        self._username_hash = _username_hash
                        _user_exists = True

                    while self._logged_in is False:
                        _password = getpass.getpass("        Passwort: ")
                        _password_hash = self._authenticator.custom_hash(_password)
                        for _user in self._user_cache.user_cache:
                            assert isinstance(_user, user_repository.User)
                            if _user.password_hash == _password_hash:
                                print("        ... Passwort korrekt!")
                                self._user = _user
                                self._logged_in = True

                        if self._logged_in is True:
                            self._password_hash = _password_hash

    def get_authenticated_user(self):
        """Method to get the authenticated user object"""
        if self._logged_in is True:
            return authentication.AuthenticatedUser(
                self._user,
                self._username_hash,
                self._password_hash,
                self._authenticator,
            )
        return None


if __name__ == "__main__":
    user_cache = user_management.UserCache()

    login_menu = LoginMenu(user_cache)
    _authenticated_user = login_menu.get_authenticated_user()

    menu = MainMenu(_authenticated_user)
    printer.Printer.clear_cli()
    menu.main_menu_loop(user_cache)
