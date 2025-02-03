import os
import platform


class Printer:
    def __init__(self, **message: str):
        lines = []
        
        for line in lines:
            print(line, sep=" ", end="\n")
    
    def clear_cli():
        _platform = platform.system()
        if _platform == "Linus":
            os.system("clear")
            
        elif _platform == "Windows":
            os.system("cls")