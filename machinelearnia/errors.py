from sklearn.neighbors import KNeighborsClassifier
from tools import *
from time import sleep

# from rich import print

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def exemple1():
    iris = sns.load_dataset("iris")

    print("Head :", iris.head())
    sl(w)
    print("Sample :", iris.sample(7))
    sl(w)
    print("Tail :", iris.tail())

    sl(w)
    print(f"shape : {iris.shape}")

    sl(w)
    print(iris["species"].value_counts())

    sl(w)
    print(iris["petal_length"])


def exemple_regression_lineaire():
    from sklearn.model_selection import train_test_split
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

    # Generate some sample data
    np.random.seed(0)
    X = 2 * np.random.rand(100, 1)
    y = 4 + 3 * X + np.random.randn(100, 1)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Create and train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Calculate error metrics
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Mean Absolute Error (MAE): {mae}")
    sl(w)
    print(f"Mean Squared Error (MSE): {mse}")
    sl(w)
    print(f"R-squared (R2 ): {r2}")


def exemple2():
    import numpy as np
    import matplotlib.pyplot as plt

    # Generate many values from a standard normal distribution
    data = np.random.randn(2_000_000)

    plt.hist(data, bins=6000, density=True)
    plt.title("Approximation de la distribution normale N(0,1)")
    plt.xlabel("Valeurs")
    plt.ylabel("Densité")

    plt.show()


def exemple3():
    dataset = {f"exp_{i}": np.random.randn(100) for i in range(4)}
    print(dataset)

    def graph_box(data):
        df = pd.DataFrame(data)
        sns.boxplot(data=df)
        plt.title("Boxplot des expériences")
        plt.xlabel("Expériences")
        plt.ylabel("Valeurs")
        plt.show()

    def graph(data):
        n = len(data)
        plt.figure(figsize=(12, 20))

        for i in range(1, n + 1):
            plt.subplot(n, 1, i)
            plt.plot(data[f"exp_{i-1}"], label=f"exp_{i-1}")
            plt.legend()
        plt.tight_layout()
        plt.show()

    graph_box(dataset)
    graph(dataset)


def exemple4():

    from sklearn.datasets import load_iris

    print("ok")
    iris = load_iris()
    print(iris["target"])  # video 18:24


def exemple5():

    a = np.ones((3, 4))
    b = "3"

    a += int(b)

    a.astype("int")

    print(a)


def exemple6():

    from sklearn.datasets import make_regression

    np.random.seed(0)

    x, y = make_regression(n_samples=100, n_features=1, noise=10)

    plt.scatter(x, y)

    # y = y.reshape(y.shape[0], 1)
    # X = np.hstack((x, np.ones(x.shape)))
    plt.show()


def exemple7():
    from sklearn.datasets import load_iris

    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.model_selection import learning_curve

    iris = load_iris()
    X = iris.data
    y = iris.target

    print(X.shape)

    model = KNeighborsClassifier(n_neighbors=12)

    N, train_score, val_score = learning_curve(
        model, X, y, train_sizes=np.linspace(0.1, 1, 10), cv=5
    )

    print(N)

    plt.plot(N, train_score.mean(axis=1), label="train")
    plt.plot(N, val_score.mean(axis=1), label="validation")
    plt.xlabel("train_sizes")
    plt.legend()
    plt.show()


def exemple8():
    cls()
    ms = pd.read_csv("datasets/movie.csv")
    print(ms.shape, ms, sep="\n")


def exemple9():
    def div(a, b):
        try:
            return a / b
        except ZeroDivisionError:
            print(f"Division de {a} par {b} interdite !")
            return False

    print(div(1, 0))


if __name__ == "__main__":

    w = 55

    cls()

    # exemple1() # iris dataset
    # exemple_regression_lineaire()
    # exemple2() # courbe de gauss
    # exemple3() # Dessine le graphe des expériences
    # exemple4()
    # exemple5()
    # exemple6() # make_reression()
    # exemple7() # Aff des neighbors
    # exemple8() # file not found
    exemple9() # Division par 0

    sleep(1)
    sl(w)
    print('Ready.')
