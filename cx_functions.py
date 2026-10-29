from pathlib import Path


def get_bins(file_path: str) -> dict:

    bins = {"name": [], "path": [], "line_name": [], "line_path": []}
    try: 
        lines = file_path.read_text(encoding="utf-8").splitlines()
        inside_bin = False
        current_bin = {}
        for i, line in enumerate(lines):
            stripped = line.strip()

            if stripped == "[[bin]]":
                inside_bin = True
                continue
            if stripped.startswith("[") and stripped != "[[bin]]":
                inside_bin = False

            if inside_bin and ("name" in stripped or "path" in stripped) and not stripped.startswith("#"):
                if "=" in stripped:
                    key, value = stripped.split("=",1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if key in bins:
                        bins[key].append(value)
                        bins[f"line_{key}"].append(i)
        return bins

    except FileNotFoundError:
        print("The file doesn't exist")
        return None

def print_bins(bins: dict) -> None:
    print(f"{'N':<5}{'Name':<15}{'Path':<30}{'Line':<10}")

    for i in range(len(bins["name"])):
        print(f"{i:<5}{bins['name'][i]:<15}{bins['path'][i]:<30}{bins['line_path'][i]:<10}")
    


def add_bin(file_path: Path, bins: dict, new_name: str, new_path: str) -> None:
    names = bins.get("name", [])
    if new_name in names:
        position = names.index(new_name)
        print(f"El nombre ({new_name}) ya existe en Cargo.toml y apunta a {bins.get('path')[position]}")
        continuar = input("¿Desea continuar de todas formas? (y/n) ").lower()
        if continuar != "y": 
            return None

    try:
        lines = file_path.read_text(encoding="utf-8").splitlines()
        
        # Si hay binarios previos, inserta justo despues del ultimo.
        # Si la lista esta vacía, inserta al final del archivo.
        if bins.get("line_path"):
            insert_line = bins.get("line_path")[-1] + 1
        else:
            insert_line = len(lines)

        new_bin = f'\n[[bin]]\nname = "{new_name}"\npath = "{new_path}"'
        lines.insert(insert_line, new_bin)
        
        file_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        
        # actualizar el dict
        bins["name"].append(new_name)
        bins["path"].append(new_path)
        bins["line_name"].append(insert_line + 2)
        bins["line_path"].append(insert_line + 3)

        print(f"Nuevo binario agregado: Name={new_name}, Path={new_path}")

    except FileNotFoundError:
        print("El archivo Cargo.toml no existe")

def remove_bin(file_path: Path, bins: dict, n: int, confirm: bool = True) -> None:
    if not bins.get("name") or n < 0 or n >= len(bins["name"]):
        print("El índice especificado no existe.")
        return

    target_name = bins["name"][n]

    # Solo pide confirmacion si confirm es True
    if confirm:
        print(f"{'Name':<15}{'Path':<30}{'Line':<10}")
        print(f"{bins['name'][n]:<15}{bins['path'][n]:<30}{bins['line_path'][n]:<10}")
        delete = input("\n¿Seguro que desea eliminar el binario? (y/n) ").lower()
        if delete != "y":
            return

    try:
        lines = file_path.read_text(encoding="utf-8").splitlines(keepends=True)
        line_name_idx = bins["line_name"][n]
        line_path_idx = bins["line_path"][n]

        bin_header_idx = line_name_idx
        while bin_header_idx >= 0 and lines[bin_header_idx].strip() != "[[bin]]":
            bin_header_idx -= 1

        if bin_header_idx < 0:
            return

        end_idx = max(line_name_idx, line_path_idx)
        while end_idx + 1 < len(lines):
            next_line = lines[end_idx + 1].strip()
            if next_line.startswith("["):
                break
            end_idx += 1

        lines_to_remove = set(range(bin_header_idx, end_idx + 1))
        lines_filtered = [line for i, line in enumerate(lines) if i not in lines_to_remove]

        file_path.write_text("".join(lines_filtered), encoding="utf-8")

        bins["name"].pop(n)
        bins["path"].pop(n)
        bins["line_name"].pop(n)
        bins["line_path"].pop(n)

        print(f"Binario '{target_name}' eliminado exitosamente.")

    except FileNotFoundError:
        print("El archivo no existe.")

def modify_bin(file_path: Path, bins: dict, n:int, new_name: str = None, new_path: str = None) -> None:
    if not bins.get("name") or n<0 or n>=len(bins["name"]):
        print("El indice no existe")
        return
    
    print(f"{'Name':<15}{'Path':<30}{'Line':<10}")
    print(f"{bins['name'][n]:<15}{bins['path'][n]:<30}{bins['line_path'][n]:<10}")

    delete = input("\n¿Seguro que desea modificarlo? (y/n) ").lower()
    if delete != "y":
        return

    try:
        lines = file_path.read_text(encoding="utf-8").splitlines(keepends=True)
        
        line_name_idx = bins["line_name"][n]
        line_path_idx = bins["line_path"][n]
        
        # Valores antiguos
        old_name = bins["name"][n]
        old_path = bins["path"][n]


        if new_path==None: new_path=old_path
        lines[line_name_idx] = f'name = "{new_name}"\n'
        lines[line_path_idx] = f'path = "{new_path}"\n'
        
        # Guardar
        file_path.write_text("".join(lines), encoding="utf-8")

        # Actualizamos el diccionario
        bins["name"][n] = new_name
        bins["path"][n] = new_path

        print(f"Binario cambiado:\nName: {old_name} -> {new_name}\nPath: {old_path} -> {new_path}")

    except FileNotFoundError:
        print("El archivo Cargo.toml no existe")

def run_bin(bins: dict, N: int) -> None:
    if not bins.get("name") or N < 0 or N >= len(bins["name"]):
        print("El índice no existe.")
        return

    import subprocess
    name = bins["name"][N]
    command = ["cargo", "run", "--bin", name]
    subprocess.run(command)

def auto_fix(cargo_path: Path, bins: dict) -> None:
    for i in range(len(bins["name"]) - 1, -1, -1):
        remove_bin(cargo_path, bins, i, confirm=False)

    folder = Path("src")

    for rs_file in folder.rglob("*.rs"):
        file_name = rs_file.stem
        rs_path_str = rs_file.as_posix()

        add_bin(cargo_path, bins, file_name, rs_path_str)

