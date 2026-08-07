# Proyecto 0 — MCOC

## Propósito general

Implementar una función propia de multiplicación de matrices (`mimatmul`)
en Python puro, comparar su rendimiento con `numpy.matmul` mediante un
benchmark sencillo y documentar el resultado (tiempos, uso de CPU/RAM y
gráfico final en P0E2).

Esta entrega (P0E1) cubre: configuración del ambiente, información básica
del computador y una primera versión de la implementación con una prueba
inicial.

## Sistema operativo y versión de Python

- Sistema operativo: Windows 11 (ver detalles en `data/system_info.json`)
- Versión de Python: 3.14.7

## Crear y activar el ambiente virtual

Desde la raíz del repositorio:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Linux / macOS:

```bash
source .venv/bin/activate
```

## Instalar dependencias

Con el ambiente virtual activado:

```bash
pip install -r requirements.txt
```

## Estado actual del proyecto

- Ambiente configurado (Python, Git, GitHub, OpenCode).
- Información del computador disponible en `data/system_info.json`
  (generada por `src/system_info.py`).
- Primera versión de `src/mimatmul.py` (multiplicación de matrices en
  Python puro, caso general cuadrado y rectangular).
- Prueba inicial en `tests/test_mimatmul.py`.

Pendiente para P0E2: benchmark definitivo, datos finales, gráfico completo
y documentación final.
