"""
Deze functie is volledig overgenomen uit package/test_runge_kutta.py
"""
def runge_kutta(f, t_start, y_start, dt, n_steps, **kwargs):
    """
    Params:
    **kwargs: eventuele extra constanten die de formule nodig heeft
    """
    ts = [t_start]
    ys = [y_start]
    y = y_start
    for i in range(n_steps):
        k1 = f(y, **kwargs)
        k2 = f(y + 0.5 * k1 * dt, **kwargs)
        k3 = f(y + 0.5 * k2 * dt, **kwargs)
        k4 = f(y + k3 * dt, **kwargs)
        y = y + (k1 + 2 * k2 + 2 * k3 + k4) / 6 * dt
        ts.append(t_start + (i + 1) * dt)
        ys.append(y)
    return ts, ys
