from tools import *
import flet
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
    mc = Laptop()
    lio = Programmer()
    lio.work(mc)
    sl()
