"""Pruebas iniciales de mimatmul."""

import pytest

from src.mimatmul import mimatmul


def test_identidad():
    identidad = [[1, 0], [0, 1]]
    assert mimatmul(identidad, [[5, 6], [7, 8]]) == [[5, 6], [7, 8]]


def test_producto_conocido():
    A = [[1, 2, 3], [4, 5, 6]]
    B = [[7, 8], [9, 10], [11, 12]]
    esperado = [[58, 64], [139, 154]]
    assert mimatmul(A, B) == esperado


def test_matrices_cuadradas():
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    esperado = [[19, 22], [43, 50]]
    assert mimatmul(A, B) == esperado


def test_compara_con_numpy():
    import numpy as np

    rng = np.random.default_rng(0)
    A = rng.integers(0, 10, size=(4, 5)).tolist()
    B = rng.integers(0, 10, size=(5, 3)).tolist()
    resultado = mimatmul(A, B)
    esperado = (np.asarray(A) @ np.asarray(B)).tolist()
    assert resultado == esperado


def test_dimensiones_incompatibles():
    with pytest.raises(ValueError):
        mimatmul([[1, 2]], [[1], [2], [3]])
