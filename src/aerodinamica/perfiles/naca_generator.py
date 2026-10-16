"""
Módulo para generar la geometría de perfiles NACA de 4 dígitos.
Referencia: Abbott & Von Doenhoff, "Theory of Wing Sections", 1949.
"""

import numpy as np


def naca4_coordenadas(codigo: str, n_puntos: int = 200):
    """
    Genera las coordenadas (x, y) del contorno de un perfil NACA de 4 dígitos.
    """
    if len(codigo) != 4 or not codigo.isdigit():
        raise ValueError("El código NACA debe tener 4 dígitos, ej. '2412'.")

    m = int(codigo[0]) / 100.0   # curvatura máxima
    p = int(codigo[1]) / 10.0    # posición de la curvatura
    t = int(codigo[2:]) / 100.0  # espesor máximo

    beta = np.linspace(0, np.pi, n_puntos)
    x = 0.5 * (1 - np.cos(beta))

    yt = 5 * t * (
        0.2969 * np.sqrt(x)
        - 0.1260 * x
        - 0.3516 * x**2
        + 0.2843 * x**3
        - 0.1015 * x**4
    )

    yc = np.zeros_like(x)
    dyc_dx = np.zeros_like(x)

    if m > 0 and p > 0:
        idx1 = x < p
        idx2 = x >= p
        yc[idx1] = (m / p**2) * (2 * p * x[idx1] - x[idx1]**2)
        yc[idx2] = (m / (1 - p)**2) * ((1 - 2 * p) + 2 * p * x[idx2] - x[idx2]**2)
        dyc_dx[idx1] = (2 * m / p**2) * (p - x[idx1])
        dyc_dx[idx2] = (2 * m / (1 - p)**2) * (p - x[idx2])

    theta = np.arctan(dyc_dx)

    xu = x - yt * np.sin(theta)
    yu = yc + yt * np.cos(theta)
    xl = x + yt * np.sin(theta)
    yl = yc - yt * np.cos(theta)

    x_contorno = np.concatenate([xu[::-1], xl[1:]])
    y_contorno = np.concatenate([yu[::-1], yl[1:]])

    return x_contorno, y_contorno


def espesor_maximo(codigo: str) -> float:
    return int(codigo[2:]) / 100.0


def curvatura_maxima(codigo: str) -> float:
    return int(codigo[0]) / 100.0
    