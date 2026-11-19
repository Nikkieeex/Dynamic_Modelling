from matplotlib import pyplot as plt
from math import log


def logistic(t, volume, alpha = 0.25, beta = 0.1):
    """
    formule uit: https://www.researchgate.net/publication/378286328_Treatment_Optimization_for_Tumor_Growth_by_Ordinary_Differential_Equations
    Params:
      volume (float):   volume van de tumor (mm^3)
      alpha (float):    gemiddelde cel groei (per dag)
      beta (float):     maximum tumor volume (mm^3)
    Retourneert:
      groei (float):    groei van de tumor (mm^3)
    """
    return (alpha*volume) * (1 - (volume / beta))



def bertalanffy(t, volume, alpha = 0.25, beta = 0.1):
    """
    formule uit: https://www.researchgate.net/publication/378286328_Treatment_Optimization_for_Tumor_Growth_by_Ordinary_Differential_Equations
    Params:
      volume (float):   volume van de tumor (mm^3)
      alpha (float):    gemiddelde cel groei (per dag)
      beta (float):     gemiddelde cel dood (per dag)
    Retourneert:
      groei (float):    groei van de tumor (mm^3)
    """
    return (alpha * volume**(2/3)) - (beta * volume)


def gompertz(t, volume, alpha = 0.25, beta = 0.1):
    """
    formule uit: https://www.researchgate.net/publication/378286328_Treatment_Optimization_for_Tumor_Growth_by_Ordinary_Differential_Equations
    Params:
      volume (float):   volume van de tumor (mm^3)
      alpha (float):    gemiddelde cel groei (per dag)
      beta (float):     maximum tumor volume (mm^3)
    Retourneert:
      groei (float):    groei van de tumor (mm^3)
    """
    # "If the base is not specified, returns the natural logarithm (base e) of x.", dus log is hier ln
    return volume * (alpha - beta * log(x = volume))



def model_tumor_growth(formule, start_volume = 0.0001, N=50, delta_t=1.0, **kwargs):
    """
      formule (functie)  functie voor de specifieke groei formule
      N (int):           aantal integratiestappen
      delta_t (float):   stapgrootte (in dagen)
      **kwargs:          optionele argumenten voor de formule
    Retourneert:
      ts (list[float]):  lijst met tijdstippen (dag)
      Vs (list[float]):  lijst met volumes (mm^3)
    """
    t = 0.0
    ts = [t]
    volume = start_volume
    volumes = [start_volume]
    for _ in range(N):
        groei = formule(t, volume, **kwargs)
        t = t + delta_t
        volume = volume + groei # bij andere delta stapgrootte moet hier wel * delta_t
        ts.append(t)
        volumes.append(volume)
    return ts, volumes


def plot_model(ts, volumes, modelnaam):
    """Plot de resultaten van het groei model.
    Parameters:
      ts (list[float]): lijst met tijdstippen (dag)
      Ss (list[float]): lijst met volumes (mm^3)
    """
    model = f"{modelnaam} model"
    plt.plot(ts, volumes, label = model)
    plt.legend()
    