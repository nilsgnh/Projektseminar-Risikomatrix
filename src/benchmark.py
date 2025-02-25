import numpy as np
from predefinedMatrices import dinMatrix, optimalMatrix
from scipy.stats import spearmanr


def calculate_range_compression(matrix):
    """
    Berechnet den Range Compression Score einer gegebenen Risikomatrix.
    
    Args:
    - matrix: Instanz der Klasse Matrix
    
    Returns:
    - ScoreRange: Der berechnete Score für die Range Compression.
    """
    # für jedes Feld in der Matrix wird kleinster und größter Wert berechnet und mitsamt der Klasse in ein Array gespeichert
    min_max_values = []
    anzx = matrix.cols
    anzy = matrix.rows       
    x_step=1/anzx
    y_step=1/anzy

    for i in range(anzy):
        for j in range(anzx):
            risk_class = matrix.representation[i][j]
            minval=(j*x_step) *(1-(i+1)*y_step)
            maxval=(j+1)*x_step*(1-i*y_step)

            min_max_values.append((risk_class, minval, maxval))

    # Sortierung der Werte nach Risikoklasse
    min_max_values.sort(key=lambda x: x[0])
    #print(min_max_values)

    # Anzahl risk classes in der Matrix:
    n_classes = len(matrix.riskLabels)

    # je Klasse ein Array, in dem die Werte der Klasse gespeichert werden
    class_values = [[] for _ in range(n_classes)] # erste Dimension: Klasse, zweite Dimension: Werte

    # in min_max_values gespeicherte Werte werden in die entsprechenden Klassen-Arrays eingefügt
    for risk_class, minval, maxval in min_max_values:
        class_values[int(risk_class-1)].append(minval)
        class_values[int(risk_class-1)].append(maxval)

    # je Klasse wird der kleinste und größte Wert berechnet
    class_range = []
    global_min = 1
    global_max = 0
    for i in range(n_classes):
        #print("Klasse: ", i+1)
        #print(class_values[i])
        #print(min(class_values[i]))
        #print(max(class_values[i]))
        range_i = abs(max(class_values[i])-min(class_values[i]))
        class_range.append(range_i)
        if(min(class_values[i])<global_min):
            global_min=min(class_values[i])
        if(max(class_values[i])>global_max):
            global_max=max(class_values[i])

    #print("Class Range:")
    #print(class_range)
    # Berechnung des Range Compression Scores
    ScoreRange = 0
    for i in range(n_classes):
        ScoreRange += class_range[i]

    # Berechnen von Summe an Unterscheidungen zwischen den Klassen (der Ranges)
    sumdiff = 0
    for i in range(n_classes-1):
        for j in range(i+1,n_classes):
            sumdiff += abs(class_range[i]-class_range[j])

    # Durchschnittlicher Unterschied zwischen den Klassen
    if n_classes == 1:
        AverageSumDiff = 0
    else:
        AverageSumDiff = sumdiff/(n_classes*(n_classes-1)/2) # durch n(n-1)/2 geteilt, da es n(n-1)/2 Unterscheidungen gibt
    #print("AverageSumDiff: ", AverageSumDiff)
    
    AverageRange = ScoreRange/n_classes

    ScoreRange = 1- ((0.7*AverageRange+0.3*AverageSumDiff)/(global_max-global_min)) ##TODO: Dafür sorgen, dass ScoreRange immer zwischen 0 und 1 liegt

    return ScoreRange

def calculate_overlap(matrix):
    """
    Berechnet den Overlap Score einer gegebenen Risikomatrix.
    
    Args:
    - matrix: Instanz der Klasse Matrix
    
    Returns:
    - ScoreOverlap: Der berechnete Score für den Overlap.
    """
    # Anzahl risk classes in der Matrix:
    n_classes = len(matrix.riskLabels)

    # für jede Klasse Intervall I_j = [min(quantiative_risk_j), max(quantiative_risk_j)] berechnen und speichern
    min_max_values = []
    anzx = matrix.cols
    anzy = matrix.rows       
    x_step=1/anzx
    y_step=1/anzy

    for i in range(anzy):
        for j in range(anzx):
            risk_class = matrix.representation[i][j]
            minval=(j*x_step) *(1-(i+1)*y_step)
            maxval=(j+1)*x_step*(1-i*y_step)

            min_max_values.append((risk_class, minval, maxval))

    min_max_values.sort(key=lambda x: x[0])

    n_classes = len(matrix.riskLabels)

    class_values = [[] for _ in range(n_classes)]

    for risk_class, minval, maxval in min_max_values:
        class_values[int(risk_class-1)].append(minval)
        class_values[int(risk_class-1)].append(maxval)

    class_range = []
    for i in range(n_classes):
        class_range.append((min(class_values[i]), max(class_values[i])))

    #print(class_range)

    # Berechnung der einzelnen Overlaps
    k=n_classes
    totaloverlap=0

    for j in range(1, k):
        for x in range(1, k-j+1):
            overlap=max(0, class_range[j-1][1]-(class_range[j+x-1][0]))
            totaloverlap+=overlap*x
            #print("Overlap: ", overlap)
    maxoverlap = 0
    for x in range (1, k):
        maxoverlap+=(k-x)*x

    if maxoverlap == 0:
        scoreoverlap = 0
    else:
        scoreoverlap = 1- totaloverlap/maxoverlap

    #print("Total Overlap: ", totaloverlap)
    #print("Max Overlap: ", maxoverlap)

    return scoreoverlap

def calc_quantifying_errors(matrix):
    # Speichern der Risikoklassen der 4 umliegenden Felder für jedes Kreuz der Matrix
    # (nur für die Felder, die nicht am Rand liegen)

    # Anzahl Kreuze
    n_crosses = (matrix.rows-1)*(matrix.cols-1)

    # Speichern der Risikoklassen der 4 umliegenden Felder für jedes Kreuz
    cross_classes = np.zeros((n_crosses, 4)) # 2D-Array: Zeilen: Kreuze, Spalten: Risikoklassen
    
    for i in range(matrix.rows-1):
        for j in range(matrix.cols-1):
            # Kreuznummer
            cross_num = i*(matrix.cols-1)+j

            # Risikoklassen der 4 umliegenden Felder
            cross_classes[cross_num, 0] = matrix.representation[i][j] # oben links
            cross_classes[cross_num, 1] = matrix.representation[i][j+1] # oben rechts
            cross_classes[cross_num, 2] = matrix.representation[i+1][j] # unten links
            cross_classes[cross_num, 3] = matrix.representation[i+1][j+1] # unten rechts

    #print(cross_classes)

    # Berechnung der Quantifying Errors
    quantifying_errors = 0
    for i in range(n_crosses):
        # Anzahl der unterschiedlichen Risikoklassen in einem Kreuz berechnen
        unique_classes = np.unique(cross_classes[i])
        n_unique_classes = len(unique_classes)
        quantifying_errors += n_unique_classes

    # Score berechnen
    if n_crosses == 0:
        quantifying_errors_score = 1
    else:
        quantifying_errors_score = 1 - quantifying_errors/(n_crosses*4)
    return quantifying_errors_score


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

def ordnung_risk_matrix(matrix, nSimulations=10000):
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

    # Score
    if(rank_correlation/ideal_case_corr>=0):
        score=rank_correlation/ideal_case_corr
    else:
        score = 0
    # Zusammenfassung der Ergebnisse
    results = {
        "rank_correlation": rank_correlation,
        "ideal_case_correlation": ideal_case_corr,
        "worst_case_correlation": worst_case_corr,
        "risk_distribution": risk_distribution,
        "risk_points": risk_points,
        "benchmark_score": score
    }
    return results

def calc_benchmark(matrix):
    """
    Berechnet den Benchmark Score einer gegebenen Risikomatrix.
    
    Args:
    - matrix: Instanz der Klasse Matrix
    
    Returns:
    - ScoreBenchmark: Der berechnete Benchmark Score.
    """
    res = ordnung_risk_matrix(matrix)
    w = res['benchmark_score']
    x = calculate_range_compression(matrix)
    y = calculate_overlap(matrix)
    z = calc_quantifying_errors(matrix)

#Berechnet durch Ausgabe von idealer Matrix (0.9887)
    a = 0.1947 
    b = 0.2881
    c = 0.2092
    d = 0.308

    ScoreBenchmark = a*w + b*x + c*y + d*z

    results = {
        "benchmark_score": ScoreBenchmark,
        "ordnung_score": w,
        "range_compression_score": x,
        "overlap_score": y,
        "quantifying_errors_score": z
    }
    return results

# Beispiel für die Nutzung
if __name__ == "__main__":
    matrix = dinMatrix()
    matrixopt = optimalMatrix()

    # Ordnungs-Score durchführen
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

    # Range Compression Score berechnen
    range_compression_score = calculate_range_compression(matrix)
    range_compression_score_opt = calculate_range_compression(matrixopt)

    print("\nRange Compression Score für din-Matrix:")
    print(f"Range Compression Score: {range_compression_score}")

    print("\nRange Compression Score für optimal-Matrix:")
    print(f"Range Compression Score: {range_compression_score_opt}")

    # Overlap Score berechnen
    overlap_score = calculate_overlap(matrix)
    overlap_score_opt = calculate_overlap(matrixopt)

    print("\nOverlap Score für din-Matrix:")
    print(f"Overlap Score: {overlap_score}")

    print("\nOverlap Score für optimal-Matrix:")
    print(f"Overlap Score: {overlap_score_opt}")

    # Quantifying Errors berechnen
    quanterr_score=calc_quantifying_errors(matrix)
    quanterr_score_opt=calc_quantifying_errors(matrixopt)

    print("\nQuantifying Errors Score für din-Matrix:")
    print(f"Quantifying Errors Score: {quanterr_score}")

    print("\nQuantifying Errors Score für optimal-Matrix:")
    print(f"Quantifying Errors Score: {quanterr_score_opt}")

    benchmarkscore_din = calc_benchmark(matrix)
    benchmarkscore_opt = calc_benchmark(matrixopt)

    print('--------------------------------')
    print("\nBenchmark Score für din-Matrix:")
    print(f"Benchmark Score: {benchmarkscore_din}")

    print("\nBenchmark Score für optimal-Matrix:")
    print(f"Benchmark Score: {benchmarkscore_opt}")