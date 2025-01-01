# main.py
from flask import Blueprint, render_template, request
from predefinedMatrices import optimalMatrix, dinMatrix
from simulation import *
from plot import *
import numpy as np
from matrix import *
from benchmark import calc_benchmark

customMatr = None
main_bp = Blueprint('main', __name__)

riskMatrixList = [optimalMatrix(), dinMatrix()] #--------------------------------------------> globale Liste für die risiko Maztritzen, initial mit din und optimal gefüllt


@main_bp.route('/', methods=['GET'])
def main():
    return render_template("index.html")

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




# Plots the custom Matrix (nicht mehr gebraucht)
'''
@main_bp.route('/custom/submit', methods=['GET', 'POST'])
def plotCustom():
    if customMatr == None:
        return 'bad request!', 400

    # taking User Input
    if request.method == 'POST':
        n_simulations = int(request.form['n_simulations'])
        frequency_mean = float(request.form['frequency_mean'])
        frequency_perc = float(request.form['frequency_perc'])
        severity_mean = float(request.form['severity_mean'])
        severity_perc = float(request.form['severity_perc'])

    frequency_var = conv_perc_var(95, frequency_perc)
    severity_var = conv_perc_var(95, severity_perc)


    #generating Points
    points = generatePoints(n_simulations, frequency_mean, frequency_var, severity_mean, severity_var)
    frequencies = points[0]
    severities = points[1]


    #Simulation
    pointsInMatrix = simulateRiskMatrix(frequencies, severities, customMatr)
    priorities = pointsInMatrix[0]
    matrix_felder = pointsInMatrix[1]

    bar_plot = plotPriorityDistribution(priorities, customMatr)
    heat_plot = plotHeatmap(matrix_felder, customMatr)
    scatter_plot = plotScatter(severity_mean, frequency_mean, priorities, severities, frequencies, customMatr)


    #render images back to page
    return render_template("customMatrix.html", customBar=bar_plot, customHeat=heat_plot, customScatter=scatter_plot)
'''



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


    #Simulation of first Matrix
    matrix = riskMatrixList[0] ###--------------------------------------------------------------------------------------1.übergebene Matrix hier aus der Liste auswählen
    pointsInMatrix = simulateRiskMatrix(frequencies, severities, matrix)
    priorities = pointsInMatrix[0]
    matrix_felder = pointsInMatrix[1]

    bar_plot = plotPriorityDistribution(priorities, matrix)
    heat_plot = plotHeatmap(matrix_felder, matrix)
    scatter_plot = plotScatter(severity_mean, frequency_mean, priorities, severities, frequencies, matrix)

    print('calc benchmark-score for 1. matrix:')
    score1 = calc_benchmark(matrix)

    #Simulation of second Matrix
    matrix1 = riskMatrixList[1] ###--------------------------------------------------------------------------------------2.übergebene Matrix hier aus der Liste auswählen
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
    return render_template("index.html", bar1=bar_plot, heat1=heat_plot, scatter1=scatter_plot, bar2=bar_plot1, heat2=heat_plot1, scatter2=scatter_plot1, score1=score1, score2=score2,greatestscores=greatestscores)


