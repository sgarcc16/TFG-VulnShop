from pathlib import Path


def check_requirements(filename):
    path = Path(filename)

    if not path.exists():
        print(f"No existe el archivo: {filename}")
        return

    lines = path.read_text().splitlines()

    dependencies = []

    for line in lines:
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        dependencies.append(line)

    print(f"\nAnalizando: {filename}")
    print("-" * 40)

    for dependency in dependencies:

        if "==" in dependency:
            print(f"[OK]       {dependency}")
        else:
            print(f"[UNPINNED] {dependency}")


check_requirements("requirements.txt")
check_requirements("requirements-lab-insecure.txt")