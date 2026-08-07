"""Multiplicación de matrices en Python puro (mimatmul)."""


def mimatmul(A, B):
    """Multiplica dos matrices A (m×k) y B (k×n), devolviendo m×n.

    Acepta secuencias anidadas (listas/tuplas) o arrays de numpy.
    Lanza ValueError si las dimensiones son incompatibles.
    """
    m = len(A)
    k = len(A[0]) if m else 0
    n = len(B[0]) if B else 0

    if m == 0 or k == 0 or n == 0:
        raise ValueError("Las matrices no pueden ser vacías")

    if k != len(B):
        raise ValueError(
            f"Dimensiones incompatibles: A es {m}×{k} y B es {len(B)}×{n}"
        )

    resultado = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            acumulado = 0
            for t in range(k):
                acumulado += A[i][t] * B[t][j]
            resultado[i][j] = acumulado
    return resultado


if __name__ == "__main__":
    A = [[1, 2, 3], [4, 5, 6]]
    B = [[7, 8], [9, 10], [11, 12]]
    print(mimatmul(A, B))
