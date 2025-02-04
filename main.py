import order_processing
import customer_management 
import user_management

class MainMenu:
    def __init__(self):
        self._initialized = False

    def main_menu_loop(self):
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
                user_management.user_management_menu_loop()

            if _menu_item == "4":
                print("Das Programm wird beendet!")
                quit()
            else:
                print("Ungültige Eingabe, bitte versuchen Sie es erneut!")

if __name__ == "__main__":
    menu = MainMenu()
    menu.main_menu_loop()
    