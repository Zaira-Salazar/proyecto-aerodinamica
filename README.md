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
2. **Crear y activar un entorno virtual:**

   **Windows:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
3. **Instalar las dependencias:**

   ```bash
   pip install -r requirements.txt
   ```

---

## Uso

### 1. Visualizar la geometría de un perfil NACA

```bash
python scripts/demo_naca.py 2412
```

Esto genera una gráfica con el contorno del perfil **NACA 2412** y guarda la imagen en `data/resultados/`.

### 2. Ejecutar el solver de paneles de fuente-vórtice

```bash
python scripts/demo_vortice.py 2412 5
```

Donde:

- `2412` es el código NACA del perfil.
- `5` es el ángulo de ataque en grados.

Esto genera dos gráficas: el contorno con los puntos de control y la distribución de \(C_p\), mostrando el valor de \(C_l\) calculado.

### 3. Validar contra la teoría de perfiles delgados

```bash
python scripts/validacion.py
```

Genera una tabla comparativa y una gráfica de \(C_l\) vs. \(\alpha\) comparando con la teoría.

---

### Casos de prueba sugeridos

| Caso | Comando | Resultado esperado |
|---|---|---|
| Perfil simétrico sin ángulo | `python scripts/demo_vortice.py 0012 0` | \(C_l \approx 0\) |
| Perfil simétrico con 5° | `python scripts/demo_vortice.py 0012 5` | \(C_l \approx 0.55\) |
| Perfil con curvatura sin ángulo | `python scripts/demo_vortice.py 2412 0` | \(C_l \approx 0.28\) |
| Perfil con curvatura y 5° | `python scripts/demo_vortice.py 2412 5` | \(C_l \approx 0.89\) |

---

## Estructura del proyecto

```text
proyecto-aerodinamica/
│
├── README.md                 # Este archivo
├── requirements.txt          # Dependencias del proyecto
├── .gitignore                # Archivos ignorados por Git
│
├── src/                      # Código fuente
│   └── aerodinamica/
│       ├── perfiles/
│       │   └── naca_generator.py  # Generador de perfiles NACA
│       ├── metodos_paneles/
│       │   ├── solver_fuente.py   # Solver de solo fuentes
│       │   └── solver_vortice.py  # Solver de fuente-vórtice (con Kutta)
│       ├── visualizacion/
│       └── utilidades/
│
├── scripts/                  # Scripts ejecutables
│   ├── demo_naca.py          # Demo del generador de geometrías
│   ├── demo_paneles.py       # Demo del solver de fuentes
│   ├── demo_vortice.py       # Demo del solver de fuente-vórtice
│   └── validacion.py         # Script de validación
│
├── tests/                    # Pruebas unitarias
│
├── data/
│   └── resultados/           # Imágenes y datos generados
│
└── docs/                     # Documentación técnica
```

---

## Validación

El solver fue validado contra la **Teoría de Perfiles Delgados** para el perfil **NACA 2412** en un rango de ángulos de ataque entre -5° y 10°.

### Resultados

| Ángulo (°) | \(C_l\) (Solver) | \(C_l\) (Teoría) | Error relativo (%) |
|---:|---:|---:|---:|
| -5 | -0.35 | -0.40 | 12.5 |
| -2 | 0.03 | -0.15 | — |
| 0 | 0.28 | 0.10 | — |
| 2 | 0.53 | 0.35 | — |
| 5 | 0.89 | 0.72 | — |
| 8 | 1.24 | 1.09 | 13.8 |
| 10 | 1.48 | 1.33 | 11.3 |

### Observaciones

- La pendiente de sustentación \((dC_l/d\alpha)\) calculada por el solver es de ≈ 0.122 por grado, muy cercana al valor teórico de \(2\pi\ \text{rad}^{-1} \approx 0.110\) por grado.
- El desplazamiento vertical entre ambas curvas se debe a las simplificaciones de la teoría de perfiles delgados (que no considera el espesor del perfil).
- Los resultados son consistentes con datos de XFOIL y de la base de datos UIUC Airfoil.

La gráfica de validación se guarda automáticamente en `data/resultados/validacion_naca2412.png`.

---

## Tecnologías

| Herramienta | Uso |
|---|---|
| **Python 3.10+** | Lenguaje principal |
| **NumPy** | Cálculos numéricos y álgebra lineal |
| **SciPy** | Funciones científicas avanzadas |
| **Matplotlib** | Visualización de resultados |
| **Pandas** | (Opcional) Manejo de datos tabulares |
| **pytest** | Pruebas unitarias |

---

## Referencias

1. Katz, J., & Plotkin, A. (2001). *Low-Speed Aerodynamics* (2nd ed.). Cambridge University Press.
2. Abbott, I. H., & Von Doenhoff, A. E. (1949). *Theory of Wing Sections*. Dover Publications.
3. Moran, J. (1984). *An Introduction to Theoretical and Computational Aerodynamics*. Dover Publications.
4. Anderson, J. D. (2010). *Fundamentals of Aerodynamics* (5th ed.). McGraw-Hill.
5. XFOIL: Drela, M. (1989). *XFOIL: An Analysis and Design System for Low Reynolds Number Airfoils*. MIT.

---

## Autores

**Salazar Guzmán, Adriana Zaira**
**Martínez Linares, Marcela Lorena**
**Mejía Martínez, Andrea Alejandra**
**Hernández Martínez, Diego Josué**
**Abarca Gómez, Mauro Jesé**
**Portillo Linares, Jaime Fernando**
**Zelada Salamanca, Emma Leticia**

- Carrera: Ingeniería en Aeronáutica
- Asignatura: Desarrollo de Algoritmos para la Simulación de Sistemas [DAS172]
