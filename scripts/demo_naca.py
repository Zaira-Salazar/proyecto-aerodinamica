"""
Script de demostración: grafica el contorno de un perfil NACA.
Uso: python scripts/demo_naca.py 2412
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import matplotlib.pyplot as plt
from aerodinamica.perfiles.naca_generator import naca4_coordenadas


def main(codigo: str = "2412"):
    x, y = naca4_coordenadas(codigo, n_puntos=200)

    plt.figure(figsize=(10, 4))
    plt.plot(x, y, "b-", linewidth=1.5)
    plt.axis("equal")
    plt.grid(True, alpha=0.3)
    plt.title(f"Perfil NACA {codigo}")
    plt.xlabel("x/c")
    plt.ylabel("y/c")
    plt.tight_layout()
    plt.savefig(f"data/resultados/naca_{codigo}.png", dpi=150)
    plt.show()


if __name__ == "__main__":
    codigo = sys.argv[1] if len(sys.argv) > 1 else "2412"
    main(codigo)
    