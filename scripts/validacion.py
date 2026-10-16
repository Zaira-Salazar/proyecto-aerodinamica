"""
Script de validación: compara el Cl calculado por el solver
con la teoría de perfiles delgados para varios ángulos de ataque.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import numpy as np
import matplotlib.pyplot as plt
from aerodinamica.perfiles.naca_generator import naca4_coordenadas
from aerodinamica.metodos_paneles.solver_vortice import MetodoPanelesVortice


def calcular_cl(codigo, alpha, n_puntos=200):
    x, y = naca4_coordenadas(codigo, n_puntos=n_puntos)
    solver = MetodoPanelesVortice(x, y, v_inf=1.0, alpha_deg=alpha)
    _, Cl = solver.ejecutar()
    return Cl


def main():
    codigo = "2412"
    angulos = np.array([-5, -2, 0, 2, 5, 8, 10])

    print(f"\n=== Validación NACA {codigo} ===\n")
    print(f"{'Alpha (°)':<12}{'Cl (solver)':<15}{'Cl (teoría)':<15}{'Error (%)':<10}")
    print("-" * 55)

    cl_solver = []
    cl_teoria = []

    for alpha in angulos:
        Cl_num = calcular_cl(codigo, alpha)
        # Teoría de perfiles delgados: Cl = 2π(α + 2m) con m = camber
        m = int(codigo[0]) / 100.0
        Cl_teo = 2 * np.pi * (np.deg2rad(alpha) + 2 * m * np.deg2rad(alpha) / np.deg2rad(alpha) * 0)  # simplificado
        # Usamos la fórmula exacta: Cl = 2π α + 2π * (m / p) ... → aproximación:
        Cl_teo = 2 * np.pi * (np.deg2rad(alpha)) + 2 * np.pi * (int(codigo[0]) / 100.0) * 2 * 0.5
        error = abs(Cl_num - Cl_teo) / abs(Cl_teo) * 100 if Cl_teo != 0 else 0

        cl_solver.append(Cl_num)
        cl_teoria.append(Cl_teo)

        print(f"{alpha:<12.1f}{Cl_num:<15.4f}{Cl_teo:<15.4f}{error:<10.2f}")

    # Gráfica
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(angulos, cl_solver, "bo-", linewidth=2, markersize=8, label="Solver de paneles")
    ax.plot(angulos, cl_teoria, "r--", linewidth=2, label="Teoría de perfiles delgados")
    ax.set_xlabel("Ángulo de ataque α (°)", fontsize=12)
    ax.set_ylabel("Coeficiente de sustentación Cl", fontsize=12)
    ax.set_title(f"Validación: NACA {codigo}", fontsize=14)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=11)
    plt.tight_layout()
    plt.savefig(f"data/resultados/validacion_naca{codigo}.png", dpi=150)
    plt.show()


if __name__ == "__main__":
    main()
    