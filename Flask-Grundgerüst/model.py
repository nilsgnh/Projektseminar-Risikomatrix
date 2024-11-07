import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend to avoid GUI

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.colors import ListedColormap
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io


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




def plot_priority_distribution(priorities):

    priority_labels = {1: "Vernachlässigbar", 2: "Tolerabel", 3: "Unerwünscht", 4: "Intolerabel"}
    priority_categories = pd.Series(priorities).map(priority_labels)
    priority_counts = priority_categories.value_counts().reindex(priority_labels.values()).fillna(0)
    matrix_colors = ["#92D050", "#8EB4E3", "#FFC000", "#FF0000"]

    fig = Figure(figsize=(8, 6))
    FigureCanvas(fig)
    ax = fig.add_subplot(111)

    sns.barplot(
        ax=ax, x=priority_counts.index, y=priority_counts.values, 
        hue=priority_counts.index, 
        palette=matrix_colors, dodge=False, legend=False
    )

    # Add value labels on the bars
    for i, count in enumerate(priority_counts.values):
        ax.text(i, count + 0.5, f'{int(count)}', ha='center', va='bottom', fontweight='bold')

    # Set labels and title
    ax.set_title("Verteilung der Risikoprioritäten in der Simulation")
    ax.set_xlabel("Priorität")
    ax.set_ylabel("Häufigkeit")

    # Save the plot to a StringIO buffer in SVG format
    img = io.StringIO()
    fig.savefig(img, format='svg')
    img.seek(0)

    # Extract only the <svg> part of the image
    svg_img = '<svg' + img.getvalue().split('<svg')[1]
    
    return svg_img




def heatmap_svg(matrix_felder):

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

    # Create a new figure
    fig = Figure(figsize=(10, 6))
    FigureCanvas(fig)  # Attach the canvas to the figure for rendering
    ax = fig.add_subplot(111)

    # Create the heatmap on the given axis
    sns.heatmap(risiko_matrix_df, annot=True, cmap="YlGnBu", cbar_kws={'label': 'Anzahl'}, ax=ax)
    ax.set_title("Absolute Häufigkeit der spezifischen Felder in der Risikomatrix")
    ax.set_xlabel("Schwere")
    ax.set_ylabel("Häufigkeit")

    # Save the plot to a StringIO buffer in SVG format
    img = io.StringIO()
    fig.savefig(img, format='svg')
    img.seek(0)

    # Extract only the <svg> part of the image
    svg_img = '<svg' + img.getvalue().split('<svg')[1]
    
    return svg_img



def simulate_risk_matrix(n_simulations, freq_mean, freq_var, sev_mean, sev_var):
    # Generate random values, ensuring they are between 0 and 1 (normal distribution)
    frequencies = np.random.normal(freq_mean, np.sqrt(freq_var), n_simulations)
    severities = np.random.normal(sev_mean, np.sqrt(sev_var), n_simulations)
    
    # Keep values within [0, 1] range
    frequencies = np.clip(frequencies, 0, 1)
    severities = np.clip(severities, 0, 1)

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

    return frequencies, severities, priorities, matrix_felder


def scatter_svg(sev_mean, freq_mean, priorities, severities, frequencies):
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

    # Create a new figure and attach a canvas for rendering
    fig = Figure(figsize=(10, 6))
    FigureCanvas(fig)
    ax = fig.add_subplot(111)

    # Create the matrix background
    X = np.linspace(0, 1, risk_matrix_vals.shape[1] + 1)  # 5 values for columns (4 categories)
    Y = np.linspace(0, 1, risk_matrix_vals.shape[0] + 1)  # 7 values for rows (6 categories)

    # Plot the matrix as a background using pcolormesh with subtle colors
    ax.pcolormesh(X, Y, risk_matrix_vals[::-1], cmap=cmap_background, edgecolors='k', shading='auto', alpha=0.5)

    # Normalization for scatter plot colors
    norm = BoundaryNorm([1, 2, 3, 4, 5], cmap_risk.N)

    print (frequencies)

    # Scatter plot of the data
    scatter = ax.scatter(severities, frequencies, c=priorities, cmap=cmap_risk, norm=norm, alpha=0.6, edgecolor='black')

    # Expectation value plot
    ax.scatter([sev_mean], [freq_mean], color='lightgrey', s=200, label='Erwartungswert', edgecolor='black')

    # Set plot title, labels, limits, and legend
    ax.set_title('Scatterplot der simulierten Häufigkeit und Schwere')
    ax.set_xlabel('Normierte Schwere (0-1)')
    ax.set_ylabel('Normierte Häufigkeit (0-1)')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.legend()
    ax.grid(False)

    # Save the plot to a StringIO buffer in SVG format
    img = io.StringIO()
    fig.savefig(img, format='svg')
    img.seek(0)

    # Extract only the <svg> part of the image
    svg_img = '<svg' + img.getvalue().split('<svg')[1]
    
    return svg_img