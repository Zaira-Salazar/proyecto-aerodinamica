"""
Módulo para el método de paneles de fuente (Source Panel Method).
Calcula la distribución de velocidades y presiones para flujo potencial
incompresible alrededor de un perfil aerodinámico.

Referencia: Katz & Plotkin, "Low-Speed Aerodynamics", 2001.
"""

import numpy as np


class MetodoPanelesFuente:
    """
    Implementa el método de paneles de fuente para un cuerpo 2D.
    """

    def __init__(self, x_contorno: np.ndarray, y_contorno: np.ndarray,
                 v_inf: float = 1.0, alpha_deg: float = 0.0):
        """
        Parámetros
        ----------
        x_contorno, y_contorno : np.ndarray
            Coordenadas del contorno del perfil (cerrado).
        v_inf : float
            Velocidad del flujo libre.
        alpha_deg : float
            Ángulo de ataque en grados.
        """
        self.x = np.asarray(x_contorno, dtype=float)
        self.y = np.asarray(y_contorno, dtype=float)
        self.v_inf = v_inf
        self.alpha = np.deg2rad(alpha_deg)

        # Validaciones básicas
        if len(self.x) != len(self.y):
            raise ValueError("x_contorno e y_contorno deben tener la misma longitud.")
        if len(self.x) < 3:
            raise ValueError("Se necesitan al menos 3 puntos para definir un perfil.")

        # Puntos de control (punto medio de cada panel) y normales
        self.xc, self.yc = self._puntos_control()
        self.nx, self.ny = self._normales()
        self.s = self._longitudes_panel()

        # Matriz de influencia y vector de términos independientes
        self.A = None
        self.b = None
        self.sigma = None
        self.vt = None
        self.cp = None

    def _puntos_control(self):
        """Calcula el punto medio (de control) de cada panel."""
        xc = 0.5 * (self.x[:-1] + self.x[1:])
        yc = 0.5 * (self.y[:-1] + self.y[1:])
        return xc, yc

    def _longitudes_panel(self):
        """Calcula la longitud de cada panel."""
        return np.sqrt(np.diff(self.x)**2 + np.diff(self.y)**2)

    def _normales(self):
        """Calcula el vector normal unitario de cada panel (apuntando hacia afuera)."""
        dx = np.diff(self.x)
        dy = np.diff(self.y)
        s = np.sqrt(dx**2 + dy**2)
        # La normal apunta hacia afuera del cuerpo (asumiendo contorno en sentido horario)
        nx = dy / s
        ny = -dx / s
        return nx, ny

    def _influencia_fuente(self, i, j):
        """
        Calcula la influencia del panel j sobre el punto de control del panel i.
        Retorna la velocidad normal y tangencial inducida por una fuente unitaria.
        """
        # Coordenadas relativas
        x_rel = self.xc[i] - self.x[j]
        y_rel = self.yc[i] - self.y[j]

        # Ángulo del panel j
        theta_j = np.arctan2(self.y[j+1] - self.y[j], self.x[j+1] - self.x[j])

        # Rotar al sistema local del panel j
        x_local = x_rel * np.cos(theta_j) + y_rel * np.sin(theta_j)
        y_local = -x_rel * np.sin(theta_j) + y_rel * np.cos(theta_j)

        # Longitud del panel
        sj = self.s[j]

        # Fórmulas analíticas de influencia de una fuente uniforme
        r1 = np.sqrt(x_local**2 + y_local**2)
        r2 = np.sqrt((x_local - sj)**2 + y_local**2)

        # Evitar divisiones por cero si el punto está muy cerca
        if r1 < 1e-12 or r2 < 1e-12:
            return 0.0, 0.0

        # Velocidad normal y tangencial en coordenadas locales
        vn_local = (1.0 / (2.0 * np.pi)) * np.log(r2 / r1)
        vt_local = (1.0 / (2.0 * np.pi)) * (np.arctan2(y_local, x_local - sj) - np.arctan2(y_local, x_local))

        # Rotar de vuelta al sistema global
        vn_global = vn_local * np.cos(theta_j) - vt_local * np.sin(theta_j)
        vt_global = vn_local * np.sin(theta_j) + vt_local * np.cos(theta_j)

        return vn_global, vt_global

    def resolver(self):
        """Construye la matriz de influencia y resuelve el sistema lineal."""
        n_paneles = len(self.s)
        self.A = np.zeros((n_paneles, n_paneles))
        self.b = np.zeros(n_paneles)

        # Llenar la matriz de influencia
        for i in range(n_paneles):
            for j in range(n_paneles):
                if i == j:
                    # Autoinfluencia de un panel sobre sí mismo (solo componente normal)
                    self.A[i, j] = 0.5
                else:
                    vn, _ = self._influencia_fuente(i, j)
                    self.A[i, j] = vn

            # Término independiente: flujo libre proyectado sobre la normal
            self.b[i] = -self.v_inf * (np.cos(self.alpha) * self.nx[i] + np.sin(self.alpha) * self.ny[i])

        # Resolver el sistema lineal A * sigma = b
        self.sigma = np.linalg.solve(self.A, self.b)

    def calcular_velocidades(self):
        """Calcula la velocidad tangencial y el coeficiente de presión en cada panel."""
        n_paneles = len(self.s)
        self.vt = np.zeros(n_paneles)

        for i in range(n_paneles):
            # Contribución del flujo libre (tangencial)
            vt_libre = self.v_inf * (-np.sin(self.alpha) * self.nx[i] + np.cos(self.alpha) * self.ny[i])
            
            # Contribución de todas las fuentes
            vt_fuentes = 0.0
            for j in range(n_paneles):
                if i != j:
                    _, vt = self._influencia_fuente(i, j)
                    vt_fuentes += vt * self.sigma[j]
                else:
                    # Autoinfluencia tangencial es cero para paneles de fuente
                    vt_fuentes += 0.0

            self.vt[i] = vt_libre + vt_fuentes

        # Coeficiente de presión: Cp = 1 - (Vt / V_inf)^2
        self.cp = 1.0 - (self.vt / self.v_inf)**2

    def ejecutar(self):
        """Ejecuta todo el flujo de cálculo."""
        self.resolver()
        self.calcular_velocidades()
        return self.cp
        