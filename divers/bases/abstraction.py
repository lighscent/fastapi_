# import sys
# from pathlib import Path
# Ajoute le dossier parent "fastapi" au sys.path
# BASE_DIR = Path(__file__).resolve().parents[2]   # remonte 2 niveaux
# sys.path.append(str(BASE_DIR))

# OU

# Copier 1 seule fois D:\c2\fastapi\tools\sitecustomize.py
# (Lire instructions dedans)

from tools import *
from abc import ABC, abstractmethod


class Computer(ABC):
    """Abstract class car contient au moins une abstract method"""

    @abstractmethod
    def process(self):
        pass


class Laptop(Computer):
    def process(self):
        print("Laptop is running...")
        # pass


class Programmer:
    def work(self, tool):
        print("Solving problems by programming...")
        tool.process()


if __name__ == "__main__":
    
    cls()
    print ('\nScript abstraction.py')
    mc = Laptop()
    lio = Programmer()
    sl()
    lio.work(mc)
    
    sl()
