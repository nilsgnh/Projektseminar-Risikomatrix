# main.py
from flask import Blueprint, render_template, request
from simulation import *
from matrix import *
from plot import *
import numpy as np

customMatr = None

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def main():
    return render_template("index.html")

@main_bp.route('/custom', methods=['GET'])
def custom():
    return render_template("customMatrix.html")


@main_bp.route('/custom/plot', methods=["GET"])
def plotCustomMatrix():
    points = generatePoints(1000, 0.4, 0.4, 0.4, 0.4)
    frequencies = points[0]
    severities = points[1]

    pointsInMatrix1 = simulateRiskMatrix(frequencies, severities, customMatr)
    priorities1 = pointsInMatrix1[0]

    bar_plot = plotPriorityDistribution(priorities1, customMatr)



    #render images back to index page
    render_template("customMatrix.html", bar3=bar_plot)

    return render_template("customMatrix.html", bar3=bar_plot)



@main_bp.route('/custom/submit', methods=["POST"])
def process_table():
    # Retrieve JSON data from the request
    data = request.get_json()
    
    table_data = np.array(data.get('table', []))
    colors = data.get('colors', [])
    names = data.get('names', [])
    
    y_beschriftungen = []
    x_beschriftungen = []


    risk_labels = {}
    for i, field in enumerate(names):
        risk_labels[i+1] = field


    field_nums = np.zeros((len(table_data), len(table_data[0])), dtype=int)

    counter = 1
    for i in range (len(table_data)):
        for j in range (len(table_data[0])):
            field_nums[i][j] = counter
            counter += 1
        
    for i in range(len(table_data)):
        y_beschriftungen.append("Y")
    
    for i in range(len(table_data[0])):
        x_beschriftungen.append("X")


    print("Matrix: ", table_data)
    print("Farben: ", colors)
    print("X-Beschriftungen:", x_beschriftungen)
    print("Y-Beschriftungen:", y_beschriftungen)
    print("FelderNummerierung:", field_nums)
    print("Risiko Labels: ", risk_labels)

    matrix = Matrix(table_data, field_nums, risk_labels, colors, x_beschriftungen, y_beschriftungen)
    customMatr = matrix

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



# Definition of Din EN 50126 Matrix
def dinMatrix():
    matrix_rep = np.array([
        [3, 4, 4, 4],   # Häufig
        [2, 3, 4, 4],   # Wahrscheinlich
        [2, 3, 3, 4],   # Gelegentlich
        [1, 2, 3, 3],   # Selten
        [1, 1, 2, 2],   # Unwahrscheinlich
        [1, 1, 1, 1],    # Unvorstellbar
    ])

    field_nums = np.zeros((len(matrix_rep), len(matrix_rep[0])), dtype=int)

    for i in range (len(matrix_rep)):
        for j in range (len(matrix_rep[0])):
            field_nums[i][j] = i+j+1

    risk_labels = {1: "Vernachlässigbar", 2: "Tolerabel", 3: "Unerwünscht", 4: "Intolerabel"}

    risk_colors = ["#92D050", "#8EB4E3", "#FFC000", "#FF0000"]

    y_beschriftungen = ["Häufig", "Wahrscheinlich", "Gelegentlich", "Selten", "Unwahrscheinlich", "Unvorstellbar"]
    x_beschriftungen = ["Unbedeutend", "Marginal", "Kritisch", "Katastrophal"]

    matrix = Matrix(matrix_rep, field_nums, risk_labels, risk_colors, x_beschriftungen, y_beschriftungen)

    return matrix


# Definition optimal Matrix by Cox

def optimalMatrix():
    matrix_rep = np.array([
        [1, 1, 2, 3, 3], 
        [1, 1, 2, 2, 3], 
        [1, 1, 1, 2, 2], 
        [1, 1, 1, 1, 1 ],
        [1, 1, 1, 1, 1], 
    ])

    field_nums = np.zeros((len(matrix_rep), len(matrix_rep[0])), dtype=int)

    counter = 1
    for i in range (len(matrix_rep)):
        for j in range (len(matrix_rep[0])):
            field_nums[i][j] = counter
            counter += 1

    risk_labels = {1: "Grün", 2: "Gelb", 3: "Rot"}


    risk_colors = ["#92D050", "#FFC000", "#FF0000"]


    y_beschriftungen = ["0-0.2", "0.2-0.4", "0.4-0.6", "0.6-0.8", "0.8-1"]
    x_beschriftungen = ["0-0.2", "0.2-0.4", "0.4-0.6", "0.6-0.8", "0.8-1"]


    matrix = Matrix(matrix_rep, field_nums, risk_labels, risk_colors, x_beschriftungen, y_beschriftungen)

    return matrix