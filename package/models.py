from matplotlib import pyplot as plt
from math import log

def exponential(volume, c = 0.08):
    """
    exponentiele groei formule
    Params:
      volume (float): volume van de tumor
      c (float): constante
    Return:

    """
    return c * volume


def mendelsohn(volume, c = 0.08, d = 1):
    """
    Mendelsohn groei formule
    Params:
      volume (float): volume van de tumor
      c (float): constante
      d (float): constante
    """ 
    return c * (volume**d)


def logistic(volume, alpha = 1.5, beta = 1500):
    """
    logistische  groei formule
    formule uit: https://www.researchgate.net/publication/378286328_Treatment_Optimization_for_Tumor_Growth_by_Ordinary_Differential_Equations
    Params:
      volume (float):   volume van de tumor
      alpha (float):    cel groei
      beta (float):     maximum tumor volume
    Retourneert:
      groei (float):    groei van de tumor
    """
    if beta <= 0:  # voorkomt delen door nul
        raise ValueError("beta moet groter dan nul zijn")
    return (alpha*volume) * (1 - (volume / beta))
    



def bertalanffy(volume, alpha = 1.5, beta = 0.1):
    """
    Von Bertalanffy groei formule
    formule uit: https://www.researchgate.net/publication/378286328_Treatment_Optimization_for_Tumor_Growth_by_Ordinary_Differential_Equations
    Params:
      volume (float):   volume van de tumor
      alpha (float):    cel groei
      beta (float):     gemiddelde cel dood
    Retourneert:
      groei (float):    groei van de tumor
    """
    return (alpha * volume**(2/3)) - (beta * volume)


def gompertz(volume, alpha = 1.5, beta = 0.1):
    """
    Gompertz groei formule
    formule uit: https://www.researchgate.net/publication/378286328_Treatment_Optimization_for_Tumor_Growth_by_Ordinary_Differential_Equations
    Params:
      volume (float):   volume van de tumor
      alpha (float):    cel groei 
      beta (float):     afname van het cel groei
    Retourneert:
      groei (float):    groei van de tumor
    """
    # "If the base is not specified, returns the natural logarithm (base e) of x.", dus log is hier ln
    volume = max(volume, 1e-10)  # voorkom negatieve waarden 
    return volume * (alpha - (beta * log(volume)))



def model_tumor_growth(formule, start_volume = 0.0001, N=50, delta_t=1.0, **kwargs):
    """
      formule (functie)  functie voor de specifieke groei formule
      N (int):           aantal integratiestappen
      delta_t (float):   stapgrootte
      **kwargs:          optionele argumenten voor de formule
    Retourneert:
      ts (list[float]):  lijst met tijdstippen
      Vs (list[float]):  lijst met volumes
    """
    t = 0.0
    ts = [t]
    volume = start_volume
    volumes = [start_volume]
    for _ in range(N):
        groei = formule(volume, **kwargs)
        t = t + delta_t
        
        volume = volume + (groei * delta_t) # bij andere delta stapgrootte moet hier wel * delta_t
        
        ts.append(t)
        volumes.append(volume)
    return ts, volumes


def plot_model(ts, volumes, modelnaam = None):
    """Plot de resultaten van het groei model.
    Parameters:
      ts (list[float]): lijst met tijdstippen
      volumes (list[float]): lijst met volumes
      modelnaam (string): naam van de te plotten model
    """
    plt.plot(ts, volumes, label =  modelnaam)
    if modelnaam:  # plt.legend() geeft warning als er niks is om in de legend te zetten
      plt.legend()
    