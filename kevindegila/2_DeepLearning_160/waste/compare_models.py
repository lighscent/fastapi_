import argparse
import argparse
import shutil
import subprocess
import time
from pathlib import Path
import tempfile
import numpy as np


def find_system_python():
    candidates = [
        r"C:\Users\utilisateur\AppData\Local\Programs\Python\Python313\python.exe",
        "python",
    ]
    for c in candidates:
        try:
            out = subprocess.check_output(
                [c, "-c", "import sys; print(sys.executable)"]
            )
            return c
        except Exception:
            continue
    raise RuntimeError("No system python found to run TensorFlow script")


def run_and_time(python_exe, script, args):
    cmd = [python_exe, script] + args
    t0 = time.time()
    proc = subprocess.run(cmd, capture_output=True, text=True)
    t1 = time.time()
    return proc.returncode, proc.stdout, proc.stderr, t1 - t0


def prepare_sample(src_data_dir: Path, dst_dir: Path, batch_size: int):
    src_train = Path(src_data_dir) / "TRAIN"
    classes = [p.name for p in src_train.iterdir() if p.is_dir()]
    for cls in classes:
        dst_cls = dst_dir / "TRAIN" / cls
        dst_cls.mkdir(parents=True, exist_ok=True)
        src_cls = src_train / cls
        count = 0
        for img in src_cls.iterdir():
            if img.is_file():
                shutil.copy(img, dst_cls / img.name)
                count += 1
                if count >= batch_size:
                    break
    src_test = Path(src_data_dir) / "TEST"
    for cls in classes:
        dst_cls = dst_dir / "TEST" / cls
        dst_cls.mkdir(parents=True, exist_ok=True)
        src_cls = src_test / cls
        count = 0
        for img in src_cls.iterdir():
            if img.is_file():
                shutil.copy(img, dst_cls / img.name)
                count += 1
                if count >= batch_size:
                    break


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-dir", default="./datasets/WASTE/", help="original dataset"
    )
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--img-size", type=int, default=160)
    parser.add_argument(
        "--tf-python",
        type=str,
        default=None,
        help="python executable for tensorflow (system)",
    )
    parser.add_argument(
        "--pt-python",
        type=str,
        default=r"D:\\dl\\.venv\\Scripts\\python.exe",
        help="python executable for pytorch venv",
    )
    parser.add_argument(
        "--cleanup", action="store_true", help="remove temporary sample dir after run"
    )
    args = parser.parse_args()

    tf_python = args.tf_python or find_system_python()
    pt_python = args.pt_python

    tmp = Path(tempfile.mkdtemp(prefix="cmp_models_"))
    try:
        print("Preparing sample data in:", tmp)
        prepare_sample(Path(args.data_dir), tmp, args.batch_size)

        tf_script = str(Path(__file__).parent / "test_poubelle_tf_gap.py")
        pt_script = str(Path(__file__).parent / "test_poubelle_AMD_GPU.py")

        tf_preds = tmp / "tf_preds.npy"
        pt_preds = tmp / "pt_preds.npy"

        tf_args = [
            "--dry-run",
            "--data-dir",
            str(tmp),
            "--batch-size",
            str(args.batch_size),
            "--img-size",
            str(args.img_size),
            "--save-preds",
            str(tf_preds),
        ]

        pt_args = [
            "--dry-run",
            "--data-dir",
            str(tmp),
            "--batch-size",
            str(args.batch_size),
            "--img-size",
            str(args.img_size),
            "--save-preds",
            str(pt_preds),
        ]

        print("\n==> Running TensorFlow script (system python):")
        rc, out, err, t_tf = run_and_time(tf_python, tf_script, tf_args)

        print("\n==> Running PyTorch script (venv python):")
        rc2, out2, err2, t_pt = run_and_time(pt_python, pt_script, pt_args)

        report_lines = []
        report_lines.append("COMPARISON REPORT")
        report_lines.append("=================")
        report_lines.append(f"Dataset sample dir: {tmp}")
        report_lines.append("")

        report_lines.append("TensorFlow run:")
        report_lines.append(f"  python: {tf_python}")
        report_lines.append(f"  return_code: {rc}")
        report_lines.append(f"  runtime (s): {t_tf:.2f}")
        report_lines.append("  stdout:")
        for line in (out or "").splitlines():
            report_lines.append(f"    {line}")
        report_lines.append("  stderr (first 10 lines):")
        for i, line in enumerate((err or "").splitlines()):
            if i >= 10:
                report_lines.append("    ... (truncated)")
                break
            report_lines.append(f"    {line}")
        report_lines.append("")

        report_lines.append("PyTorch run:")
        report_lines.append(f"  python: {pt_python}")
        report_lines.append(f"  return_code: {rc2}")
        report_lines.append(f"  runtime (s): {t_pt:.2f}")
        report_lines.append("  stdout:")
        for line in (out2 or "").splitlines():
            report_lines.append(f"    {line}")
        report_lines.append("  stderr (first 10 lines):")
        for i, line in enumerate((err2 or "").splitlines()):
            if i >= 10:
                report_lines.append("    ... (truncated)")
                break
            report_lines.append(f"    {line}")
        report_lines.append("")

        pred_section = ["Prediction comparison:"]
        if tf_preds.exists() and pt_preds.exists():
            a = np.load(tf_preds)
            b = np.load(pt_preds)
            if b.max() > 2.0 or b.min() < -2.0:
                b_sig = 1.0 / (1.0 + np.exp(-b))
                pred_section.append(
                    "  Note: PyTorch outputs looked like logits; applied sigmoid for comparison"
                )
            else:
                b_sig = b
            a_flat = a.reshape(-1)
            b_flat = b_sig.reshape(-1)
            l2 = np.linalg.norm(a_flat - b_flat)
            linf = np.max(np.abs(a_flat - b_flat))
            pred_section.append(f"  TF preds shape: {a.shape}")
            pred_section.append(f"  PT preds shape: {b.shape}")
            pred_section.append(f"  L2 diff: {l2:.6f}")
            pred_section.append(f"  Linf diff: {linf:.6f}")
        else:
            pred_section.append(
                f"  Missing prediction files: TF {tf_preds.exists()}, PT {pt_preds.exists()}"
            )

        report_lines.extend(pred_section)
        report_lines.append("")
        report_lines.append(f"Summary times: TF {t_tf:.2f}s, PT {t_pt:.2f}s")
        report_lines.append("")
        report_lines.append("Notes:")
        report_lines.append(
            " - Differences can come from architecture, initialization, CPU/GPU math, or logits vs probabilities."
        )
        report_lines.append(
            " - To reduce differences: align preprocessing (mean/std), use identical weight inits, and compare probabilities not logits."
        )

        report = "\n".join(report_lines)

        print("\n" + report)

        report_file = tmp / "report.txt"
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(report)

        print(f"\nReport saved to: {report_file}")

        if args.cleanup:
            try:
                shutil.rmtree(tmp)
                print(f"Temporary directory {tmp} removed (--cleanup requested).")
            except Exception as e:
                print(f"Could not remove temporary directory: {e}")

    except Exception as e:
        print("Error during compare run:", e)
        print("Temp dir left at:", tmp)
        raise


if __name__ == "__main__":
    main()
import sys
import time
from pathlib import Path
import tempfile
import numpy as np


def find_system_python():
    # try common location discovered earlier
    candidates = [
        r"C:\Users\utilisateur\AppData\Local\Programs\Python\Python313\python.exe",
        "python",
    ]
    for c in candidates:
        try:
            out = subprocess.check_output(
                [c, "-c", "import sys; print(sys.executable)"]
            )
            return c
        except Exception:
            continue
    raise RuntimeError("No system python found to run TensorFlow script")


def run_and_time(python_exe, script, args):
    cmd = [python_exe, script] + args
    t0 = time.time()
    proc = subprocess.run(cmd, capture_output=True, text=True)
    t1 = time.time()
    return proc.returncode, proc.stdout, proc.stderr, t1 - t0


def prepare_sample(src_data_dir: Path, dst_dir: Path, batch_size: int):
    # copy first batch_size images from each class from TRAIN
    src_train = Path(src_data_dir) / "TRAIN"
    classes = [p.name for p in src_train.iterdir() if p.is_dir()]
    for cls in classes:
        dst_cls = dst_dir / "TRAIN" / cls
        dst_cls.mkdir(parents=True, exist_ok=True)
        src_cls = src_train / cls
        count = 0
        for img in src_cls.iterdir():
            if img.is_file():
                shutil.copy(img, dst_cls / img.name)
                count += 1
                if count >= batch_size:
                    break
    # mirror for TEST
    src_test = Path(src_data_dir) / "TEST"
    for cls in classes:
        dst_cls = dst_dir / "TEST" / cls
        dst_cls.mkdir(parents=True, exist_ok=True)
        src_cls = src_test / cls
        count = 0
        for img in src_cls.iterdir():
            if img.is_file():
                shutil.copy(img, dst_cls / img.name)
                count += 1
                if count >= batch_size:
                    break


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data-dir", default="./datasets/WASTE/", help="original dataset"
    )
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--img-size", type=int, default=160)
    parser.add_argument(
        "--tf-python",
        type=str,
        default=None,
        help="python executable for tensorflow (system)",
    )
    parser.add_argument(
        "--pt-python",
        type=str,
        default=r"D:\\dl\\.venv\\Scripts\\python.exe",
        help="python executable for pytorch venv",
    )
    parser.add_argument(
        "--cleanup", action="store_true", help="remove temporary sample dir after run"
    )
    args = parser.parse_args()

    tf_python = args.tf_python or find_system_python()
    pt_python = args.pt_python

    tmp = Path(tempfile.mkdtemp(prefix="cmp_models_"))
    try:
        print("Preparing sample data in:", tmp)
        prepare_sample(Path(args.data_dir), tmp, args.batch_size)

        tf_script = str(Path(__file__).parent / "test_poubelle_tf_gap.py")
        pt_script = str(Path(__file__).parent / "test_poubelle_AMD_GPU.py")

        tf_preds = tmp / "tf_preds.npy"
        pt_preds = tmp / "pt_preds.npy"

        tf_args = [
            "--dry-run",
            "--data-dir",
            str(tmp),
            "--batch-size",
            str(args.batch_size),
            "--img-size",
            str(args.img_size),
            "--save-preds",
            str(tf_preds),
        ]

        pt_args = [
            "--dry-run",
            "--data-dir",
            str(tmp),
            "--batch-size",
            str(args.batch_size),
            "--img-size",
            str(args.img_size),
            "--save-preds",
            str(pt_preds),
        ]

        print("\n==> Running TensorFlow script (system python):")
        rc, out, err, t_tf = run_and_time(tf_python, tf_script, tf_args)

        print("\n==> Running PyTorch script (venv python):")
        rc2, out2, err2, t_pt = run_and_time(pt_python, pt_script, pt_args)

        # Build a clear report string
        report_lines = []
        report_lines.append("COMPARISON REPORT")
        report_lines.append("=================")
        report_lines.append(f"Dataset sample dir: {tmp}")
        report_lines.append("")

        report_lines.append("TensorFlow run:")
        report_lines.append(f"  python: {tf_python}")
        report_lines.append(f"  return_code: {rc}")
        report_lines.append(f"  runtime (s): {t_tf:.2f}")
        report_lines.append("  stdout:")
        for line in (out or "").splitlines():
            report_lines.append(f"    {line}")
        report_lines.append("  stderr (first 10 lines):")
        for i, line in enumerate((err or "").splitlines()):
            if i >= 10:
                report_lines.append("    ... (truncated)")
                break
            report_lines.append(f"    {line}")
        report_lines.append("")

        report_lines.append("PyTorch run:")
        report_lines.append(f"  python: {pt_python}")
        report_lines.append(f"  return_code: {rc2}")
        report_lines.append(f"  runtime (s): {t_pt:.2f}")
        report_lines.append("  stdout:")
        for line in (out2 or "").splitlines():
            report_lines.append(f"    {line}")
        report_lines.append("  stderr (first 10 lines):")
        for i, line in enumerate((err2 or "").splitlines()):
            if i >= 10:
                report_lines.append("    ... (truncated)")
                break
            report_lines.append(f"    {line}")
        report_lines.append("")

        # compare predictions
        pred_section = ["Prediction comparison:"]
        if tf_preds.exists() and pt_preds.exists():
            a = np.load(tf_preds)
            b = np.load(pt_preds)
            # detect logits -> convert
            if b.max() > 2.0 or b.min() < -2.0:
                b_sig = 1.0 / (1.0 + np.exp(-b))
                pred_section.append(
                    "  Note: PyTorch outputs looked like logits; applied sigmoid for comparison"
                )
            else:
                b_sig = b
            a_flat = a.reshape(-1)
            b_flat = b_sig.reshape(-1)
            l2 = np.linalg.norm(a_flat - b_flat)
            linf = np.max(np.abs(a_flat - b_flat))
            pred_section.append(f"  TF preds shape: {a.shape}")
            pred_section.append(f"  PT preds shape: {b.shape}")
            pred_section.append(f"  L2 diff: {l2:.6f}")
            pred_section.append(f"  Linf diff: {linf:.6f}")
        else:
            pred_section.append(
                f"  Missing prediction files: TF {tf_preds.exists()}, PT {pt_preds.exists()}"
            )

        report_lines.extend(pred_section)
        report_lines.append("")
        report_lines.append(f"Summary times: TF {t_tf:.2f}s, PT {t_pt:.2f}s")
        report_lines.append("")
        report_lines.append("Notes:")
        report_lines.append(
            " - Differences can come from architecture, initialization, CPU/GPU math, or logits vs probabilities."
        )
        report_lines.append(
            " - To reduce differences: align preprocessing (mean/std), use identical weight inits, and compare probabilities not logits."
        )

        report = "\n".join(report_lines)

        # print clear report to stdout
        print("\n" + report)

        # write report to file in tmp
        report_file = tmp / "report.txt"
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(report)

        print(f"\nReport saved to: {report_file}")

        if args.cleanup:
            try:
                shutil.rmtree(tmp)
                print(f"Temporary directory {tmp} removed (--cleanup requested).")
            except Exception as e:
                print(f"Could not remove temporary directory: {e}")

    except Exception as e:
        print("Error during compare run:", e)
        print("Temp dir left at:", tmp)
        raise


if __name__ == "__main__":
    main()
