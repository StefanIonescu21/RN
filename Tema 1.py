import pathlib


# 1. Parsing the System of Equations
def load_system(path: pathlib.Path) -> tuple[list[list[float]], list[float]]:
    coeficienti_A = []
    termeni_B = []

    with open(path, "r") as fisier:
        for rand in fisier:
            if "=" not in rand:
                continue

            partea_stanga, partea_dreapta = rand.split("=")
            termeni_B.append(float(partea_dreapta.strip()))

            rand_curent = []
            semn_curent = 1.0

            for element in partea_stanga.split():
                if element == "+":
                    semn_curent = 1.0
                elif element == "-":
                    semn_curent = -1.0
                else:
                    valoare_str = element[:-1]  # eliminam x, y sau z
                    coef = 1.0 if valoare_str == "" else float(valoare_str)
                    rand_curent.append(coef * semn_curent)

            coeficienti_A.append(rand_curent)

    return coeficienti_A, termeni_B


A, B = load_system(pathlib.Path("system.txt"))
print(f"{A=}\n{B=}")


# 2. Matrix and Vector Operations
def determinant(matrix: list[list[float]]) -> float:
    termen1 = matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
    termen2 = matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
    termen3 = matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
    return termen1 - termen2 + termen3


def trace(matrix: list[list[float]]) -> float:
    return sum(matrix[i][i] for i in range(len(matrix)))

def norm(vector: list[float]) -> float:
    return sum(x ** 2 for x in vector) ** 0.5

def transpose(matrix: list[list[float]]) -> list[list[float]]:
    dim = len(matrix)
    return [[matrix[rand][col] for rand in range(dim)] for col in range(len(matrix[0]))]

def multiply(matrix: list[list[float]], vector: list[float]) -> list[float]:
    rezultat = []
    for rand in matrix:
        suma_produse = sum(rand[i] * vector[i] for i in range(len(vector)))
        rezultat.append(suma_produse)
    return rezultat


# 3. Solving using Cramer's Rule
def solve_cramer(matrix: list[list[float]], vector: list[float]) -> list[float]:
    det_principal = determinant(matrix)
    solutii = []

    for coloana_tinta in range(3):
        matrice_temporara = [[matrix[i][j] for j in range(3)] for i in range(3)]

        for rand in range(3):
            matrice_temporara[rand][coloana_tinta] = vector[rand]

        solutii.append(determinant(matrice_temporara) / det_principal)

    return solutii


# 4. Solving using Inversion
def minor(matrix: list[list[float]], rand_exclus: int, col_exclusa: int) -> list[list[float]]:
    return [[val for j, val in enumerate(rand) if j != col_exclusa]
            for i, rand in enumerate(matrix) if i != rand_exclus]


def cofactor(matrix: list[list[float]]) -> list[list[float]]:
    dim = len(matrix)
    matrice_cofactori = []

    for i in range(dim):
        rand_nou = []
        for j in range(dim):
            min_mat = minor(matrix, i, j)
            det_minor = min_mat[0][0] * min_mat[1][1] - min_mat[0][1] * min_mat[1][0]
            rand_nou.append(((-1) ** (i + j)) * det_minor)
        matrice_cofactori.append(rand_nou)

    return matrice_cofactori


def adjoint(matrix: list[list[float]]) -> list[list[float]]:
    return transpose(cofactor(matrix))


def solve(matrix: list[list[float]], vector: list[float]) -> list[float]:
    det_A = determinant(matrix)
    adjuncta_A = adjoint(matrix)

    inversa_A = [[element / det_A for element in rand] for rand in adjuncta_A]

    return multiply(inversa_A, vector)