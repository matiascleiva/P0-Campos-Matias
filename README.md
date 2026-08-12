# Proyecto 0 — MCOC

## Propósito general

Implementar una función propia de multiplicación de matrices (`mimatmul`)
en Python puro, comparar su rendimiento con `numpy.matmul` mediante un
benchmark y documentar los resultados (tiempos, uso de CPU/RAM/GPU y
gráfico final).

Este repositorio contiene la entrega P0E1 y P0E2 del Proyecto 0.

## Repositorio

```bash
git clone https://github.com/matiascleiva/P0-Campos-Matias.git
cd P0-Campos-Matias
```

## Ambiente y ejecución

### Crear el ambiente virtual

```bash
python -m venv .venv
```

### Activar el ambiente

Windows:

```bash
.venv\Scripts\activate
```

Linux / macOS:

```bash
source .venv/bin/activate
```

### Instalar dependencias

Con el ambiente activado:

```bash
pip install -r requirements.txt
```

### Ejecutar las pruebas

```bash
python -m pytest
```

### Ejecutar el benchmark

```bash
python src/benchmark.py
```

El benchmark mide `mimatmul` vs NumPy (`A @ B`) para matrices cuadradas de
tamaños 50, 100, 200 y 300, con 3 repeticiones por tamaño y método y una
ejecución de calentamiento. Genera:

- `data/benchmark_results.csv` — cada medición individual;
- `figures/benchmark.png` — gráfico de tiempos.

### Información del computador

```bash
python src/system_info.py
```

Genera `data/system_info.json`.

## Información del computador

Características principales del equipo utilizado para las mediciones:

| Característica | Valor |
|---|---|
| Sistema operativo | Windows 11 |
| Arquitectura | AMD64 |
| Procesador | Intel (Family 6, Model 154) |
| Núcleos físicos | 8 |
| Procesadores lógicos | 12 |
| RAM total | 16.89 GB |
| GPU | NVIDIA GeForce RTX 3060 Laptop + Intel UHD Graphics |
| Versión de Python | 3.14.7 |

## Resultados del benchmark

Los tiempos completos están en `data/benchmark_results.csv` y el gráfico en
`figures/benchmark.png`. Resumen de tiempos promedio por método:

| Tamaño (n×n) | mimatmul | NumPy |
|---|---|---|
| 50 | ~5 ms | ~0.01 ms |
| 100 | ~41 ms | ~0.14 ms |
| 200 | ~0.35 s | ~0.5 ms |
| 300 | ~1.3 s | ~7.6 ms |

## Observaciones de rendimiento

**¿mimatmul parece utilizar uno o varios núcleos?**

Uno. Durante las mediciones el proceso usó en promedio 0.88 núcleos (máximo
1.2). Python puro está limitado por el GIL, que solo permite ejecutar un hilo
de Python a la vez por proceso.

**¿NumPy parece utilizar uno o varios núcleos?**

Varios. El mismo proceso llegó a usar en promedio 3.5 núcleos con picos
cercanos a los 12 lógicos. NumPy delega la operación en su biblioteca BLAS
(OpenBLAS), que paraleliza la multiplicación en múltiples hilos.

**¿Por qué NumPy es más rápido?**

Por tres motivos principales: (1) el bucle crítico está escrito en C/Fortran
optimizado, no en Python interpretado; (2) usa instrucciones SIMD del
procesador y un algoritmo de multiplicación en bloques más eficiente que el
bucle triple ingenuo; (3) aprovecha varios núcleos, mientras que mimatmul queda
limitado a uno por el GIL.

**¿Por qué las repeticiones no entregan exactamente el mismo tiempo?**

Porque el tiempo de ejecución depende del estado del sistema: otros procesos
en segundo plano, cambios en la frecuencia del CPU, caché, y el arranque de
los hilos de BLAS en la primera ejecución. Por eso el benchmark toma varias
repeticiones y reporta cada una, en lugar de un único valor.

**¿Cuál es aproximadamente la matriz cuadrada de mayor tamaño que cabría en
la RAM libre del computador?**

Con 5.62 GB libres y 8 bytes por elemento float64, una sola matriz cabría
hasta n ≈ 26 500. Como una multiplicación necesita al menos A, B y el
resultado C, un tamaño realista es del orden de n ≈ 15 000 (unos 4.5 GB en
las tres matrices).

## Uso de OpenCode

**¿Qué parte realizó correctamente el agente?**

Configuró el ambiente (Python, Git, GitHub, OpenCode, ambiente virtual),
creó la estructura del repositorio, implementó `mimatmul`, las pruebas, el
benchmark y el gráfico, y mantuvo el trabajo en commits incrementales.

**¿Qué parte tuvo que corregir o modificar?**

El ajuste de los tamaños del benchmark (inicialmente eran demasiado
pequeños), la corrección del `.gitignore` (excluía el CSV de resultados que
sí debe subirse), la visibilidad del repositorio en GitHub y su traslado
fuera de la carpeta sincronizada de OneDrive.

**¿Qué archivo comprende mejor después del proyecto?**

`src/mimatmul.py`: es el más corto y claro. La función verifica que las
dimensiones sean compatibles (lanza `ValueError` si no), y luego hace tres
bucles anidados que acumulan `A[i][t] * B[t][j]` en la posición `[i][j]` del
resultado. Se puede seguir con papel y lápiz, y lo validé comparándolo con
NumPy en las pruebas.

**¿Qué parte del código todavía le resulta menos clara?**

`src/benchmark.py`, en especial la generación del gráfico: agrupar los datos
del CSV con diccionarios anidados para sacar promedios, el uso de `errorbar`
con barras de error asimétricas, y los detalles de la librería matplotlib
(figuras, ejes, leyenda). Es código de librería que todavía no me resulta
natural.

## Estado actual del proyecto

- P0E1: ambiente configurado, información del computador y primera versión
  de `mimatmul` con pruebas.
- P0E2: `mimatmul` completa, pruebas ampliadas (5 casos), benchmark con
  mediciones reales, CSV de resultados y gráfico final.
