import numpy as np
from scipy.stats import norm

def generatePoints(nSimulations, frequencyMean, frequencyVariance, severityMean, severityVariance):
    
    # Generate random values, ensuring they are between 0 and 1 (normal distribution)
    frequencies = np.random.normal(frequencyMean, np.sqrt(frequencyVariance), nSimulations)
    severities = np.random.normal(severityMean, np.sqrt(severityVariance), nSimulations)
        
    frequencies = np.clip(frequencies, 0, 1)
    severities = np.clip(severities, 0, 1)

    return frequencies, severities
    

def simulateRiskMatrix(frequencies, severities, matrix):
    priorities = []
    fieldNum = []
    
    # Simulation der Risikomatrix
    for i in range(len(frequencies)):
        freq = frequencies[i]
        sev = severities[i]
        
        # Einordnung in die Risikomatrix
        priority, matrix_feld = matrix.computeDataPoint(freq, sev)
        priorities.append(priority)
        fieldNum.append(matrix_feld)

    return priorities, fieldNum



def conv_perc_std(certainly, percent):
    # z-Quantil für die gegebene Sicherheit berechnen
    z = norm.ppf((certainly / 100) + (1 - (certainly / 100)) / 2)
    
    # Standardabweichung berechnen
    sigma = (percent / 100) / z
    return sigma


def conv_perc_var(certainly, percent):
    # z-Quantil für die gegebene Sicherheit berechnen
    z = norm.ppf((certainly / 100) + (1 - (certainly / 100)) / 2)
    
    # Varianz berechnen
    var = (percent / 100) ** 2 / z ** 2
    return var