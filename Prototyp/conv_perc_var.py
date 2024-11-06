from scipy.stats import norm

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

# Test-Aufruf
certainly = 90  # Sicherheit in Prozent
percent = 1    # Prozentuale Abweichung vom Erwartungswert
sigma = conv_perc_std(certainly, percent)
print(f"Standardabweichung: {sigma}")
var = conv_perc_var(certainly, percent)
print(f"Varianz: {var}")
