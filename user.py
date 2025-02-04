from pathlib import Path
import os

class User:
    _user_id_set = set()
    _user_number_counter = 0
    def __init__(self, lastname: str, firstname: str, username: str, password: str, user_id: int = 0):
        self._user_id = user_id
        if user_id == 0:
            User._user_number_counter += 1
            self._user_id = User._user_number_counter
            User._user_id_set.add(self._user_id)
        else:
            _user_id = user_id
            if not User._user_id_set.__contains__(_user_id):
                User._user_id_set.add(_user_id)
                if User._user_number_counter < _user_id:
                    User._user_number_counter = _user_id
            self._user_id = _user_id

        self._lastname = lastname
        self._firstname = firstname
        self._username_hash = hash(username)
        self._password_hash = hash(password)
        
    def save_user_to_csv(self):
        _user_csv = Path("./Datenbanken/user.csv")
        _user_csv_exists = _user_csv.exists()
        _folder = Path("./Datenbanken")
        _folder_exists = _folder.exists()
        
        if _user_csv_exists:
            with open(_user_csv, "a") as file:
                file.write(f"{self._user_id};{self._lastname};{self._firstname};{self._username_hash};{self._password_hash}")

        else:
            if not _folder_exists:
                os.mkdir("./Datenbanken/")

            with open(_user_csv, "w") as file:
                file.write("Userid;Name;Vorname;Benutzernamen(hashed);Passwort(hashed)")
                file.write(f"{self._user_id};{self._lastname};{self._firstname};{self._username_hash};{self._password_hash}")
                
    def update_user_in_csv(self):
        pass
    
    def delete_user_from_csv(self):
        pass
    
    def __repr__(self):
        return repr((self._user_id))
    
    def __str__(self):
        return f"{self._user_id}"