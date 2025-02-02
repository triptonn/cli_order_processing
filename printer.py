import os
import platform


class Printer:
    def clear_cli():
        _platform = platform.system()
        if _platform == "Linus":
            os.system("clear")
            
        elif _platform == "Windows":
            os.system("cls")