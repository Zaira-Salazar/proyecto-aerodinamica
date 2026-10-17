"""
Pruebas unitarias para el generador de perfiles NACA.
Ejecutar con: python -m pytest tests/ -v
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

import numpy as np
import pytest
from aerodinamica.perfiles.naca_generator import naca4_coordenadas, espesor_maximo, curvatura_maxima


def test_naca_codigo_valido():
    """Verifica que se genere correctamente un perfil válido."""
    x, y = naca4_coordenadas("2412", n_puntos=100)
    assert len(x) == len(y)
    assert len(x) > 50


def test_naca_codigo_letras():
    """Verifica que se lance error si el código tiene letras."""
    with pytest.raises(ValueError, match="4 dígitos"):
        naca4_coordenadas("abc", n_puntos=100)


def test_naca_codigo_muy_corto():
    """Verifica que se lance error si el código tiene menos de 4 dígitos."""
    with pytest.raises(ValueError, match="4 dígitos"):
        naca4_coordenadas("12", n_puntos=100)


def test_validacion_curvatura():
    """Verifica que se rechacen curvaturas mayores al 6%."""
    with pytest.raises(ValueError, match="Curvatura máxima inválida"):
        naca4_coordenadas("9999", n_puntos=100)


def test_validacion_espesor():
    """Verifica que se rechacen espesores fuera de rango (6%-21%)."""
    with pytest.raises(ValueError, match="Espesor máximo inválido"):
        naca4_coordenadas("0010", n_puntos=100)  # Espesor de 10% (válido)
        naca4_coordenadas("0025", n_puntos=100)  # Espesor de 25% (inválido)


def test_espesor_maximo():
    """Verifica el cálculo del espesor máximo."""
    assert espesor_maximo("0012") == 0.12
    assert espesor_maximo("2415") == 0.15


def test_curvatura_maxima():
    """Verifica el cálculo de la curvatura máxima."""
    assert curvatura_maxima("2412") == 0.02
    assert curvatura_maxima("0012") == 0.0


def test_borde_ataque():
    """El perfil debe empezar en x=0 (borde de ataque)."""
    x, y = naca4_coordenadas("0012", n_puntos=200)
    assert np.isclose(x.min(), 0.0, atol=1e-6)
    