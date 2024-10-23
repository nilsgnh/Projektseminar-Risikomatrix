import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Funktion zur Definition der neuen Risikomatrix nach dem Beispielbild
def risk_matrix(frequency, severity):
    # Die 6x4 Risikomatrix (basierend auf der Grafik)
    matrix = [
        [1, 1, 2, 3],  # Unvorstellbar
        [1, 1, 2, 3],  # Unwahrscheinlich
        [1, 2, 2, 3],  # Selten
        [2, 2, 3, 4],  # Gelegentlich
        [2, 3, 4, 4],  # Wahrscheinlich
        [3, 4, 4, 4]   # Häufig
    ]
    
    # Häufigkeit in 6 Kategorien (1 bis 6) einteilen
    freq_cat = int(np.clip(frequency * 6, 1, 6))  # Normiert auf 6 Kategorien
    # Ausmaß in 4 Kategorien (1 bis 4) einteilen
    sev_cat = int(np.clip(severity * 4, 1, 4))    # Normiert auf 4 Kategorien
    
    # Rückgabe der Risikoprioritätsstufe basierend auf den Kategorien
    return matrix[freq_cat-1][sev_cat-1]

# Simulationsfunktion, die den Erwartungswert und die Varianz als Parameter annimmt
def simulate_risk_matrix(n_simulations, freq_mean, freq_var, sev_mean, sev_var):
    # Generierung von Zufallswerten (Normalverteilung) für Häufigkeit und Schwere
    frequencies = np.random.normal(freq_mean, np.sqrt(freq_var), n_simulations)
    severities = np.random.normal(sev_mean, np.sqrt(sev_var), n_simulations)
    
    # Sicherstellen, dass die Werte im Bereich [0, 1] bleiben (nach der Normalverteilung)
    frequencies = np.clip(frequencies, 0, 1)
    severities = np.clip(severities, 0, 1)

    # Liste zur Speicherung der Risikoprioritäten
    priorities = []

    # Simulation und Einordnung in die Risikomatrix
    for i in range(n_simulations):
        freq = frequencies[i]
        sev = severities[i]
        
        # Einordnung in die Risikomatrix
        priority = risk_matrix(freq, sev)
        priorities.append(priority)

    # Auswertung der Prioritätsverteilung
    unique, counts = np.unique(priorities, return_counts=True)

    # Ausgabe der Verteilung der Risikoprioritäten
    print("Prioritätsverteilung:")
    for u, c in zip(unique, counts):
        print(f"Priorität {u}: {c} mal zugeordnet")

    # Visualisierung der Prioritätsverteilung
    sns.histplot(priorities, bins=range(1, 6), kde=False)
    plt.title("Verteilung der Risikoprioritäten in der Simulation")
    plt.xlabel("Priorität")
    plt.ylabel("Häufigkeit")
    plt.show()

    # Scatterplot der simulierten Häufigkeit und Schwere
    plt.figure(figsize=(10, 6))
    plt.scatter(frequencies, severities, c=priorities, cmap='RdYlGn', alpha=0.6, edgecolor='black')
    plt.colorbar(label='Risikopriorität')

    # Markierung des Erwartungswerts auf der Risikomatrix
    plt.scatter([freq_mean], [sev_mean], color='blue', s=200, label='Erwartungswert', edgecolor='black')

    # Titel und Achsenbeschriftungen
    plt.title('Scatterplot der simulierten Häufigkeit und Schwere\nmit Erwartungswert-Markierung')
    plt.xlabel('Normierte Häufigkeit (0-1)')
    plt.ylabel('Normierte Schwere (0-1)')
    plt.legend()
    plt.grid(True)
    plt.show()

# Beispiel: Aufruf der Simulation mit benutzerdefinierten Parametern
n_simulations = 2000
frequency_mean = 0.3  # Erwartungswert für Häufigkeit (im Bereich 0 bis 1)
frequency_var = 0.05  # Varianz für Häufigkeit
severity_mean = 0.2   # Erwartungswert für Schwere (im Bereich 0 bis 1)
severity_var = 0.05   # Varianz für Schwere

# Aufruf der Simulationsfunktion mit benutzerdefinierten Parametern
simulate_risk_matrix(n_simulations, frequency_mean, frequency_var, severity_mean, severity_var)
