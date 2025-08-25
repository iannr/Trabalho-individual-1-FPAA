def karatsuba(x: int, y: int) -> int:
    # Caso base: se os números tiverem apenas 1 dígito
    if x < 10 or y < 10:
        return x * y

    # Determina o tamanho máximo em dígitos
    n = max(len(str(x)), len(str(y)))
    m = n // 2

    # Divide os números em partes
    high_x, low_x = divmod(x, 10**m)
    high_y, low_y = divmod(y, 10**m)

    # Recursivamente calcula os três produtos
    z0 = karatsuba(low_x, low_y)
    z1 = karatsuba((low_x + high_x), (low_y + high_y))
    z2 = karatsuba(high_x, high_y)

    # Combina os resultados
    return (z2 * 10**(2*m)) + ((z1 - z2 - z0) * 10**m) + z0


if __name__ == "__main__":
    print("Algoritmo de Karatsuba em execução...\n")

    # Exemplo de uso
    a = int(input("Digite o primeiro número: "))
    b = int(input("Digite o segundo número: "))

    resultado = karatsuba(a, b)

    print(f"\nResultado da multiplicação: {resultado}")