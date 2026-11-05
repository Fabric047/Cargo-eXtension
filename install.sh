#!/usr/bin/env bash

# Crear el directorio local de ejecutables si no existe
mkdir -p ~/.local/bin

# Otorgar permisos de ejecución a cx.py
chmod +x cx.py

# Crear un enlace simbólico 'cx' hacia cx.py en ~/.local/bin
ln -sf "$(pwd)/cx.py" ~/.local/bin/cx

echo "¡Instalación completada! Ahora puedes usar el comando 'cx'."
echo "Asegúrate de que ~/.local/bin esté en tu PATH."
