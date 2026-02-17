import flet
from tools import *


def duck_typing_example1():
    class Editor:

        def execute(self):
            print(f"Coding.")
            print(f"Debugging.")
            print(f"Compiling.")
            print(f"Inside my editor.")

    class VSC:

        def execute(self):
            print(f"Coding.")
            print(f"Debugging.")
            print(f"Compiling.")
            print(f"Inside my VSC.")

    class Laptop:
        def code(self, ide):
            ide.execute()

    writingtool1 = VSC()
    mc = Laptop()
    mc.code(writingtool1)
    print("-" * 55)
    writingtool2 = Editor()
    mc = Laptop()
    mc.code(writingtool2)


def duck_typing_example2():

    class Duck:
        def quack(self):
            print("Quack!")

    class Person:
        def quack(self):
            print("I'm pretending to be a duck!")

    def make_it_quack(duck):
        duck.quack()

    duck = Duck()
    person = Person()

    make_it_quack(duck)  # Output: Quack!
    make_it_quack(person)  # Output: I'm pretending to be a duck!


def operation_overloading_example():

    def add(a, b):

        try:
            return int(a) + int(b)
        except TypeError:
            raise TypeError(
                f"Unsupported types for my add() function :\n\n{a} ({type(a)}) + {b} ({type(b)}) isn't supported."
            )

    a = 5
    # a = [5] # Raise my error, because I can't convert a list to an int
    b = "7"
    # print(a+int(b)) # 12
    # print(a+b) # ERROR
    print(add(a, b))  # 12

    class Student:
        def __init__(self, m1, m2):
            self.m1 = m1
            self.m2 = m2

        # def greet(self, other):
        #     print(f"Hello, I'm {self.name}!")

        # À noter qu'il existe aussi:
        # __sub__(self, other) pour la soustraction
        # __mul__(self, other) pour la multiplication
        # __truediv__(self, other) pour la division
        # etc...
        def __add__(self, other):
            r1 = self.m1 + other.m1
            r2 = self.m2 + other.m2
            return Student(r1, r2)

        def __repr__(self):
            return f"Student({self.m1}, {self.m2})"

    s1 = Student(17, 13)
    s2 = Student(11, 14)

    # print(s1 + s2)  # ERROR, because I haven't defined how to add two Student objects
    print(s1 + s2)
    # print(s1.__add__(s2))


def method_overloading_example():

    def addition(a, b):
        return a + b

    def overloaded_addition(a=None, b=None, c=None):
        s = 0
        if a != None and b != None and c != None:
            s = a + b + c
        elif a != None and b != None:
            s = a + b
        else:
            s = a
        return s

    print(addition(3, 4))  # 7
    # print (addition(3, 4, 5)) # ERR
    print(overloaded_addition(3, 4))  # 7
    print(overloaded_addition(3, 4, 5))  # 12


def metho_overriding_example():

    class Animal:
        def speak(self):
            print("Animal speaks")

    class Dog(Animal):
        def speak(self):
            print("Woof!")

    class Cat(Animal):
        def speak(self):
            print("Meow!")

    animal = Animal()
    dog = Dog()
    cat = Cat()
    animal.speak()  # Output: Animal speaks
    dog.speak()  # Output: Woof!
    cat.speak()  # Output: Meow!


if __name__ == "__main__":
    w = 55
    cls()

    # DUCK TYPING
    # Python ne se soucie pas du type, tant que l’objet sait répondre à la méthode demandée.
    duck_typing_example1()
    sl(55)
    duck_typing_example2()
    print("-" * 55)

    sl(w)
    ## OPERATION OVERLOADING
    # C'est lorsque vous redéfinissez les opérateurs pour des types personnalisés. Par exemple, si vous avez une classe "Student" avec des attributs de note, vous pouvez redéfinir l'opérateur "+" pour permettre d'additionner les notes de deux étudiants. Cela permet d'utiliser des opérateurs de manière intuitive avec vos propres classes.
    operation_overloading_example()

    sl(w)
    ## METHOD OVERLOADING
    # C'est lorsque vous avez plusieurs méthodes avec le même nom mais des signatures différentes (différents types ou nombre d'arguments) dans la même classe. Cependant, Python ne supporte pas directement le method overloading comme certains autres langages, mais vous pouvez simuler ce comportement en utilisant des arguments par défaut ou en vérifiant les types d'arguments à l'intérieur de la méthode. Par exemple, si vous avez une méthode "add()" qui peut prendre soit deux entiers, soit deux chaînes de caractères, vous pouvez vérifier les types des arguments pour déterminer comment les traiter.
    method_overloading_example()

    sl(w)
    ## METHOD OVERRIDING
    # C'est lorsque vous redéfinissez une méthode dans une classe dérivée pour changer le comportement de la méthode héritée. Par exemple, si vous avez une classe de base "Animal" avec une méthode "speak()", et que vous créez une classe dérivée "Dog" qui redéfinit la méthode "speak()" pour faire "Woof!", alors c'est du method overriding.
    metho_overriding_example()
