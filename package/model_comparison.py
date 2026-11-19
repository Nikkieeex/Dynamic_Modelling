from inspect import signature
from math import log


def BIC(mse, n , function):
    """
    Berekent de Bayes Information Criterion (BIC) voor een model.
    Parameters:
        mse(float): Mean Squared Error (MSE) van het model.
        n(int): het aantal datapunten waarvoor de fit gemaakt wordt.
        function(function): functie gebruikt voor het model.
    Retouneert:
        De BIC voor het model, als float.
    """
    k = len(signature(function).parameters)  # k = het aantal parameters in het model
    return n * log(mse) + k * log(n)


def AIC(mse, n, function):
    """
    Berekent de Akaike Information Criterion (AIC) voor een model.
    Parameters:
        mse(float): Mean Squared Error (MSE) van het model.
        n(int): het aantal datapunten waarvoor de fit gemaakt wordt.
        function(function): functie gebruikt voor het model.
    Retouneert:
        De BIC voor het model, als float.
    """
    k = len(signature(function).parameters)  # k = het aantal parameters in het model
    return n * log(mse) + k * 2.0


def AICc(mse, n, function):
    """
    Berekent de Akaike Information Criterion corrected (AICc) voor een model.
    Parameters:
        mse(float): Mean Squared Error (MSE) van het model.
        n(int): het aantal datapunten waarvoor de fit gemaakt wordt.
        function(function): functie gebruikt voor het model.
    Retouneert:
        De AICc voor het model, als float.
    """
    k = len(signature(function).parameters)  # k = het aantal parameters in het model
    return n * log(mse) + k * 2.0 * n/(n-k-1)
