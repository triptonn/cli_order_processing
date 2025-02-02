import main
import printer


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

    while True:
        printer.Printer.clear_cli()
        print(_menu_string)
        
        _menu_item = input("        Bitte wählen Sie den gewünschen Menüpunkt:\n")
        
        if _menu_item == "4":
            main.main_menu_loop()
        else:
            print("        Ungültige Eingabe, bitte versuchen Sie es erneut")