import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.colors import ListedColormap
from matplotlib.colors import ListedColormap, BoundaryNorm

# Funktion zur Risikomatrix nach DIN EN 50126
def risk_matrix(frequency, severity):
    # Die 6x4 Risikomatrix
    matrix = [
        [3, 4, 4, 4],   # Häufig
        [2, 3, 4, 4],   # Wahrscheinlich
        [2, 3, 3, 4],   # Gelegentlich
        [1, 2, 3, 3],   # Selten
        [1, 1, 2, 2],   # Unwahrscheinlich
        [1, 1, 1, 1]    # Unvorstellbar
    ]
    
    # Häufigkeit in 6 Kategorien (1 bis 6) einteilen (dabei 1 = häufig, 6 = unwahrscheinlich)
    if(frequency < 1/6):
        freq_cat = 6
    elif(frequency >= 1/6 and frequency < 2/6):
        freq_cat = 5
    elif(frequency >= 2/6 and frequency < 3/6):
        freq_cat = 4
    elif(frequency >= 3/6 and frequency < 4/6):
        freq_cat = 3
    elif(frequency >= 4/6 and frequency < 5/6):
        freq_cat = 2
    elif(frequency >= 5/6):
        freq_cat = 1

    # Ausmaß in 4 Kategorien (1 bis 4) einteilen
    if(severity < 1/4):
        sev_cat = 1
    elif(severity >= 1/4 and severity < 2/4):
        sev_cat = 2
    elif(severity >= 2/4 and severity < 3/4):
        sev_cat = 3
    elif(severity >= 3/4):
        sev_cat = 4
    
    # Rückgabe der Risikoprioritätsstufe und des spezifischen Feldes basierend auf den Kategorien
    matrix_value = matrix[freq_cat-1][sev_cat-1]

    # Index für Matrix-Feld
    matrix_feld = [
        [1, 2, 3, 4],  # Häufig 
        [5, 6, 7, 8],  # Wahrscheinlich
        [9, 10, 11, 12],  #  Gelegentlich
        [13, 14, 15, 16],  # Selten
        [17, 18, 19, 20],  #  Unwahrscheinlich
        [21, 22, 23, 24]   # Unvorstellbar
    ]
    matrix_feld_value = matrix_feld[freq_cat-1][sev_cat-1]

    return matrix_value, matrix_feld_value

# Funktion zur Anpassung der Visualisierung der Prioritätsverteilung
def plot_priority_distribution(priorities):
    # Kategorien zur Beschreibung der Prioritäten
    priority_labels = {1: "Vernachlässigbar", 2: "Tolerabel", 3: "Unerwünscht", 4: "Intolerabel"}
    # Umwandlung in kategorisierte Daten
    priority_categories = pd.Series(priorities).map(priority_labels)

    # Erstellen eines Count DataFrames für die Häufigkeiten
    priority_counts = priority_categories.value_counts().reindex(priority_labels.values()).fillna(0)

    matrix_colors = ["#92D050", "#8EB4E3", "#FFC000", "#FF0000"]
    
    # Erstellen des Balkendiagramms
    plt.figure(figsize=(8, 6))
    ax = sns.barplot(x=priority_counts.index, y=priority_counts.values, hue=priority_counts.index, dodge=False, legend=False, palette=matrix_colors)

    # Hinzufügen von Häufigkeitswerten über den Balken
    for i, count in enumerate(priority_counts.values):
        ax.text(i, count + 0.5, f'{int(count)}', ha='center', va='bottom', fontweight='bold')

    plt.title("Verteilung der Risikoprioritäten in der Simulation")
    plt.xlabel("Priorität")
    plt.ylabel("Häufigkeit")
    #plt.show()

from sklearn.metrics import cohen_kappa_score
import numpy as np

def calculate_quantitative_risk(frequencies, severities):
    # Berechnung des quantitativen Risikowerts als Produkt aus Häufigkeit und Schwere
    quantitative_risks = frequencies * severities
    
    # Ordne die Werte in 4 Kategorien basierend auf Quantilsgrenzen
    quantiles = np.percentile(quantitative_risks, [25, 50, 75])
    quantitative_categories = np.digitize(quantitative_risks, quantiles) + 1  # Kategorien 1 bis 4
    
    return quantitative_categories, quantitative_risks

def evaluate_matrix_with_kappa(qualitative_priorities, quantitative_categories):
    # Berechnung der Kappa-Statistik für die Übereinstimmung
    kappa_score = cohen_kappa_score(qualitative_priorities, quantitative_categories, weights="linear")
    print(f"Kappa-Score für die Übereinstimmung: {kappa_score:.4f}")
    return kappa_score

# Integration in die Simulationsfunktion
def simulate_risk_matrix_with_evaluation(n_simulations, freq_mean, freq_var, sev_mean, sev_var):
    # Generierung der Häufigkeits- und Schwerewerte
    frequencies = np.random.normal(freq_mean, np.sqrt(freq_var), n_simulations)
    severities = np.random.normal(sev_mean, np.sqrt(sev_var), n_simulations)
    frequencies = np.clip(frequencies, 0, 1)
    severities = np.clip(severities, 0, 1)

    # Ergebnisse speichern
    qualitative_priorities = []
    matrix_felder = []

    # Simulation und qualitative Bewertung mit der Matrix
    for i in range(n_simulations):
        freq = frequencies[i]
        sev = severities[i]
        priority, matrix_feld = risk_matrix(freq, sev)
        qualitative_priorities.append(priority)
        matrix_felder.append(matrix_feld)

    # Quantitative Risikokategorien berechnen
    quantitative_categories, quantitative_risks = calculate_quantitative_risk(frequencies, severities)

    # Übereinstimmung der qualitativen Matrix mit den quantitativen Kategorien
    kappa_score = evaluate_matrix_with_kappa(qualitative_priorities, quantitative_categories)

    # Ausgabe der quantitativen Risikoverteilung als zusätzlichen Plot
    plt.figure(figsize=(8, 6))
    sns.histplot(quantitative_risks, bins=20, color="skyblue", edgecolor="black")
    plt.title("Verteilung der berechneten quantitativen Risikoprodukte")
    plt.xlabel("Quantitatives Risiko (Häufigkeit * Schwere)")
    plt.ylabel("Häufigkeit")
    plt.show()

    # Optional: Rückgabe der Ergebnisse
    return kappa_score, qualitative_priorities, quantitative_categories

# Beispiel: Aufruf der erweiterten Simulation
n_simulations = 2000
frequency_mean = 1/3  # oder 5/6
frequency_var = 0.005
severity_mean = 0.5  # oder 0.25
severity_var = 0.005

# Aufruf der erweiterten Simulations- und Bewertungsfunktion
simulate_risk_matrix_with_evaluation(n_simulations, frequency_mean, frequency_var, severity_mean, severity_var)
