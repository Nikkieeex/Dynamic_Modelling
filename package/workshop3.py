import numpy as np
import pandas as pd
from random import gauss
from matplotlib import pyplot as plt

from package.models import bertalanffy
from package.test_runge_kutta import runge_kutta

# Data van muis 33
data = pd.read_csv("test_data/LM2-4LUC.txt", sep="\t")
# mouse = mouse[mouse["Observation"] > 0] er zitten nul waarden in de data idk of het zinvol is om die eruit te halen
mouse = data[data["ID"] == 33]
t_data = mouse["Time"].values
V_data = mouse["Observation"].values

dt = 1.0
t_start = t_data[0]
V_start = V_data[0]
n_steps = round((t_data[-1] - t_start) / dt)


def MSE(alpha, beta):
    """
    Berekent hoe ver de modelcurve van de metingen afligt.
    Params:
      alpha (float):  gemiddelde cel groei (per dag)
      beta (float):   gemiddelde cel dood (per dag)
    Retourneert:
      mse (float):    mean squared error
    """
    ts, Vs = runge_kutta(bertalanffy, t_start, V_start, dt, n_steps, alpha=alpha, beta=beta)

    # Bij rare parameters kan het volume negatief of complex worden, dat is dan een slechte fit
    if any(isinstance(V, complex) or not np.isfinite(V) for V in Vs):
        return float("inf")

    # Modelwaarden op de tijdstippen van de metingen
    V_model = np.interp(t_data, ts, Vs)

    sum_squared_error = 0.0
    for V_meting, V_mod in zip(V_data, V_model):
        error = V_meting - V_mod
        sum_squared_error += error * error
    return sum_squared_error / len(V_data)


start_params = {"alpha": 1.65, "beta": 0.1}  # Startwaarden uit workshop 1
print(f"MSE met startwaarden = {MSE(**start_params):.2f}")


# Random search
params = start_params.copy()
mse = MSE(**params)
tries = 0
while tries < 1000:
    tries += 1
    new_params = {key: val + gauss(0, 0.01) for key, val in params.items()}
    new_mse = MSE(**new_params)
    if new_mse < mse:
        params = new_params
        mse = new_mse
        tries = 0

params_random = params
mse_random = mse
print("Random search:")
for key, val in params_random.items():
    print(f"* {key:>5s} = {val:9.6f}")
print(f"MSE = {mse_random:.2f}")


# Direct search (Hooke & Jeeves)
params = start_params.copy()
deltas = {key: 0.1 for key in params}
mse = MSE(**params)
while max(abs(delta) for delta in deltas.values()) > 1e-6:
    for key in params:
        new_params = params.copy()

        # Probeer de parameter te verhogen
        new_params[key] = params[key] + deltas[key]
        new_mse = MSE(**new_params)
        if new_mse < mse:
            params, mse = new_params, new_mse
            deltas[key] *= 1.2
            continue

        # Probeer de parameter te verlagen
        new_params[key] = params[key] - deltas[key]
        new_mse = MSE(**new_params)
        if new_mse < mse:
            params, mse = new_params, new_mse
            deltas[key] *= -1.2
            continue

        # Verklein de stapgrootte
        deltas[key] *= 0.2

params_direct = params
mse_direct = mse
print("Direct search:")
for key, val in params_direct.items():
    print(f"* {key:>5s} = {val:9.6f}")
print(f"MSE = {mse_direct:.2f}")


# Vergelijken met de data
plt.plot(t_data, V_data, "or", label="Metingen")
for naam, p in [("Workshop 1", start_params), ("Random search", params_random), ("Direct search", params_direct)]:
    ts, Vs = runge_kutta(bertalanffy, t_start, V_start, dt, n_steps, **p)
    plt.plot(ts, Vs, label=f"{naam} (MSE = {MSE(**p):.0f})")
plt.xlabel("Tijd (dagen)")
plt.ylabel("Volume (mm³)")
plt.title("Muis 33")
plt.grid(True)
plt.legend()
plt.show()