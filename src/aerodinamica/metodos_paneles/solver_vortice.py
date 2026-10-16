"""
Módulo para el método de paneles de fuente-vórtice.
Incluye la Condición de Kutta para generar sustentación.

Referencias:
- Katz & Plotkin, "Low-Speed Aerodynamics", 2nd ed., 2001.
- Moran, "An Introduction to Theoretical and Computational Aerodynamics", 1984.
"""

import numpy as np


class MetodoPanelesVortice:
    def __init__(self, x, y, v_inf=1.0, alpha_deg=0.0):
        self.x = np.asarray(x, dtype=float)
        self.y = np.asarray(y, dtype=float)
        self.v_inf = v_inf
        self.alpha = np.deg2rad(alpha_deg)
        self.N = len(self.x) - 1

        # Geometría de cada panel
        self.dx = np.diff(self.x)
        self.dy = np.diff(self.y)
        self.s = np.sqrt(self.dx**2 + self.dy**2)
        self.theta = np.arctan2(self.dy, self.dx)
        self.cos_t = np.cos(self.theta)
        self.sin_t = np.sin(self.theta)

        # Puntos de control (punto medio)
        self.xc = 0.5 * (self.x[:-1] + self.x[1:])
        self.yc = 0.5 * (self.y[:-1] + self.y[1:])

        # Normal exterior (contorno CCW): n = (sin θ, -cos θ)
        self.nx = self.sin_t
        self.ny = -self.cos_t

        self.sigma = None
        self.gamma = None
        self.vt = None
        self.cp = None
        self.Cl = None

    def _influencia(self, i, j, tipo):
        """
        Influencia del panel j (densidad unitaria) en el punto i.
        Devuelve (V_n_outward, V_t_along_panel) en componentes globales.
        """
        # Autoinfluencia
        if i == j:
            if tipo == 'source':
                return 0.5, 0.0
            else:
                return 0.0, 0.0

        # Panel j: punto inicio (xj1, yj1) -> punto fin (xj2, yj2)
        xj1, yj1 = self.x[j], self.y[j]
        xj2, yj2 = self.x[j + 1], self.y[j + 1]
        sj = self.s[j]

        # Punto medio del panel j
        xm = 0.5 * (xj1 + xj2)
        ym = 0.5 * (yj1 + yj2)

        # Posición del punto i respecto al centro del panel j
        xr = self.xc[i] - xm
        yr = self.yc[i] - ym

        # Rotar al sistema local del panel j (panel centrado en origen)
        xl = xr * self.cos_t[j] + yr * self.sin_t[j]
        yl = -xr * self.sin_t[j] + yr * self.cos_t[j]

        # Distancias a los extremos del panel
        r1 = np.sqrt((xl + sj / 2.0)**2 + yl**2)
        r2 = np.sqrt((xl - sj / 2.0)**2 + yl**2)

        if r1 < 1e-12 or r2 < 1e-12:
            return 0.0, 0.0

        # Ángulos subtendidos por los extremos del panel
        t1 = np.arctan2(yl, xl + sj / 2.0)
        t2 = np.arctan2(yl, xl - sj / 2.0)

        if tipo == 'source':
            # Fuente: u* = (1/2π) ln(r1/r2), v* = (1/2π)(t2 - t1)
            u_loc = (1.0 / (2.0 * np.pi)) * np.log(r1 / r2)
            v_loc = (1.0 / (2.0 * np.pi)) * (t2 - t1)
        else:  # vortex
            # Vórtice: u* = -(1/2π)(t2 - t1), v* = -(1/2π) ln(r2/r1)
            u_loc = -(1.0 / (2.0 * np.pi)) * (t2 - t1)
            v_loc = -(1.0 / (2.0 * np.pi)) * np.log(r2 / r1)

        # (u_loc, v_loc) están en el sistema local del panel j:
        #   u_loc → dirección del panel t_j = (cos θ_j, sin θ_j)
        #   v_loc → perpendicular n_perp_j = (-sin θ_j, cos θ_j)
        # Componentes globales:
        #   V = u_loc * t_j + v_loc * n_perp_j
        # Proyectamos sobre t_i y n_i del panel i:
        vn_i = (u_loc * (self.cos_t[j] * self.nx[i] + self.sin_t[j] * self.ny[i]) +
                v_loc * (-self.sin_t[j] * self.nx[i] + self.cos_t[j] * self.ny[i]))
        vt_i = (u_loc * (self.cos_t[j] * self.cos_t[i] + self.sin_t[j] * self.sin_t[i]) +
                v_loc * (-self.sin_t[j] * self.cos_t[i] + self.cos_t[j] * self.sin_t[i]))

        return vn_i, vt_i

    def resolver(self):
        N = self.N
        A = np.zeros((N + 1, N + 1))
        b = np.zeros(N + 1)

        # 1. Condiciones de no penetración (N ecuaciones)
        for i in range(N):
            for j in range(N):
                vn_s, _ = self._influencia(i, j, 'source')
                A[i, j] = vn_s

                vn_v, _ = self._influencia(i, j, 'vortex')
                A[i, N] += vn_v

            b[i] = -self.v_inf * (np.cos(self.alpha) * self.nx[i] +
                                   np.sin(self.alpha) * self.ny[i])

        # 2. Condición de Kutta (última ecuación): Vt_0 + Vt_{N-1} = 0
        i_te_sup = 0
        i_te_inf = N - 1

        for j in range(N):
            _, vt_s_sup = self._influencia(i_te_sup, j, 'source')
            _, vt_s_inf = self._influencia(i_te_inf, j, 'source')
            A[N, j] = vt_s_sup + vt_s_inf

            _, vt_v_sup = self._influencia(i_te_sup, j, 'vortex')
            _, vt_v_inf = self._influencia(i_te_inf, j, 'vortex')
            A[N, N] += vt_v_sup + vt_v_inf

        # RHS de la condición de Kutta
        vt_libre_sup = self.v_inf * (np.cos(self.alpha) * self.cos_t[i_te_sup] +
                                      np.sin(self.alpha) * self.sin_t[i_te_sup])
        vt_libre_inf = self.v_inf * (np.cos(self.alpha) * self.cos_t[i_te_inf] +
                                      np.sin(self.alpha) * self.sin_t[i_te_inf])
        b[N] = -(vt_libre_sup + vt_libre_inf)

        # Resolver el sistema lineal
        sol = np.linalg.solve(A, b)
        self.sigma = sol[:N]
        self.gamma = sol[N]

    def calcular_velocidades(self):
        N = self.N
        self.vt = np.zeros(N)

        for i in range(N):
            vt_libre = self.v_inf * (np.cos(self.alpha) * self.cos_t[i] +
                                      np.sin(self.alpha) * self.sin_t[i])
            vt_paneles = 0.0
            for j in range(N):
                _, vt_s = self._influencia(i, j, 'source')
                vt_paneles += vt_s * self.sigma[j]

                _, vt_v = self._influencia(i, j, 'vortex')
                vt_paneles += vt_v * self.gamma

            self.vt[i] = vt_libre + vt_paneles

        # Cp
        self.cp = 1.0 - (self.vt / self.v_inf)**2

        # Cl (Kutta-Joukowski): Γ = γ · perímetro
        Gamma = self.gamma * np.sum(self.s)
        self.Cl = -2.0 * Gamma / (self.v_inf * 1.0)

    def ejecutar(self):
        self.resolver()
        self.calcular_velocidades()
        return self.cp, self.Cl
