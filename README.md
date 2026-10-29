# 🦀 CX - Cargo Extension

**CX** es una herramienta de línea de comandos (CLI) ligera diseñada para simplificar la gestión de múltiples binarios en proyectos de Rust. Permite agregar, listar, eliminar, modificar y ejecutar archivos binarios dentro de tu proyecto sin la necesidad de manipular manualmente la sección `[[bin]]` del archivo `Cargo.toml`.

---

## ✨ Características

- 🔍 **Detección Automática (`autofix`):** Escanea la carpeta `src/` (incluyendo subcarpetas) y registra automáticamente todos los archivos `.rs` como binarios en `Cargo.toml`.
- 📋 **Visualización Clara (`show`):** Muestra una tabla numerada con los nombres de los binarios, sus rutas y su posición dentro del archivo de configuración.
- ➕ **Gestión Sencilla:** Añade, elimina o modifica definiciones de binarios sin errores de sintaxis manuales.
- 🚀 **Ejecución Directa (`run`):** Corre cualquier binario registrado utilizando simplemente su número de índice (`N`).
- ⚡ **Rápido y Multiplataforma:** Normaliza automáticamente las rutas (`/`) para garantizar la compatibilidad con el formato TOML en cualquier sistema operativo.

---

## 📦 Instalación

Sigue estos sencillos pasos para instalar `cx` globalmente en tu sistema operativo (Linux / macOS) y poder ejecutarlo desde cualquier terminal con solo escribir `cx`:

### 1. Clonar el repositorio

```bash
git clone [https://github.com/tu_usuario/tu_repositorio.git](https://github.com/tu_usuario/tu_repositorio.git)
cd tu_repositorio

```
