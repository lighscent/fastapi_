import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":

    # Compute the x and y coordinates for points on sine and cosine curves
    x = np.arange(0, 3 * np.pi, 0.1)
    y_sin = np.sin(x)
    y_cos = np.cos(x)

    # Plot the points using matplotlib
    plt.figure(figsize=(15, 3))
    plt.plot(x, y_sin)
    plt.plot(x, y_cos)
    plt.xlabel("x axis label")
    plt.ylabel("y axis label")
    plt.title("Sine and Cosine")
    plt.legend(["Sine", "Cosine"])
    plt.tight_layout()
    plt.grid()
    plt.show()
