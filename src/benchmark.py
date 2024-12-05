import numpy as np
from matrix import Matrix
from main import dinMatrix, optimalMatrix


def calculate_range_compression(matrix):
    """
    Berechnet den Range Compression Score einer gegebenen Risikomatrix.
    
    Args:
    - matrix: Instanz der Klasse Matrix
    
    Returns:
    - ScoreRange: Der berechnete Score für die Range Compression.
    """
    risk_classes = matrix.representation.flatten()  # Alle qualitativen Risiko-Klassen
    k = len(matrix.riskLabels)  # Anzahl qualitativer Risikostufen
    ranges = []  # Liste für die Range jeder Klasse
    
    for j in range(1, k + 1):  # Iteriere über jede qualitative Klasse
        # Indizes aller Felder, die zu dieser Klasse gehören
        indices = np.argwhere(matrix.representation == j)
        
        if len(indices) == 0:  # Überspringe Klassen, die nicht verwendet werden
            continue
        
        # Berechne minimale und maximale quantitative Werte für alle Felder dieser Klasse
        quantitative_min_values = []
        quantitative_max_values = []
        for idx in indices:
            freq_idx, sev_idx = idx  # Index für Häufigkeit und Schwere
            
            # Grenzen der Häufigkeitsklasse (vertikale Achse)
            freq_lower = freq_idx / matrix.rows
            freq_upper = (freq_idx + 1) / matrix.rows
            
            # Grenzen der Schwereklasse (horizontale Achse)
            sev_lower = sev_idx / matrix.cols
            sev_upper = (sev_idx + 1) / matrix.cols
            
            # Minimaler und maximaler quantitativer Wert
            min_value = freq_lower * sev_lower  # niedrigste Kombination
            max_value = freq_upper * sev_upper  # höchste Kombination
            
            quantitative_min_values.append(min_value)
            quantitative_max_values.append(max_value)
        
        # Bestimme Range für die Klasse
        range_j = max(quantitative_max_values) - min(quantitative_min_values)
        ranges.append(range_j)

    print(ranges)
    
    # Durchschnittliche Range
    avg_range = sum(ranges) / len(ranges)
    
    # Score berechnen: max(Rquant) - min(Rquant) ist normiert auf [0, 1], daher 1 - avg_range
    score_range = 1 - avg_range
    
    return score_range

dinmatrix= dinMatrix()
optmatrix= optimalMatrix()

print(calculate_range_compression(dinmatrix))
print(calculate_range_compression(optmatrix))