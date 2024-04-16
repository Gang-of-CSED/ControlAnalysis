import numpy as np
import sympy as sp

eps = np.finfo(float).eps

def prepareString(string):
    if string is None:  
        return None
    string = string.replace(' ', '')
    if string == '':
        return None
    string = string.replace('S', 's')
    string = string.replace('**', '^')
    string = string.replace('s', '*s')
    string = string.replace('(', '*(')
    string = string.replace('+*', '+')
    string = string.replace('-*', '-')
    string = string.replace('**', '*')
    string = string.replace('/*', '/')
    string = string.replace('(*', '(')
    if string[0] == '*':
        string = string[1:]
    return string

def getPolynomialCoefficients(string):
    try:
        print(string)
        s = sp.symbols('s')
        polynomial = sp.sympify(string)
        coefficients = sp.Poly(polynomial, s).all_coeffs()
        print(coefficients)
        coefficients = [float(coeff) for coeff in coefficients]
        return coefficients
    except:
        return []

def getSystemPoles(polynomial):
    try:
        s = sp.symbols('s')
        print(polynomial)
        polynomial = sp.sympify(polynomial)
        poles = sp.roots(polynomial, s)
        return poles
    except:
        return []

def RouthHerwitzCriterion(polynomial):
    if polynomial is None:
        return None, None
    n = len(polynomial)
    if n < 2:
        return None, None
    if 0 in polynomial:
        return None, None
    table = np.zeros((n, (n+1)//2), dtype=object)
    table[0, :(n+1)//2] = polynomial[::2]
    table[1, :n//2] = polynomial[1::2]
    for i in range(2, n):
        for j in range((n-i+1)//2):
            table[i, j] = (table[i-1, 0]*table[i-2, j+1] - table[i-2, 0]*table[i-1, j+1]) / table[i-1, 0]
        if np.all(table[i, :] == 0):
            power = n-i
            for j in range((n-i+1)//2):
                if power <= 0:
                    break
                table[i, j] = table[i-1, j]*power
                power -= 2
        if table[i, 0] == 0:
            table[i, 0] = eps
    sign_changes = 0
    for i in range(1, n):
        if np.sign(table[i, 0]) != np.sign(table[i-1, 0]):
            sign_changes += 1
    print(table)
    return table, sign_changes