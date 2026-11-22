"""
Deze functie is grotendeels overgenomen uit package/workshop3.py
"""
import numpy as np
from package.test_runge_kutta import runge_kutta


def MSE(t_data, V_data, model, dt = 1, **params):
    """
    Berekent hoe ver de modelcurve van de metingen afligt.
    Params:
      t_data(iterable): data voor de x-as (tijd)
      V_data(iterable): data voor de y-as (volume)
      model(function): een model uit models.py
      dt(int): aantal punten per stap (nodig voor runge_kutta)
      **params: nodige params voor het model (bv. alpha en beta)
    Retourneert:
      mse (float):    mean squared error
    """
    t_start, t_end = t_data[0], t_data[-1]
    V_start = V_data[0]
    n_steps = round((t_end - t_start) / dt)
    ts, Vs = runge_kutta(model, t_start, V_start, dt, n_steps, **params)

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
