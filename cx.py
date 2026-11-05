#!/usr/bin/env python3
import argparse
from pathlib import Path
from cx_functions import get_bins, print_bins, add_bin, remove_bin, modify_bin, run_default, run_name, run_N, auto_fix

def main():
    file_path = Path("Cargo.toml")
    bins = get_bins(file_path)
    description = """
                    Gestor para binarios en Rust mas simple de usar que Cargo.
                    Notas:
                    N: Es el numero del binario. El primer binario es el 0, el segundo binario tiene N=1, etc
                    El N sirve para los comandos add, remove y modify
                    """
    parser = argparse.ArgumentParser(description="Gestor para binarios en Rust mas simple de usar que Cargo")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Comandos")

    # ---------------------------------------------------------
    # 1. Comando: show
    # ---------------------------------------------------------
    parser_print = subparsers.add_parser("show", help="Mostrar todos los binarios (nombre y path)")

    # ---------------------------------------------------------
    # 2. Comando: autofix
    # ---------------------------------------------------------
    parser_print = subparsers.add_parser("autofix", help="Actualizar poniendo todos los binarios (dentro de src y src/bin) en Cargo.toml")

    # ---------------------------------------------------------
    # 3. Comando: add <name> <path>
    # ---------------------------------------------------------
    parser_add = subparsers.add_parser("add", help="Añade un binario")
    parser_add.add_argument("name", type=str, help="Nombre del binario")
    parser_add.add_argument("path", type=str, help="Ruta del binario")

    # ---------------------------------------------------------
    # 4. Comando: remove (<name> O --path <path>)
    # ---------------------------------------------------------
    parser_remove = subparsers.add_parser("remove", help="Elimina un binario")
    parser_remove.add_argument("name", type=int, help="numero del binario (el primer binario es 0, etc)")

    # ---------------------------------------------------------
    # 5. Comando: modify <N> <name> <path (optional)>
    # ---------------------------------------------------------
    parser_modify = subparsers.add_parser("modify", help="Modifica un binario")
    parser_modify.add_argument("N", type=int, help="Numero del binario a modificar")
    parser_modify.add_argument("name", type=str, help="Nuevo nombre del binario")
    parser_modify.add_argument("path", type=str, nargs="?", default=None, help="Nuevo path del binario")

    # ---------------------------------------------------------
    # 6. Comando: Run
    # ---------------------------------------------------------
    parser_run = subparsers.add_parser("run", 
                                       help="correr binario\nEjemplo: - `run [name]`\n- `run` (se ejecutara el default-run en Cargo.toml si lo hay)\n- `run N [N] (ejecuta `cx show` para saber el N de cada archivo)")
    parser_run.add_argument("binary_name",type=str,nargs="?", default=None,
                            help="Nombre del binario a correr (opcional si usas -N)",
                            )
    parser_run.add_argument("-N",type=int,dest="binary_number",
        help="Numero del binario a correr (en lugar del nombre)",
    )

    # ---------------------------------------------------------
    # Parsear los argumentos de la terminal
    # ---------------------------------------------------------
    args = parser.parse_args()

    # Cargar los binarios justo antes de procesar la orden
    bins = get_bins(file_path)
    if bins is None:
        print("No se pudo leer la estructura de binarios desde Cargo.toml.")
        return

    # Logica de ejecucion
    if args.command == "show":
        print_bins(bins)

    elif args.command == "autofix":
        auto_fix(file_path,bins)

    elif args.command == "add":
        add_bin(file_path,bins, args.name, args.path)

    elif args.command == "remove":
        remove_bin(file_path, bins,args.name)

    elif args.command == "modify":
        modify_bin(file_path, bins, args.N, args.name, args.path)

    elif args.command == "run":
        if args.binary_number is not None:
            run_N(bins, args.binary_number)
            
        elif args.binary_name is not None:
            run_name(bins, args.binary_name)
            
        else:
            run_default(file_path, bins)


if __name__ == "__main__":
    main()