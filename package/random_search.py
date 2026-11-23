"""
Deze functie is grotendeels overgenomen uit package/workshop3.py
"""
from package.mse import MSE
from random import gauss
from inspect import signature, Parameter


def random_search(t_data, V_data, model, dt = 1, **user_params):
    """
    Probeert de beste parameters te bepalen voor een model op 
    basis van random search (Monte Carlo).
    Params:
        t_data(iterable): input data voor de x-as (tijd)
        V_data(iterable): input data voor de y-as (volume)
        model(function): model uit models.py
        dt(int): aantal stappen tussen de punten, nodig voor runge_kutta (default = 1)
        **user_params: nodige parameters voor het model (bijvoorbeeld alpha en beta)
    Retouneert:
        MSE(float): MSE waarde voor het model
        params(dict[string: float]): door random search bepaalde parameters voor het gekozen model met de input data
    """

    # gebruikt de default waarden van de modellen als gebruiker niks meegeeft
    defaults = get_defaults(model)
    # als de gebruiker zelf andere parameters meegeeft voor het model, overschrijf deze dan van de defaults
    for param_name, value in user_params.items():
        defaults[param_name] = value

    params = defaults.copy()
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


def get_defaults(function):
    """
    Maak een dictionary met als keys de parameter namen, en als values de defaults
    Gebruikt alleen parameters die een default waarde hebben.
    Params:
        function(function): de input functie
    Return:
        dict[string: any]: dict met parameter namen als keys, en de defaults als values

    """
    # deels overgenomen van: https://stackoverflow.com/a/54009257
    model_params_dict = signature(function).parameters
    defaults = {}
    for param_name, param_value in model_params_dict.items():
        param_default = param_value.default
        # if the parameters has a default
        if param_default != Parameter.empty:
            defaults[param_name] = param_default

    return defaults
