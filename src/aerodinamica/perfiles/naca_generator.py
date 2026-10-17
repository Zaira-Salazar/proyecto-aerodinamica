"""
Módulo para generar la geometría de perfiles NACA de 4 dígitos.
Referencia: Abbott & Von Doenhoff, "Theory of Wing Sections", 1949.
"""

import numpy as np


def naca4_coordenadas(codigo: str, n_puntos: int = 200):
    """
    Genera las coordenadas (x, y) del contorno de un perfil NACA de 4 dígitos.

    Parámetros
    ----------
    codigo : str
        Código NACA de 4 dígitos, ej. "2412", "0012".
    n_puntos : int
        Número de puntos por lado (superior e inferior).

    Retorna
    -------
    x : np.ndarray
        Coordenadas x del contorno (normalizadas por la cuerda).
    y : np.ndarray
        Coordenadas y del contorno.
    """
    # --- Validación del formato ---
    if len(codigo) != 4 or not codigo.isdigit():
        raise ValueError("El código NACA debe tener 4 dígitos, ej. '2412'.")

    m = int(codigo[0]) / 100.0   # curvatura máxima
    p = int(codigo[1]) / 10.0    # posición de la curvatura
    t = int(codigo[2:]) / 100.0  # espesor máximo

    # --- Validaciones físicas ---
    if m > 0.06:
        raise ValueError(
            f"Curvatura máxima inválida: {m*100:.0f}%. "
            "El máximo realista para perfiles NACA es 6%."
        )
    if m > 0 and p == 0:
        raise ValueError(
            "Si hay curvatura, la posición no puede ser 0."
        )
    if p > 0.9:
        raise ValueError(
            f"Posición de curvatura inválida: {p*100:.0f}%. "
            "Debe estar entre 0 y 90%."
        )
    if t < 0.06 or t > 0.21:
        raise ValueError(
            f"Espesor máximo inválido: {t*100:.0f}%. "
            "Los perfiles NACA reales tienen entre 6% y 21%."
        )

    # Distribución cosenoidal (concentra puntos en el borde de ataque)
    beta = np.linspace(0, np.pi, n_puntos)
    x = 0.5 * (1 - np.cos(beta))

    # Espesor (fórmula estándar NACA)
    yt = 5 * t * (
        0.2969 * np.sqrt(x)
        - 0.1260 * x
        - 0.3516 * x**2
        + 0.2843 * x**3
        - 0.1015 * x**4
    )

    # Línea de curvatura (camber)
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

    # Superficie superior e inferior
    xu = x - yt * np.sin(theta)
    yu = yc + yt * np.cos(theta)
    xl = x + yt * np.sin(theta)
    yl = yc - yt * np.cos(theta)

    # Unir: borde de ataque -> superior -> borde de fuga -> inferior
    x_contorno = np.concatenate([xu[::-1], xl[1:]])
    y_contorno = np.concatenate([yu[::-1], yl[1:]])

    return x_contorno, y_contorno


def espesor_maximo(codigo: str) -> float:
    """Retorna el espesor máximo como fracción de la cuerda."""
    return int(codigo[2:]) / 100.0


def curvatura_maxima(codigo: str) -> float:
    """Retorna la curvatura máxima como fracción de la cuerda."""
    return int(codigo[0]) / 100.0