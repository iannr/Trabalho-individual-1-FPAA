# Implementação do Algoritmo de Karatsuba em Python

> Repositório: **Trabalho-individual-1-FPAA**  
> **Disciplina:** Fundamentos de Projeto e Análise de Algoritmos  
> **Aluno:** Ian Nascimento Rocha

---

## 1) Descrição do projeto

Este projeto implementa, em Python, o algoritmo de Karatsuba para multiplicação eficiente de inteiros grandes.  
O método tradicional (escolar) realiza O(n²) multiplicações de dígitos; Karatsuba reduz para O(n^{log₂ 3}) ≈ O(n^{1.585}), onde *n* é o número de dígitos.

### Ideia do algoritmo
Dado `a` e `b` (não-negativos), tomamos `m = ⌊n/2⌋`, onde `n = max(dígitos(a), dígitos(b))`, e escrevemos:
- `a = a1 * 10^m + a0`  
- `b = b1 * 10^m + b0`

Calculamos:
- `z0 = karatsuba(a0, b0)`  
- `z2 = karatsuba(a1, b1)`  
- `z1 = karatsuba(a0 + a1, b0 + b1) - z0 - z2`

Então, `a*b = z2 * 10^(2m) + z1 * 10^m + z0`.

### Lógica linha a linha (arquivo `main.py`)
Principais trechos explicados (omitindo comentários/CLI):
```py
def _split_number(x: int, m: int) -> Tuple[int, int]:
    base = 10 ** m
    return x // base, x % base
```
Divide `x` em duas partes em base decimal `10^m`, retornando `(alto, baixo)`.

```py
def _num_digits(x: int) -> int:
    x = abs(x)
    if x == 0:
        return 1
    return len(str(x))
```
Conta os dígitos decimais de `|x|` (zero tem 1 dígito).

```py
def _karatsuba_nonneg(a: int, b: int) -> int:
    if a < 10 or b < 10:
        return a * b
```
**Caso base:** se algum operando tem 1 dígito, faz multiplicação direta.

```py
    n = max(_num_digits(a), _num_digits(b))
    m = n // 2  # usa piso; para n >= 2, assegura m >= 1
```
Escolhe o corte `m` (metade inferior do maior número de dígitos).

```py
    a1, a0 = _split_number(a, m)
    b1, b0 = _split_number(b, m)
```
Separa `a` e `b` em partes alta e baixa.

```py
    z0 = _karatsuba_nonneg(a0, b0)
    z2 = _karatsuba_nonneg(a1, b1)
    z1 = _karatsuba_nonneg(a0 + a1, b0 + b1) - z0 - z2
```
Três multiplicações recursivas (duas puras e uma “cruzada” simplificada).

```py
    return (z2 * (10 ** (2 * m))) + (z1 * (10 ** m)) + z0
```
Combina os resultados com deslocamentos por potências de 10.

```py
def karatsuba(x: int, y: int) -> int:
    sign = -1 if (x < 0) ^ (y < 0) else 1
    return sign * _karatsuba_nonneg(abs(x), abs(y))
```
Trata sinais e delega para a versão não-negativa.

```py
def main(argv=None):
    # CLI: lê dois inteiros e imprime o produto; sem args, roda testes de sanidade.
```
Interface de linha de comando.

---

## 2) Como executar o projeto (ambiente local)

1. **Clonar** este repositório (ou baixar os arquivos):
   ```bash
   git clone https://github.com/<iannr>/Trabalho-individual-1-FPAA.git
   cd Trabalho-individual-1-FPAA
   ```

2. **Executar** diretamente com Python 3.10+:
   ```bash
   python main.py 123456789 987654321
   ```

3. **Rodar os testes de sanidade (sem argumentos):**
   ```bash
   python main.py
   ```
   O script compara com a multiplicação nativa do Python e imprime `OK/ERRO`.

> **Dependências:** nenhuma — apenas biblioteca padrão.

---

## 3) Relatório técnico

### 3.1) Análise da **complexidade ciclomática**

**Função alvo:** `_karatsuba_nonneg(a, b)`

**Fluxo de controle (passo a passo):**
1. **Início** da função.  
2. **Decisão**: `if a < 10 or b < 10`.  
   - **Verdadeiro** ⇒ **Return (caso base)** ⇒ **Fim**.  
   - **Falso** ⇒ **Cálculos e splits** (`n`, `m`, `_split_number`) ⇒ **Recursões + retorno final** ⇒ **Fim**.

**Grafo de fluxo (nós e arestas):**  
- **Nós (N):**
  1. Start  
  2. Decisão `a<10 or b<10`  
  3. Return base  
  4. Cálculo/split  
  5. Return final  
  6. End

- **Arestas (E):**
  - 1 → 2  
  - 2 → 3  (ramo verdadeiro)  
  - 2 → 4  (ramo falso)  
  - 3 → 6  
  - 4 → 5  
  - 5 → 6

**Cálculo:** \( M = E - N + 2P = 6 - 6 + 2(1) = 2 \).

**Esquemático (ASCII):**
```
   [Start]
      |
   (Decisão) ---true---> [Return base] ---> [End]
      |
     false
      v
 [Cálculo/split] ---> [Return final] -----> [End]
```

> Nota: a recursão não aumenta a complexidade ciclomática; ela mede caminhos de decisão, não profundidade de pilha.

---

### 3.2) Análise da complexidade assintótica

Modelo: custo proporcional a *n* (dígitos). Somas/subtrações/deslocamentos: O(n).

- **Tempo:**  
  \[ T(n) = 3\,T(\lceil n/2 \rceil) + O(n) \Rightarrow T(n) = \Theta(n^{\log_2 3}) \approx \Theta(n^{1.585}) \]
- **Espaço:**  
  - **Pilha de recursão:** **O(log n)**.  
  - **Espaço de trabalho por chamada:** **O(n)** (inteiros grandes).  
  - **Total efetivo:** **O(n)** transitório + **O(log n)** de pilha.

**Casos:**
- **Melhor caso:** operandos pequenos atingem o caso base cedo ⇒ **O(1)**.  
- **Caso médio:** operandos grandes de tamanhos comparáveis ⇒ **Θ(n^{log₂ 3})**.  
- **Pior caso:** idem ao caso médio (par/ímpar não muda a ordem) ⇒ **Θ(n^{log₂ 3})**.

---

## 4) Validação rápida
Execute sem argumentos para rodar testes de sanidade e comparar com `a*b` nativo.

---

## 5) Referências
- A. Karatsuba; Y. Ofman (1962). *Multiplication of Multidigit Numbers on Automata.*  
