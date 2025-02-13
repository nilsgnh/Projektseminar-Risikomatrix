# main.py
from flask import Blueprint, render_template, request, session
from predefinedMatrices import optimalMatrix, dinMatrix, optimalMatrix2
from simulation import *
from plot import *
import numpy as np
from matrix import *
from benchmark import calc_benchmark

customMatr = None
main_bp = Blueprint('main', __name__)

riskMatrixList = [optimalMatrix(), dinMatrix(), optimalMatrix2()] # globale Liste für die risiko Maztritzen, initial mit din und optimal gefüllt

# Globale Variablen für die ausgewählten Matrizen
selected_matrices = {"matrix1": 0, "matrix2": 1}

@main_bp.route('/', methods=['GET', 'POST'])
def main():
    global selected_matrices
    if request.method == 'POST':
        # Hole die ausgewählten Matrizen-Namen aus dem Formular
        matrix1_name = request.form.get('matrix1', '')
        matrix2_name = request.form.get('matrix2', '')

        # Finde die Indizes der Matrizen basierend auf ihren Namen
        selected_matrices["matrix1"] = next((i for i, m in enumerate(riskMatrixList) if m.name == matrix1_name), 0)
        selected_matrices["matrix2"] = next((i for i, m in enumerate(riskMatrixList) if m.name == matrix2_name), 1)

    return render_template("index.html", riskMatrixList=riskMatrixList, selected_matrices=selected_matrices)

@main_bp.route('/custom', methods=['GET'])
def custom():
    matrixNames = [i.name for i in riskMatrixList]
    return render_template("customMatrix.html", matrices=matrixNames)


# turns the sent Data from customTableLogig.js into a globally accessible Matrix
@main_bp.route('/custom/enterTable', methods=["POST"])
def process_table():
    data = request.get_json()
    matrixName = data.get('name')
    table_data = np.array(data.get('table', []), dtype=float)
    colors = data.get('colors', [])
    names = data.get('riskNames', [])

    # set risk dictionary
    risk_labels = {}
    for i, field in enumerate(names):
        risk_labels[i+1] = field


    # set field numeration dinamically
    field_nums = np.zeros((len(table_data), len(table_data[0])), dtype=int)
    counter = 1
    for i in range (len(table_data)):
        for j in range (len(table_data[0])):
            field_nums[i][j] = counter
            counter += 1
        

    # set x and y labels dynamically
    y_beschriftungen = []
    x_beschriftungen = []
    
    x_step = 1 / len(table_data[0])
    y_step = 1 / len(table_data)

    for i in range(len(table_data)):
        y_beschriftungen.append(f"{round(1 - round((i + 1) * y_step, 2), 2)}-{round(1 - round(i * y_step, 2), 2)}")

    for i in range(len(table_data[0])):
        x_beschriftungen.append(f"{round(i * x_step, 2)}-{round((i + 1) * x_step, 2)}")

    print(matrixName)

    #generate and globalize matrix
    newMatrix = Matrix(matrixName, table_data, field_nums, risk_labels, colors, x_beschriftungen, y_beschriftungen)
    global riskMatrixList
    riskMatrixList.append(newMatrix)

    return '', 204  # Respond with No Content



@main_bp.route('/submit', methods=['GET', 'POST'])
def set_parameters():
    # taking User Input
    if request.method == 'POST':
        n_simulations = int(request.form['n_simulations'])
        frequency_mean = float(request.form['frequency_mean'])
        frequency_perc = float(request.form['frequency_perc'])
        severity_mean = float(request.form['severity_mean'])
        severity_perc = float(request.form['severity_perc'])


    # converting & to Variance
    frequency_var = conv_perc_var(95, frequency_perc)
    severity_var = conv_perc_var(95, severity_perc)


    #generating Points
    points = generatePoints(n_simulations, frequency_mean, frequency_var, severity_mean, severity_var)
    frequencies = points[0]
    severities = points[1]

    # Simulation der ausgewählten Matrizen
    matrix = riskMatrixList[selected_matrices["matrix1"]]
    matrix1 = riskMatrixList[selected_matrices["matrix2"]]

    #Simulation of first Matrix
    pointsInMatrix = simulateRiskMatrix(frequencies, severities, matrix)
    priorities = pointsInMatrix[0]
    matrix_felder = pointsInMatrix[1]

    bar_plot = plotPriorityDistribution(priorities, matrix)
    heat_plot = plotHeatmap(matrix_felder, matrix)
    scatter_plot = plotScatter(severity_mean, frequency_mean, priorities, severities, frequencies, matrix)

    print('calc benchmark-score for 1. matrix:')
    score1 = calc_benchmark(matrix)

    #Simulation of second Matrix
    pointsInMatrix1 = simulateRiskMatrix(frequencies, severities, matrix1)
    priorities1 = pointsInMatrix1[0]
    matrix_felder1 = pointsInMatrix1[1]

    bar_plot1 = plotPriorityDistribution(priorities1, matrix1)
    heat_plot1 = plotHeatmap(matrix_felder1, matrix1)
    scatter_plot1 = plotScatter(severity_mean, frequency_mean, priorities1, severities, frequencies, matrix1)
    
    print('calc benchmark-score for 2. matrix:')
    score2 = calc_benchmark(matrix1)

    #Vergleich der benchmarks und entsprechendes Einfärben der Scores
    greatestscores = {
        "benchmark_score": 'score1',
        "ordnung_score": 'score1',
        "range_compression_score": 'score1',
        "overlap_score": 'score1',
        "quantifying_errors_score": 'score1'
    }
    if score1['benchmark_score'] < score2['benchmark_score']:
        greatestscores['benchmark_score'] = 'score2'
    elif score1['benchmark_score'] == score2['benchmark_score']:
        greatestscores['benchmark_score'] = 'both'

    if score1['ordnung_score'] < score2['ordnung_score']:
        greatestscores['ordnung_score'] = 'score2'
    elif score1['ordnung_score'] == score2['ordnung_score']:
        greatestscores['ordnung_score'] = 'both'

    if score1['range_compression_score'] < score2['range_compression_score']:
        greatestscores['range_compression_score'] = 'score2'
    elif score1['range_compression_score'] == score2['range_compression_score']:
        greatestscores['range_compression_score'] = 'both'

    if score1['overlap_score'] < score2['overlap_score']:
        greatestscores['overlap_score'] = 'score2'
    elif score1['overlap_score'] == score2['overlap_score']:
        greatestscores['overlap_score'] = 'both'

    if score1['quantifying_errors_score'] < score2['quantifying_errors_score']:
        greatestscores['quantifying_errors_score'] = 'score2'
    elif score1['quantifying_errors_score'] == score2['quantifying_errors_score']:
        greatestscores['quantifying_errors_score'] = 'both'

    #render images back to index page
    return render_template("index.html", bar1=bar_plot, heat1=heat_plot, scatter1=scatter_plot, bar2=bar_plot1, heat2=heat_plot1, scatter2=scatter_plot1, score1=score1, score2=score2,greatestscores=greatestscores, riskMatrixList=riskMatrixList, selected_matrices=selected_matrices)


