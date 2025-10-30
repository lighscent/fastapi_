import argparse
import os
from pathlib import Path

import tensorflow as tf


def build_model(input_shape=(224, 224, 3)):
    model = tf.keras.models.Sequential(
        [
            tf.keras.layers.Conv2D(
                32, (3, 3), padding="same", activation="relu", input_shape=input_shape
            ),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Conv2D(64, (3, 3), activation="relu"),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Conv2D(128, (3, 3), activation="relu"),
            tf.keras.layers.MaxPooling2D(2, 2),
            tf.keras.layers.Conv2D(128, (3, 3), activation="relu"),
            tf.keras.layers.MaxPooling2D(2, 2),
            # Use global average pooling so the spatial reduction matches the PyTorch model
            tf.keras.layers.GlobalAveragePooling2D(),
            tf.keras.layers.Dense(128, activation="relu"),
            tf.keras.layers.Dense(1, activation="sigmoid"),
        ]
    )
    return model


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-dir",
        type=str,
        default="./datasets/WASTE/",
        help="Path to dataset (contains TRAIN/ and TEST/)",
    )
    parser.add_argument("--img-size", type=int, default=224)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument(
        "--dry-run", action="store_true", help="Load one batch and exit"
    )
    parser.add_argument(
        "--save-preds",
        type=str,
        default=None,
        help="If set, save predictions (npy) to this path",
    )
    parser.add_argument(
        "--seed", type=int, default=42, help="Random seed for reproducibility"
    )
    args = parser.parse_args()

    train_dir = Path(args.data_dir) / "TRAIN"
    test_dir = Path(args.data_dir) / "TEST"
    if not train_dir.exists() or not test_dir.exists():
        raise FileNotFoundError("TRAIN/TEST not found under %s" % args.data_dir)

    # Use basic rescale to match Keras default preprocessing
    train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1.0 / 255)
    test_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1.0 / 255)

    train_gen = train_datagen.flow_from_directory(
        directory=str(train_dir),
        target_size=(args.img_size, args.img_size),
        batch_size=args.batch_size,
        class_mode="binary",
    )

    test_gen = test_datagen.flow_from_directory(
        directory=str(test_dir),
        target_size=(args.img_size, args.img_size),
        batch_size=args.batch_size,
        class_mode="binary",
    )

    model = build_model(input_shape=(args.img_size, args.img_size, 3))
    model.compile(
        optimizer=tf.keras.optimizers.RMSprop(learning_rate=1e-3),
        loss="binary_crossentropy",
        metrics=["accuracy"],
    )

    if args.dry_run:
        import numpy as _np
        import random as _random

        _random.seed(args.seed)
        _np.random.seed(args.seed)

        x, y = next(train_gen)
        print("Dry-run batch shapes:", x.shape, y.shape)
        preds = model.predict(x)
        print("Dry-run forward shapes:", preds.shape)
        if args.save_preds:
            _np.save(args.save_preds, preds)
            print("Saved TF preds to", args.save_preds)
        return

    # otherwise run a short train for demonstration
    history = model.fit(train_gen, validation_data=test_gen, epochs=2)
    print(history.history)


if __name__ == "__main__":
    main()
