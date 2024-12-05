import numpy as np
from matrix import Matrix
from main import dinMatrix, optimalMatrix
from scipy.stats import spearmanr
from simulation import generatePoints


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

class RiskPoint:
    """
    Klasse für die Repräsentation eines simulierten Punkts in der Risikomatrix.
    """
    def __init__(self, frequency, severity, quantitative_risk, qualitative_risk):
        self.frequency = frequency
        self.severity = severity
        self.quantitative_risk = quantitative_risk
        self.qualitative_risk = qualitative_risk

    def __repr__(self):
        return (f"RiskPoint(freq={self.frequency:.2f}, sev={self.severity:.2f}, "
                f"quant_risk={self.quantitative_risk:.5f}, qual_risk={self.qualitative_risk})")

def ordnung_risk_matrix(matrix, nSimulations=100):
    """
    Führt eine simulationsgestützte Benchmark der Risikomatrix durch.

    Parameters:
        matrix (Matrix): Die zu testende Matrix.
        nSimulations (int): Anzahl der zu simulierenden Punkte.

    Returns:
        dict: Ein Dictionary mit dem Ordnungsmaß, der Verteilung der Risikoklassen und den simulierten Punkten.
    """
    # Simulation von Punkten (gleichverteilt im Bereich [0,1])
    frequencies = np.random.uniform(0, 1, nSimulations)
    severities = np.random.uniform(0, 1, nSimulations)

    # Liste von RiskPoint-Objekten erstellen
    risk_points = []
    for freq, sev in zip(frequencies, severities):
        # Berechnung des quantitativen Risikos
        quantitative_risk = freq * sev
        # Zuordnung der qualitativen Risikostufe
        qualitative_risk, _ = matrix.computeDataPoint(freq, sev) # _ ist die Feldnummer, die hier nicht benötigt wird
        # Erstellung eines RiskPoint-Objekts
        risk_points.append(RiskPoint(freq, sev, quantitative_risk, qualitative_risk))

    # Sortierung der Punkte nach quantitativem Risiko
    risk_points.sort(key=lambda point: point.quantitative_risk)

    '''#Ausgabe von sortierten Punkten (einmal nur die quantitativen Risiken und einmal die qualitativen Risiken)
    print("Quantitative Risiken:")
    for point in risk_points:
        print(point.quantitative_risk)
    print("\nQualitative Risiken:")
    for point in risk_points:
        print(point.qualitative_risk)'''

    # Ordnungsmaß: Spearman's Rank Correlation zwischen quantitativen und qualitativen Risiken
    quantitative_risks = [point.quantitative_risk for point in risk_points]
    qualitative_risks = [point.qualitative_risk for point in risk_points]
    rank_correlation, _ = spearmanr(quantitative_risks, qualitative_risks)

    # Worst-case und ideal-case Benchmarks
    worst_case = np.random.permutation(qualitative_risks)
    ideal_case = sorted(qualitative_risks) # Sortierung der qualitativen Risiken
    worst_case_corr, _ = spearmanr(quantitative_risks, worst_case)
    ideal_case_corr, _ = spearmanr(quantitative_risks, ideal_case)

    # Risikoverteilung
    unique, counts = np.unique(qualitative_risks, return_counts=True)
    risk_distribution = dict(zip(unique, counts))

    # Zusammenfassung der Ergebnisse
    results = {
        "rank_correlation": rank_correlation,
        "ideal_case_correlation": ideal_case_corr,
        "worst_case_correlation": worst_case_corr,
        "risk_distribution": risk_distribution,
        "risk_points": risk_points,
        "benchmark_score": rank_correlation/ideal_case_corr # Score für die Bewertung der Risikomatrix (0-1)
    }
    return results

# Beispiel für die Nutzung
if __name__ == "__main__":
    matrix = dinMatrix()
    matrixopt = optimalMatrix()

    # Benchmark durchführen
    benchmark_results = ordnung_risk_matrix(matrix)
    benchmark_results_opt = ordnung_risk_matrix(matrixopt)

    # Ergebnisse anzeigen
    print("Benchmark Ergebnisse für din-Matrix:")
    print(f"Ordnungsmaß (Spearman Rank Correlation): {benchmark_results['rank_correlation']}")
    print(f"Idealfall (Korrelation): {benchmark_results['ideal_case_correlation']}")
    print(f"Worst-Case (Korrelation): {benchmark_results['worst_case_correlation']}")
    print(f"Risikoverteilung: {benchmark_results['risk_distribution']}")
    print(f"Benchmark Score: {benchmark_results['benchmark_score']}")


    print("\nBenchmark Ergebnisse für optimal-Matrix:")
    print(f"Ordnungsmaß (Spearman Rank Correlation): {benchmark_results_opt['rank_correlation']}")
    print(f"Idealfall (Korrelation): {benchmark_results_opt['ideal_case_correlation']}")
    print(f"Worst-Case (Korrelation): {benchmark_results_opt['worst_case_correlation']}")
    print(f"Risikoverteilung: {benchmark_results_opt['risk_distribution']}")
    print(f"Benchmark Score: {benchmark_results_opt['benchmark_score']}")


    '''# Beispiele der simulierten Punkte anzeigen
    print("\nBeispiele der simulierten Punkte:")
    for point in benchmark_results["risk_points"][:10]:  # Zeige die ersten 10 Punkte
        print(point)'''