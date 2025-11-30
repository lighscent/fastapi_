import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":

    # Define the vectors
    v = np.array([1, 2])
    w = np.array([3, 4])

    # Calculate the dot product
    dot_product = np.dot(v, w)

    # Calculate the projection of w onto v
    # Projection of w onto v is (dot(w, v) / ||v||^2) * v
    v_squared_norm = np.sum(v**2)  # ||v||^2
    projection_w_on_v = (dot_product / v_squared_norm) * v

    print(f"Vecteur v: {v}")
    print(f"Vecteur w: {w}")
    print(f"Produit scalaire (v . w): {dot_product}")
    print(f"Projection de w sur v: {projection_w_on_v}")

    # Plotting
    plt.figure(figsize=(8, 8))
    ax = plt.gca()

    # Plot the origin
    ax.quiver(
        0,
        0,
        v[0],
        v[1],
        angles="xy",
        scale_units="xy",
        scale=1,
        color="r",
        label=f"v = {v}",
    )
    ax.quiver(
        0,
        0,
        w[0],
        w[1],
        angles="xy",
        scale_units="xy",
        scale=1,
        color="b",
        label=f"w = {w}",
    )

    # Plot the projection
    # Format individual elements of the projection array
    projection_label = f"Projection de w sur v = [{projection_w_on_v[0]:.2f}, {projection_w_on_v[1]:.2f}]"
    # Removed linestyle='dashed' from the quiver plot for the projection
    ax.quiver(
        0,
        0,
        projection_w_on_v[0],
        projection_w_on_v[1],
        angles="xy",
        scale_units="xy",
        scale=1,
        color="g",
        label=projection_label,
        alpha=0.5,
    )

    # Add a dashed line from the tip of w to the tip of its projection on v
    # This line should be perpendicular to v
    plt.plot(
        [w[0], projection_w_on_v[0]], [w[1], projection_w_on_v[1]], "k--", linewidth=0.8
    )

    # Set limits and labels
    max_val = max(max(abs(v)), max(abs(w))) + 2
    ax.set_xlim([-1, max_val])
    ax.set_ylim([-1, max_val])
    ax.set_xlabel("X axis")
    ax.set_ylabel("Y axis")
    ax.set_title("Visualisation de Vecteurs et Projection")
    ax.grid()
    ax.set_aspect("equal", adjustable="box")  # Keep aspect ratio equal

    # Draw axes through the origin
    ax.axhline(0, color="grey", lw=2)
    ax.axvline(0, color="grey", lw=2)

    plt.legend()
    plt.show()
