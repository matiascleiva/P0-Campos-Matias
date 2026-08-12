"""Benchmark de mimatmul vs NumPy (A @ B).

Compara el tiempo de mimatmul (Python puro) con numpy para matrices
cuadradas de varios tamaños. Mide varias repeticiones por tamaño y método,
con una ejecución de calentamiento, guarda cada medición en CSV y genera
el gráfico figures/benchmark.png.

Uso (desde la raíz del repositorio):
    python src/benchmark.py
"""

import csv
import sys
import time
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.mimatmul import mimatmul  # noqa: E402

CSV_FILE = REPO_ROOT / "data" / "benchmark_results.csv"
FIG_FILE = REPO_ROOT / "figures" / "benchmark.png"

SIZES = [50, 100, 200, 300]
REPETICIONES = 3
METODOS = {
    "mimatmul": lambda A, B: mimatmul(A, B),
    "numpy": lambda A, B: A @ B,
}
NOMBRES_METODOS = {
    "mimatmul": "mimatmul (Python puro)",
    "numpy": "NumPy (A @ B)",
}


def matriz_cuadrada(n: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return rng.random((n, n))


def medir(funcion, A, B, n_repeticiones: int) -> list[float]:
    tiempos = []
    for _ in range(n_repeticiones):
        inicio = time.perf_counter()
        funcion(A, B)
        tiempos.append(time.perf_counter() - inicio)
    return tiempos


def generar_grafico() -> None:
    """Genera figures/benchmark.png a partir del CSV con las mediciones."""
    datos = defaultdict(lambda: defaultdict(list))
    with CSV_FILE.open(encoding="utf-8") as f:
        for fila in csv.DictReader(f):
            datos[fila["metodo"]][int(fila["tamano"])].append(
                float(fila["tiempo_segundos"])
            )

    fig, ax = plt.subplots(figsize=(8, 5))
    for metodo in METODOS:
        tamanos = sorted(datos[metodo])
        medias = [np.mean(datos[metodo][n]) for n in tamanos]
        minimos = [np.min(datos[metodo][n]) for n in tamanos]
        maximos = [np.max(datos[metodo][n]) for n in tamanos]
        ax.errorbar(
            tamanos,
            medias,
            yerr=[np.subtract(medias, minimos), np.subtract(maximos, medias)],
            marker="o",
            label=NOMBRES_METODOS[metodo],
        )

    ax.set_yscale("log")
    ax.set_xlabel("Tamaño de la matriz (n×n)")
    ax.set_ylabel("Tiempo (segundos)")
    ax.set_title("Multiplicación de matrices: mimatmul vs NumPy")
    ax.legend()
    ax.grid(True, which="both", linestyle="--", alpha=0.5)

    FIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(FIG_FILE, dpi=150)
    plt.close(fig)
    print(f"Gráfico guardado en: {FIG_FILE}")


def main() -> None:
    CSV_FILE.parent.mkdir(parents=True, exist_ok=True)
    resultados = []

    for n in SIZES:
        A = matriz_cuadrada(n, seed=n)
        B = matriz_cuadrada(n, seed=n + 1)
        A_lista = A.tolist()
        B_lista = B.tolist()

        medir(METODOS["mimatmul"], A_lista, B_lista, 1)
        medir(METODOS["numpy"], A, B, 1)

        for metodo, funcion in METODOS.items():
            if metodo == "mimatmul":
                args = (A_lista, B_lista)
            else:
                args = (A, B)
            tiempos = medir(funcion, *args, REPETICIONES)
            for i, t in enumerate(tiempos, start=1):
                resultados.append({
                    "metodo": metodo,
                    "tamano": n,
                    "repeticion": i,
                    "tiempo_segundos": round(t, 6),
                })

    with CSV_FILE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["metodo", "tamano", "repeticion", "tiempo_segundos"]
        )
        writer.writeheader()
        writer.writerows(resultados)

    print(f"Resultados guardados en: {CSV_FILE}")
    print(f"Mediciones totales: {len(resultados)}")

    generar_grafico()


if __name__ == "__main__":
    main()
