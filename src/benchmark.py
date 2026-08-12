"""Benchmark de mimatmul vs NumPy (A @ B).

Compara el tiempo de mimatmul (Python puro) con numpy para matrices
cuadradas de varios tamaños. Mide varias repeticiones por tamaño y método,
con una ejecución de calentamiento, y guarda cada medición en CSV.

Uso (desde la raíz del repositorio):
    python src/benchmark.py
"""

import csv
import sys
import time
from pathlib import Path

import numpy as np

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from src.mimatmul import mimatmul  # noqa: E402

CSV_FILE = REPO_ROOT / "data" / "benchmark_results.csv"

SIZES = [50, 100, 200, 300]
REPETICIONES = 3
METODOS = {
    "mimatmul": lambda A, B: mimatmul(A, B),
    "numpy": lambda A, B: A @ B,
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


if __name__ == "__main__":
    main()
