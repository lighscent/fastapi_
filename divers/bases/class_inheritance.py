
from tools import *

class A:

    def __init__(self):
        print("A.__init__")

    def feature1(self):
        print("A.feture1")


class B(A):

    def __init__(self):
        print("B.__init__")
        super().__init__()

    def feature2(self):
        print("B.feture2")


# Simple héritage

# a = A()
b = B()

# classes = [a, b]
# for c in classes:
#     print(c.__class__.__name__, "est de la classe ", c.__class__.__name__)

sl()

# print("-" * 55)

# for c in classes:
#     for i in classes:
#         print(
#             c.__class__.__name__,
#             "est une instance de ",
#             i.__class__.__name__,
#             "?",
#             isinstance(c, i.__class__),
#         )


class C(
    B,
    A,
):
    def __init__(self):
        print("C.__init__")
        super().__init__()

    def feature3(self):
        print("C.feture3")


c = C()
