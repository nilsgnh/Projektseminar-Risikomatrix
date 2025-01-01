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


@main_bp.route('/', methods=['GET'])
def main():
    return render_template("index.html")

@main_bp.route('/custom', methods=['GET'])
def custom():
    return render_template("customMatrix.html")


# turns the sent Data from customTableLogig.js into a globally accessible Matrix
@main_bp.route('/custom/enterTable', methods=["POST"])
def process_table():
    data = request.get_json()
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


    #generate and globalize matrix
    matrix = Matrix(table_data, field_nums, risk_labels, colors, x_beschriftungen, y_beschriftungen)
    global customMatr
    customMatr = matrix

    '''
    print("Matrix: ", table_data)
    print("Farben: ", colors)
    print("X-Beschriftungen:", x_beschriftungen)
    print("Y-Beschriftungen:", y_beschriftungen)
    print("FelderNummerierung:", field_nums)
    print("Risiko Labels: ", risk_labels)

    print(matrix)
    '''

    return '', 204  # Respond with No Content




# Plots the custom Matrix 
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

    # Benchmark berechnen
    print('Benchmark-Score der gespeicherten Matrix: ')
    print(calc_benchmark(customMatr))

    #render images back to page
    return render_template("customMatrix.html", customBar=bar_plot, customHeat=heat_plot, customScatter=scatter_plot)




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
    matrix = optimalMatrix()
    pointsInMatrix = simulateRiskMatrix(frequencies, severities, matrix)
    priorities = pointsInMatrix[0]
    matrix_felder = pointsInMatrix[1]

    bar_plot = plotPriorityDistribution(priorities, matrix)
    heat_plot = plotHeatmap(matrix_felder, matrix)
    scatter_plot = plotScatter(severity_mean, frequency_mean, priorities, severities, frequencies, matrix)


    #Simulation of second Matrix
    matrix1 = dinMatrix()
    pointsInMatrix1 = simulateRiskMatrix(frequencies, severities, matrix1)
    priorities1 = pointsInMatrix1[0]
    matrix_felder1 = pointsInMatrix1[1]

    bar_plot1 = plotPriorityDistribution(priorities1, matrix1)
    heat_plot1 = plotHeatmap(matrix_felder1, matrix1)
    scatter_plot1 = plotScatter(severity_mean, frequency_mean, priorities1, severities, frequencies, matrix1)


    #render images back to index page
    return render_template("index.html", bar1=bar_plot, heat1=heat_plot, scatter1=scatter_plot, bar2=bar_plot1, heat2=heat_plot1, scatter2=scatter_plot1)


