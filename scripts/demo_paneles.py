"""
Script de demostración: método de paneles de fuente para un perfil NACA.
Uso: python scripts/demo_paneles.py 0012 0
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import numpy as np
import matplotlib.pyplot as plt
from aerodinamica.perfiles.naca_generator import naca4_coordenadas
from aerodinamica.metodos_paneles.solver_fuente import MetodoPanelesFuente


def main(codigo_naca: str = "0012", alpha_deg: float = 0.0):
    # 1. Generar geometría del perfil
    x, y = naca4_coordenadas(codigo_naca, n_puntos=100)

    # 2. Crear el solver e ejecutar
    solver = MetodoPanelesFuente(x, y, v_inf=1.0, alpha_deg=alpha_deg)
    cp = solver.ejecutar()

    # 3. Visualizar resultados
    fig, axs = plt.subplots(1, 2, figsize=(14, 5))

    # Gráfica 1: Geometría y puntos de control
    axs[0].plot(x, y, "k-", linewidth=1.5, label="Contorno")
    axs[0].plot(solver.xc, solver.yc, "ro", markersize=3, label="Puntos de control")
    axs[0].set_aspect("equal")
    axs[0].set_title(f"Perfil NACA {codigo_naca}")
    axs[0].set_xlabel("x/c")
    axs[0].set_ylabel("y/c")
    axs[0].legend()
    axs[0].grid(True, alpha=0.3)

    # Gráfica 2: Distribución de presiones (Cp vs x/c)
    axs[1].plot(solver.xc, cp, "b.-", markersize=4)
    axs[1].invert_yaxis()  # El eje Cp se grafica invertido por convención
    axs[1].set_title(f"Distribución de presión (Cp) - α = {alpha_deg}°")
    axs[1].set_xlabel("x/c")
    axs[1].set_ylabel("Cp")
    axs[1].grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(f"data/resultados/cp_naca{codigo_naca}_alpha{alpha_deg}.png", dpi=150)
    plt.show()


if __name__ == "__main__":
    codigo = sys.argv[1] if len(sys.argv) > 1 else "0012"
    alpha = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0
    main(codigo, alpha)
    