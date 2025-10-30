import argparse
import os
import time
from pathlib import Path

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

# Éxécuter avec: D:\dl\.venv\Scripts\python.exe D:\dl\waste\test_poubelle_AMD_GPU.py --epochs 999 --batch-size 16 --img-size 160 --amp

try:
    import torch_directml

    HAS_DIRECTML = True
except Exception:
    torch_directml = None
    HAS_DIRECTML = False


class TFLikeCNN(nn.Module):
    """Small CNN roughly matching the original Keras architecture in test_poubelle.py"""

    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            nn.Conv2d(128, 128, kernel_size=3, padding=1),
            nn.ReLU(inplace=True),
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten(),
            nn.Linear(128, 128),
            nn.ReLU(inplace=True),
            nn.Dropout(0.0),
            nn.Linear(128, 1),
        )

    def forward(self, x):
        return self.net(x)


def get_device():
    if HAS_DIRECTML:
        try:
            d = torch_directml.device()
            print("Using DirectML device:", d)
            return d
        except Exception as e:
            print("Failed to init DirectML device, falling back to CPU:", e)
    if torch.cuda.is_available():
        return torch.device("cuda")
    return torch.device("cpu")


def build_loaders(data_dir, batch_size, img_size=224, num_workers=4):
    train_transforms = transforms.Compose(
        [
            transforms.RandomResizedCrop(img_size, scale=(0.8, 1.0)),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    )
    test_transforms = transforms.Compose(
        [
            transforms.Resize((img_size, img_size)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    )

    train_dir = Path(data_dir) / "TRAIN"
    test_dir = Path(data_dir) / "TEST"

    if not train_dir.exists() or not test_dir.exists():
        raise FileNotFoundError(f"TRAIN/TEST not found under {data_dir}")

    train_ds = datasets.ImageFolder(str(train_dir), transform=train_transforms)
    test_ds = datasets.ImageFolder(str(test_dir), transform=test_transforms)

    train_loader = DataLoader(
        train_ds,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True,
    )
    test_loader = DataLoader(
        test_ds,
        batch_size=batch_size,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True,
    )

    print(
        f"Found {len(train_ds)} train images, {len(test_ds)} test images. Classes: {train_ds.classes}"
    )
    return train_loader, test_loader


def train_one_epoch(
    model, loader, criterion, optimizer, device, use_amp=False, scaler=None
):
    model.train()
    running_loss = 0.0
    running_corrects = 0
    total = 0
    for inputs, labels in loader:
        inputs = inputs.to(device)
        labels = labels.to(device).float().unsqueeze(1)

        optimizer.zero_grad()
        if use_amp:
            device_type = "cuda" if torch.cuda.is_available() else "cpu"
            dev_str = str(device).lower()
            if "dml" in dev_str or dev_str.startswith("privateuse"):
                device_type = "dml"
            try:
                with torch.autocast(device_type):
                    outputs = model(inputs)
                    loss = criterion(outputs, labels)
            except Exception:
                outputs = model(inputs)
                loss = criterion(outputs, labels)

            if scaler is not None:
                scaler.scale(loss).backward()
                scaler.step(optimizer)
                scaler.update()
            else:
                loss.backward()
                optimizer.step()
        else:
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

        preds = (torch.sigmoid(outputs) > 0.5).float()
        running_loss += loss.item() * inputs.size(0)
        running_corrects += (preds == labels).sum().item()
        total += inputs.size(0)
    epoch_loss = running_loss / total
    epoch_acc = running_corrects / total
    return epoch_loss, epoch_acc


def evaluate(model, loader, criterion, device, use_amp=False):
    model.eval()
    running_loss = 0.0
    running_corrects = 0
    total = 0
    with torch.no_grad():
        for inputs, labels in loader:
            inputs = inputs.to(device)
            labels = labels.to(device).float().unsqueeze(1)
            if use_amp:
                device_type = "cuda" if torch.cuda.is_available() else "cpu"
                dev_str = str(device).lower()
                if "dml" in dev_str or dev_str.startswith("privateuse"):
                    device_type = "dml"
                try:
                    with torch.autocast(device_type):
                        outputs = model(inputs)
                        loss = criterion(outputs, labels)
                except Exception:
                    outputs = model(inputs)
                    loss = criterion(outputs, labels)
            else:
                outputs = model(inputs)
                loss = criterion(outputs, labels)
            preds = (torch.sigmoid(outputs) > 0.5).float()
            running_loss += loss.item() * inputs.size(0)
            running_corrects += (preds == labels).sum().item()
            total += inputs.size(0)
    epoch_loss = running_loss / total
    epoch_acc = running_corrects / total
    return epoch_loss, epoch_acc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-dir",
        type=str,
        default="./datasets/WASTE/",
        help="Path to dataset (contains TRAIN/ and TEST/)",
    )
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--epochs", type=int, default=50)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument(
        "--amp",
        action="store_true",
        help="Enable automatic mixed precision if available",
    )
    parser.add_argument(
        "--img-size",
        type=int,
        default=224,
        help="Image size for training/validation (e.g. 160 or 224)",
    )
    parser.add_argument(
        "--num-workers",
        type=int,
        default=0,
        help="Number of DataLoader workers (set 0 to avoid multiprocessing issues)",
    )
    parser.add_argument("--patience", type=int, default=7)
    parser.add_argument("--save", type=str, default="best_model_poubelle.pt")
    parser.add_argument(
        "--dry-run", action="store_true", help="Load one batch and exit (sanity check)"
    )
    parser.add_argument(
        "--save-preds",
        type=str,
        default=None,
        help="If set, save predictions (npy) to this path (saved on dry-run)",
    )
    parser.add_argument(
        "--seed", type=int, default=42, help="Random seed for reproducibility"
    )
    args = parser.parse_args()

    device = get_device()

    train_loader, test_loader = build_loaders(
        args.data_dir,
        args.batch_size,
        img_size=args.img_size,
        num_workers=args.num_workers,
    )

    model = TFLikeCNN()
    model.to(device)

    criterion = nn.BCEWithLogitsLoss()
    optimizer = optim.RMSprop(model.parameters(), lr=args.lr)

    use_amp = False
    scaler = None
    if args.amp:
        try:
            from torch.cuda.amp import GradScaler

            scaler = GradScaler()
            use_amp = True
            print("AMP enabled: using GradScaler")
        except Exception:
            try:
                from torch.amp import GradScaler

                scaler = GradScaler()
                use_amp = True
                print("AMP enabled: using GradScaler (torch.amp)")
            except Exception:
                use_amp = True
                print("AMP enabled (no GradScaler available) - autocast only")

    # quick sanity check: run one batch and exit
    if args.dry_run:
        import numpy as _np
        import random as _random

        _random.seed(args.seed)
        _np.random.seed(args.seed)

        for inputs, labels in train_loader:
            inputs = inputs.to(device)
            labels = labels.to(device)
            outputs = model(inputs)
            print(
                "Dry-run OK: model forward pass successful. Output shape:",
                outputs.shape,
            )
            # move outputs to cpu numpy and save if requested
            out_np = outputs.detach().cpu().numpy()
            if args.save_preds:
                _np.save(args.save_preds, out_np)
                print("Saved PT preds to", args.save_preds)
            return

    best_acc = 0.0
    epochs_no_improve = 0
    for epoch in range(1, args.epochs + 1):
        t0 = time.time()
        train_loss, train_acc = train_one_epoch(
            model,
            train_loader,
            criterion,
            optimizer,
            device,
            use_amp=use_amp,
            scaler=scaler,
        )
        val_loss, val_acc = evaluate(
            model, test_loader, criterion, device, use_amp=use_amp
        )
        t1 = time.time()
        print(
            f"Epoch {epoch}/{args.epochs} - {t1-t0:.1f}s - train_loss: {train_loss:.4f} acc: {train_acc:.4f} | val_loss: {val_loss:.4f} acc: {val_acc:.4f}"
        )

        if val_acc > best_acc:
            best_acc = val_acc
            epochs_no_improve = 0
            torch.save(model.state_dict(), args.save)
            print(f"Saved best model ({best_acc:.4f}) to {args.save}")
        else:
            epochs_no_improve += 1
            if epochs_no_improve >= args.patience:
                print(
                    f"Early stopping after {epoch} epochs. Best val acc: {best_acc:.4f}"
                )
                break

    # final evaluation
    loss, acc = evaluate(model, test_loader, criterion, device, use_amp=use_amp)
    print(f"\nFinal evaluation - loss: {loss:.4f} acc: {acc:.4f}")


if __name__ == "__main__":
    main()
