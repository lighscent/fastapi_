# import sys
# from pathlib import Path

# # Ajoute automatiquement la racine du projet (fastapi) au sys.path
# ROOT = Path(__file__).resolve().parents[2]  # remonte 2 niveaux
# sys.path.insert(0, str(ROOT))

# import bootstrap
from tools import sl, cls

class Student:
    def __init__(self):
        self.__course = "Programming"
        self.tech = "Python"

    def get_course(self):
        return self.__course

    def set_course(self, course):
        self.__course = course

    def informations(self):
        return f"Course: {self.__course}\nTech: {self.tech}\n{'-'*55}"


student = Student()
print(
    student._Student__course
)  # Permet de frorcer l'accès à une var privée, mais ce n'est pas recommandé
print(student.get_course())
print(student.informations())

sl()

student.set_course('System')
print(student._Student__course)
print(student.informations())
