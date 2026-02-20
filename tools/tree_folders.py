import os

EXCLUDE = {".git", ".github", ".vscode", ".venv", "node_modules", "__pycache__"}


def tree(path, prefix=""):
    entries = [e for e in os.listdir(path) if e not in EXCLUDE]
    entries = [e for e in entries if os.path.isdir(os.path.join(path, e))]
    entries.sort()

    for i, entry in enumerate(entries):
        full_path = os.path.join(path, entry)
        is_last = i == len(entries) - 1

        connector = "└── " if is_last else "├── "
        child_prefix = "    " if is_last else "│   "

        print(prefix + connector + entry)
        tree(full_path, prefix + child_prefix)


if __name__ == "__main__":
    with open("STRUCTURE.md", "w", encoding="utf-8") as f:
        import sys

        original_stdout = sys.stdout
        sys.stdout = f

        print("```text")
        tree(".")
        print("```")

        sys.stdout = original_stdout

    print("STRUCTURE.md généré avec succès.")
