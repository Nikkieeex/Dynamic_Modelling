"""
Deze functie is grotendeels overgenomen uit package/workshop3.py
"""
from package.mse import MSE
from random import gauss

def random_search(t_data, V_data, model, dt = 1, **start_params):
    """
    Probeert de beste parameters te bepalen voor een model op 
    basis van random search (Monte Carlo).
    Params:
        t_data(iterable): input data voor de x-as (tijd)
        V_data(iterable): input data voor de y-as (volume)
        model(function): model uit models.py
        dt(int): aantal stappen tussen de punten, nodig voor runge_kutta (default = 1)
        **start_params: nodige parameters voor het model (bijvoorbeeld alpha en beta)
    Retouneert:
        MSE(float): MSE waarde voor het model
        params(dict[string: float]): door random search bepaalde parameters voor het gekozen model met de input data
    """
    params = start_params.copy()
    mse = MSE(t_data, V_data, model, dt, **params)
    tries = 0
    while tries < 1000:
        tries += 1
        new_params = {key: val + gauss(0, 0.01) for key, val in params.items()}
        new_mse = MSE(t_data, V_data, model, dt, **new_params)
        if new_mse < mse:
            params = new_params
            mse = new_mse
            tries = 0

    return mse, params
