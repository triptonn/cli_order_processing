from pathlib import Path
import os


class User:
    _user_id_set = set()
    _user_number_counter = 0
    def __init__(self, lastname: str, firstname: str, username_hash: str, password_hash: str, user_id: int = 0):
        self._user_id = user_id

        self._lastname = lastname
        self._firstname = firstname
        self.username_hash = username_hash
        self.password_hash = password_hash

        if user_id == 0:
            User._user_number_counter += 1
            self._user_id = User._user_number_counter
            User._user_id_set.add(self._user_id)

        elif user_id == -1:
            User._user_number_counter += 1
            self._user_id = self._user_number_counter
            self._user_id_set.add(1)

        else:
            _user_id = user_id
            if not User._user_id_set.__contains__(_user_id):
                User._user_id_set.add(_user_id)
                if User._user_number_counter < _user_id:
                    User._user_number_counter = _user_id

            self._user_id = _user_id
        
    def save_user_to_csv(self):
        _user_csv = Path("./Datenbanken/user.csv")
        _user_csv_exists = _user_csv.exists()
        _folder = Path("./Datenbanken")
        _folder_exists = _folder.exists()
        
        if _user_csv_exists:
            with open(_user_csv, "a") as file:
                file.write(f"{self._user_id};{self._lastname};{self._firstname};{self.username_hash};{self.password_hash}\n")

        else:
            if not _folder_exists:
                os.mkdir("./Datenbanken/")

            with open(_user_csv, "w") as file:
                file.write("Userid;Name;Vorname;Benutzernamen(hashed);Passwort(hashed)\n")
                file.write(f"{self._user_id};{self._lastname};{self._firstname};{self.username_hash};{self.password_hash}\n")
                
    def update_user_in_csv(self):
        # TODO:
        pass
    
    def reset_password(self, old_password_hash: str, new_password_hash: str):
        if old_password_hash != self.password_hash:
            print("        Falsches Passwort!")
        elif old_password_hash == self.password_hash:
            self.password_hash = new_password_hash
            print("        Passwort neu gesetzt!")
    
    def delete_user_from_csv(self):
        # TODO:
        pass
    
    def output_print(self):
        return f"{self._user_id};{self._lastname};{self._firstname}"
    
    def admin_output_print(self):
        return f"{self._user_id};{self._lastname};{self._firstname};{self.username_hash};{self.password_hash}"
    
    def __repr__(self):
        return repr((self._user_id))
    
    def __str__(self):
        return f"{self._user_id}"