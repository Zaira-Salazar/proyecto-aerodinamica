# Método de Paneles para Perfiles NACA

Implementación en Python del **Método de Paneles de Fuente-Vórtice** para el cálculo de coeficientes aerodinámicos (\(C_l\), \(C_p\)) sobre perfiles NACA de 4 dígitos, con aplicación a la **Aerodinámica y Aeroelasticidad** computacional.

---

##  Tabla de contenidos

- [Descripción](#-descripción)
- [Características](#-características)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Estructura del proyecto](#-estructura-del-proyecto)
- [Validación](#-validación)
- [Tecnologías](#-tecnologías)
- [Referencias](#-referencias)
- [Autor](#-autor)

---

##  Descripción

Este proyecto implementa un **solver aerodinámico 2D** basado en el Método de Paneles de Fuente-Vórtice para analizar el flujo potencial incompresible alrededor de perfiles aerodinámicos de la serie **NACA de 4 dígitos** (por ejemplo, NACA 0012, NACA 2412).

El programa permite:

- Generar la geometría de perfiles NACA de 4 dígitos.
- Calcular la distribución de velocidades tangenciales y de presión (\(C_p\)) sobre el contorno del perfil.
- Estimar el coeficiente de sustentación (\(C_l\)) mediante la aplicación de la **Condición de Kutta**.
- Visualizar los resultados en gráficas de calidad técnica.
- Validar los resultados contra la **Teoría de Perfiles Delgados**.

Este proyecto fue desarrollado como **Proyecto Integrador** para la asignatura *Desarrollo de Algoritmos para la Simulación de Sistemas [DAS172]* de la carrera de **Ingeniería en Aeronáutica**.

---

##  Características

-  Generación de perfiles **NACA de 4 dígitos** con distribución cosenoidal de puntos (concentración en el borde de ataque).
- **Solver de paneles de fuente-vórtice** con condición de no penetración y Condición de Kutta.
- Cálculo de **coeficientes de presión (\(C_p\))** y **sustentación (\(C_l\))**.
- Scripts de **demostración** y **validación** listos para usar.
- Validaciones de entrada (códigos NACA inválidos, número de puntos insuficiente).
- Visualización con `matplotlib` de calidad publicable.

---

##  Instalación

### Requisitos previos

- **Python 3.10 o superior** ([descargar](https://www.python.org/downloads/))
- **Git** ([descargar](https://git-scm.com/))

### Pasos

1. **Clonar el repositorio:**

   ```bash
   git clone https://github.com/TU-USUARIO/proyecto-aerodinamica.git
   cd proyecto-aerodinamica
