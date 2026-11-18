import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def runge_kutta(f, t_start, y_start, dt, n_steps):
    ts = [t_start]
    ys = [y_start]
    y = y_start
    for i in range(n_steps):
        t = t_start + i * dt
        k1 = f(t, y)
        k2 = f(t + 0.5 * dt, y + 0.5 * k1 * dt)
        k3 = f(t + 0.5 * dt, y + 0.5 * k2 * dt)
        k4 = f(t + dt, y + k3 * dt)
        y = y + (k1 + 2 * k2 + 2 * k3 + k4) / 6 * dt
        ts.append(t_start + (i + 1) * dt)
        ys.append(y)
    return ts, ys


# Tijdelijk model, later vervangen door de modellen van me boy sven
c = 0.08


def exponential(t, V):
    return c * V


# Data inlezen
data = pd.read_csv("LM2-4LUC.txt", sep="\t")

# Eén muis kiezen
mouse = data[data["ID"] == 0]
t_data = mouse["Time"].values
V_data = mouse["Observation"].values

# Solver laten rekenen vanaf de eerste meting tot de laatste
dt = 1.0
t_start = t_data[0]
V_start = V_data[0]
n_steps = round((t_data[-1] - t_start) / dt)

ts, Vs = runge_kutta(exponential, t_start, V_start, dt, n_steps)

# Exacte oplossing ter controle
ts_exact = np.linspace(t_start, t_data[-1], 200)
Vs_exact = V_start * np.exp(c * (ts_exact - t_start))
print(f"Fout RK4 aan het eind  {Vs_exact[-1] - Vs[-1]:.6f} mm³")

# Plotten
plt.plot(t_data, V_data, "or", label="Metingen")
plt.plot(ts_exact, Vs_exact, "-k", label="Exact")
plt.plot(ts, Vs, ".:g", label="Runge-Kutta")
plt.xlabel("Tijd (dagen)")
plt.ylabel("Volume (mm³)")
plt.title(f"Muis 0, dt = {dt}")
plt.legend()
plt.grid(True)
plt.show()