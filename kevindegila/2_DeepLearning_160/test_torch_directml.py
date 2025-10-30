import time
import torch
import torch_directml

# Obtenir le device DirectML
try:
    d = torch_directml.device()
    print("DirectML device:", d)
except Exception as e:
    print("Erreur en initialisant torch_directml:", e)
    raise

# Test: multiplication matricielle sur le device
try:
    a = torch.randn(2000, 2000, device=d)
    b = torch.randn(2000, 2000, device=d)
    t0 = time.time()
    c = a @ b
    # Forcer la synchronisation en lisant une valeur
    _ = c[0, 0].item()
    t1 = time.time()
    print(f"Matmul 2000x2000 sur DirectML: {t1 - t0:.3f}s")
except Exception as e:
    print("Erreur durant le test matriciel:", e)
    raise
