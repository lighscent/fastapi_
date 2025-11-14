import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":

    # Define the matrix
    x = np.array([[1, 2], [3, 4]])

    # Define the standard basis vectors
    i = np.array([1, 0])
    j = np.array([0, 1])

    # Transform the basis vectors by multiplying them by the matrix x
    i_transformed = x @ i  # or x.dot(i) or np.dot(x, i)
    j_transformed = x @ j  # or x.dot(j) or np.dot(x, j)

    print(f"Matrice x:\n{x}")
    print(f"Vecteur de base i original: {i}")
    print(f"Vecteur de base j original: {j}")
    print(f"Vecteur de base i transformé: {i_transformed}")
    print(f"Vecteur de base j transformé: {j_transformed}")
    
    print(i_transformed.shape, '=', i.shape, '→', i_transformed.reshape(2,1).shape)
    # i[:, None] = i.reshape(2,1) = i[:, np.newaxis]

    # Plotting the transformation
    plt.figure(figsize=(8, 8))
    ax = plt.gca()

    # Plot original basis vectors (now solid) - Removed linestyle='dashed'
    ax.quiver(
        0,
        0,
        i[0],
        i[1],
        angles="xy",
        scale_units="xy",
        scale=1,
        color="grey",
        label="Base originale (i, j)",
    )
    ax.quiver(0, 0, j[0], j[1], angles="xy", scale_units="xy", scale=1, color="grey")

    # Plot transformed basis vectors (solid)
    ax.quiver(
        0,
        0,
        i_transformed[0],
        i_transformed[1],
        angles="xy",
        scale_units="xy",
        scale=1,
        color="r",
        label=f"i transformé = {i_transformed}",
    )
    ax.quiver(
        0,
        0,
        j_transformed[0],
        j_transformed[1],
        angles="xy",
        scale_units="xy",
        scale=1,
        color="b",
        label=f"j transformé = {j_transformed}",
    )

    # Set limits and labels
    max_val = (
        max(
            np.max(np.abs(x)),
            np.max(np.abs(i_transformed)),
            np.max(np.abs(j_transformed)),
        )
        + 1
    )
    ax.set_xlim([-0.2, max_val])
    ax.set_ylim([-0.2, max_val])
    ax.set_xlabel("X axis")
    ax.set_ylabel("Y axis")
    ax.set_title("Transformation Linéaire par la Matrice")
    ax.grid()
    ax.set_aspect("equal", adjustable="box")  # Keep aspect ratio equal

    # Draw axes through the origin
    ax.axhline(0, color="grey", lw=0.5)
    ax.axvline(0, color="grey", lw=0.5)

    plt.legend()
    plt.show()
