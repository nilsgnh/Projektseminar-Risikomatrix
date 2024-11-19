import numpy as np
from scipy.stats import norm


def simulateRiskMatrix(nSimulations, frequencyMean, frequencyVariance, sevserityMean, severityVariance, matrix):
    
    # Generate random values, ensuring they are between 0 and 1 (normal distribution)
    frequencies = np.random.normal(frequencyMean, np.sqrt(frequencyVariance), nSimulations)
    severities = np.random.normal(sevserityMean, np.sqrt(severityVariance), nSimulations)
    
    # Keep values within [0, 1] range
    frequencies = np.clip(frequencies, 0, 1)
    severities = np.clip(severities, 0, 1)

    priorities = []
    matrix_felder = []

    # Simulation der Risikomatrix
    for i in range(nSimulations):
        freq = frequencies[i]
        sev = severities[i]
        
        # Einordnung in die Risikomatrix
        priority, matrix_feld = matrix.computeDataPoints(freq, sev)
        priorities.append(priority)
        matrix_felder.append(matrix_feld)

    return frequencies, severities, priorities, matrix_felder



def convertPercentToStandardDeviation(certainly, percent):
    # z-Quantil für die gegebene Sicherheit berechnen
    z = norm.ppf((certainly / 100) + (1 - (certainly / 100)) / 2)
    
    # Standardabweichung berechnen
    sigma = (percent / 100) / z
    return sigma



def convertPercentToVariance(certainly, percent):
    # z-Quantil für die gegebene Sicherheit berechnen
    z = norm.ppf((certainly / 100) + (1 - (certainly / 100)) / 2)
    
    # Varianz berechnen
    var = (percent / 100) ** 2 / z ** 2
    return var