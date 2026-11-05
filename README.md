# 🦀 CX - Cargo Extension

[![Rust](https://img.shields.io/badge/Rust-compatible-orange.svg)](https://www.rust-lang.org/)
[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)

**CX** es un gestor CLI ligero diseñado para simplificar la gestión y ejecución de múltiples binarios en proyectos de Rust sin tener que manipular manualmente la sección `[[bin]]` ni el atributo `default-run` de tu archivo `Cargo.toml`.

---

## ✨ Características

- 🔍 **Detección Automática (`autofix`):** Escanea la carpeta `src/` (incluyendo subcarpetas) y registra automáticamente todos los archivos `.rs` como binarios en `Cargo.toml`.
- 📋 **Visualización Clara (`show`):** Muestra una tabla numerada con el índice (`N`), nombre de los binarios, sus rutas y la línea exacta donde están en el archivo.
- ➕ **Gestión Sencilla (`add`, `remove`, `modify`):** Añade, elimina o modifica definiciones de binarios de forma interactiva utilizando números de índice simples.
- 🚀 **Ejecución Flexible (`run`):** 
  - Ejecuta el binario definido en `default-run` o te ayuda a configurarlo interactivamente si no existe.
  - Ejecuta binarios por su nombre (`cx run <nombre>`).
  - Ejecuta binarios por su número de índice (`cx run -N <número>`).
- ⚙️ **Configuración Inteligente de `default-run`:** Si no existe un binario por defecto en `Cargo.toml`, `cx run` te permite seleccionar uno de la lista e inserta la clave `default-run` manteniendo la sangría original justo debajo de `edition`.
- ⚡ **Multiplataforma:** Normaliza automáticamente las rutas (`/`) para garantizar la compatibilidad con el formato TOML.

---

## 📦 Instalación

Sigue estos pasos para instalar `cx` globalmente en tu sistema (Linux / macOS) y poder ejecutarlo desde cualquier terminal con solo escribir `cx`:

```bash
git clone [https://github.com/Fabric047/Cargo-eXtension.git](https://github.com/Fabric047/Cargo-eXtension.git)
cd Cargo-eXtension
chmod +x install.sh
./install.sh
```
