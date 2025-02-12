from pathlib import Path
import os


class User:
    '''Data class for user objects'''
    _user_id_set = set()
    _user_number_counter = 0
    def __init__(self, lastname: str, firstname: str, username_hash: str, password_hash: str, user_id: int = 0):
        self.user_id = user_id

        self.lastname = lastname
        self.firstname = firstname
        self.username_hash = username_hash
        self.password_hash = password_hash

        if user_id == 0:
            User._user_number_counter += 1
            self.user_id = User._user_number_counter
            User._user_id_set.add(self.user_id)

        elif user_id == -1:
            User._user_number_counter += 1
            self.user_id = self._user_number_counter
            self._user_id_set.add(1)

        else:
            _user_id = user_id
            if not User._user_id_set.__contains__(_user_id):
                User._user_id_set.add(_user_id)
                if User._user_number_counter < _user_id:
                    User._user_number_counter = _user_id

            self.user_id = _user_id

    def save_user_to_csv(self):
        '''Method to save user data to a csv file'''
        _user_csv = Path("./Datenbanken/user.csv")
        _user_csv_exists = _user_csv.exists()
        _folder = Path("./Datenbanken")
        _folder_exists = _folder.exists()

        if _user_csv_exists:
            with open(_user_csv, "a", encoding="UTF-8") as file:
                file.write(f"{self.user_id};{self.lastname};{self.firstname};{self.username_hash};{self.password_hash}\n")

        else:
            if not _folder_exists:
                os.mkdir("./Datenbanken/")

            with open(_user_csv, "w", encoding="UTF-8") as file:
                file.write("Userid;Name;Vorname;Benutzernamen(hashed);Passwort(hashed)\n")
                file.write(f"{self.user_id};{self.lastname};{self.firstname};{self.username_hash};{self.password_hash}\n")

    def update_user_in_csv(self):
        '''Method to update the user data in the csv file'''
        # TODO:

    def reset_password(self, old_password_hash: str, new_password_hash: str):
        '''Method to change the password of a registered user'''
        if old_password_hash != self.password_hash:
            print("        Falsches Passwort!")
        elif old_password_hash == self.password_hash:
            self.password_hash = new_password_hash
            print("        Passwort neu gesetzt!")

    def delete_user_from_csv(self):
        '''Method to delete the user data from the csv file'''
        # TODO:

    def output_print(self):
        '''Method to print out the user data to the console'''
        return f"{self.user_id};{self.lastname};{self.firstname}"

    def admin_output_print(self):
        '''Method to print out the user data for admins to the console'''
        return f"{self.user_id};{self.lastname};{self.firstname};{self.username_hash};{self.password_hash}"

    def __repr__(self):
        return repr((self.user_id))

    def __str__(self):
        return f"{self.user_id}"
