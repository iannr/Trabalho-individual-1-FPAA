from __future__ import annotations
from typing import Tuple


def _split_number(x: int, m: int) -> Tuple[int, int]:
    base = 10 ** m
    return x // base, x % base


def _num_digits(x: int) -> int:
    x = abs(x)
    if x == 0:
        return 1
    return len(str(x))


def _karatsuba_nonneg(a: int, b: int) -> int:
    if a < 10 or b < 10:
        return a * b

    n = max(_num_digits(a), _num_digits(b))
    m = n // 2

    a1, a0 = _split_number(a, m)
    b1, b0 = _split_number(b, m)

    z0 = _karatsuba_nonneg(a0, b0)
    z2 = _karatsuba_nonneg(a1, b1)
    z1 = _karatsuba_nonneg(a0 + a1, b0 + b1) - z0 - z2

    return (z2 * (10 ** (2 * m))) + (z1 * (10 ** m)) + z0


def karatsuba(x: int, y: int) -> int:
    sign = -1 if (x < 0) ^ (y < 0) else 1
    return sign * _karatsuba_nonneg(abs(x), abs(y))


if __name__ == "__main__":
    print("== Multiplicação por Karatsuba ==")
    try:
        a = int(input("Digite o primeiro inteiro: ").strip())
        b = int(input("Digite o segundo inteiro: ").strip())
    except ValueError:
        print("Erro: por favor insira apenas inteiros.")
        exit(1)

    resultado = karatsuba(a, b)
    print(f"\nResultado: {a} * {b} = {resultado}")

    # verificação
    if resultado == a * b:
        print("Verificação: OK (resultado confere com a multiplicação nativa)")
    else:
        print("Verificação: ERRO (resultado difere da multiplicação nativa)")