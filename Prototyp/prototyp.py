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

# Simulationsfunktion
def simulate_risk_matrix(n_simulations, freq_mean, freq_var, sev_mean, sev_var):
    # Generierung von Zufallswerten, aber nur zwischen 0 und 1
    frequencies = np.random.normal(freq_mean, np.sqrt(freq_var), n_simulations)
    severities = np.random.normal(sev_mean, np.sqrt(sev_var), n_simulations)
    
    # Werte im Bereich [0, 1] halten
    frequencies = np.clip(frequencies, 0, 1)
    severities = np.clip(severities, 0, 1)

    # Ergebnisse speichern
    priorities = []
    matrix_felder = []

    # Simulation der Risikomatrix
    for i in range(n_simulations):
        freq = frequencies[i]
        sev = severities[i]
        
        # Einordnung in die Risikomatrix
        priority, matrix_feld = risk_matrix(freq, sev)
        priorities.append(priority)
        matrix_felder.append(matrix_feld)

    # Zählung, wie oft jedes Feld ausgewählt wurde
    feld_counts = np.zeros(24, dtype=int)  # Für 24 Felder der Matrix
    unique_feld, counts_feld = np.unique(matrix_felder, return_counts=True)
    feld_counts[unique_feld - 1] = counts_feld  # Zählung auf die richtigen Felder verteilen

    # Risikomatrix in Tabellenform mit Pandas DataFrame erstellen
    rows, cols = 6, 4
    matrix_reshaped = feld_counts.reshape(rows, cols)

    # Beschriftungen hinzufügen
    zeilen_beschriftungen = ["Häufig", "Wahrscheinlich", "Gelegentlich", "Selten", "Unwahrscheinlich", "Unvorstellbar"]
    spalten_beschriftungen = ["Unbedeutend", "Marginal", "Kritisch", "Katastrophal"]
    risiko_matrix_df = pd.DataFrame(matrix_reshaped, index=zeilen_beschriftungen, columns=spalten_beschriftungen)

    # Ausgabe der Verteilung der Risikoprioritäten
    print("Prioritätsverteilung:")
    for u, c in pd.Series(priorities).value_counts().items():
        if(u == 1):
            print(f"- Vernachlässigbar: {c} Mal")
        elif(u == 2):
            print(f"- tolerabel: {c} Mal")
        elif(u == 3):
            print(f"- unerwünscht: {c} Mal")
        elif(u == 4):
            print(f"- intolerabel: {c} Mal")
    
    print("")

    # Ausgabe der spezifischen Felder als Tabelle
    print("\nVerteilung der spezifischen Felder in der Risikomatrix:")
    print(risiko_matrix_df)

    # Visualisierung der Prioritätsverteilung
    plot_priority_distribution(priorities)

    # Visualisierung der Häufigkeit der Felder in der Risikomatrix als Heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(risiko_matrix_df, annot=True, cmap="YlGnBu", cbar_kws={'label': 'Anzahl'})
    plt.title("Absolute Häufigkeit der spezifischen Felder in der Risikomatrix")
    plt.xlabel("Schwere")
    plt.ylabel("Häufigkeit")
    #plt.show()

    # Scatterplot der simulierten Häufigkeit und Schwere
    background_colors = ['lightgreen', 'lightblue', 'moccasin', 'lightcoral']
    risk_colors = ["#92D050", "#8EB4E3", "#FFC000", "#FF0000"]

    cmap_background = ListedColormap(background_colors)
    cmap_risk = ListedColormap(risk_colors)

    risk_matrix_vals = np.array([
        [3, 4, 4, 4], 
        [2, 3, 4, 4],  
        [2, 3, 3, 4],  
        [1, 2, 3, 3],  
        [1, 1, 2, 2], 
        [1, 1, 1, 1] 
    ])

    plt.figure(figsize=(10, 6))

    # Erzeugung des Matrix-Hintergrunds
    X = np.linspace(0, 1, risk_matrix_vals.shape[1] + 1)  # 5 values for columns (4 categories)
    Y = np.linspace(0, 1, risk_matrix_vals.shape[0] + 1)  # 7 values for rows (6 categories)
    
    # Plot the matrix as a background using pcolormesh with subtle colors
    p = plt.pcolormesh(X, Y, risk_matrix_vals[::-1], cmap=cmap_background, edgecolors='k', shading='auto', alpha=0.5)

    # Normierung für die Farben der Plots
    norm = BoundaryNorm([1, 2, 3, 4, 5], cmap_risk.N)

    scatter = plt.scatter(severities, frequencies, c=priorities, cmap=cmap_risk, norm=norm, alpha=0.6, edgecolor='black')
    
    # Erwartungswert plot
    plt.scatter([sev_mean], [freq_mean], color='lightgrey', s=200, label='Erwartungswert', edgecolor='black')

    plt.title('Scatterplot der simulierten Häufigkeit und Schwere')
    plt.xlabel('Normierte Schwere (0-1)')
    plt.ylabel('Normierte Häufigkeit (0-1)')

    plt.xlim(0, 1)
    plt.ylim(0, 1)

    plt.legend()
    plt.grid(False)
    plt.show()

# Beispiel: Aufruf der Simulation
n_simulations = 2000
frequency_mean = 0.333
frequency_var = 0.005
severity_mean = 0.5
severity_var = 0.005

# Aufruf der Simulationsfunktion
simulate_risk_matrix(n_simulations, frequency_mean, frequency_var, severity_mean, severity_var)