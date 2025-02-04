

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
        
        if _menu_item == "4":
            _user_management = False
        else:
            print("        Ungültige Eingabe, bitte versuchen Sie es erneut")