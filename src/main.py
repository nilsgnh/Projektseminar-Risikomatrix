# main.py
from flask import Blueprint, render_template, request
from simulation import *
from matrix import *
from plot import *

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def main():
    return render_template("index.html")


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

    field_nums = [
        [1, 2, 3, 4],  # Häufig 
        [5, 6, 7, 8],  # Wahrscheinlich
        [9, 10, 11, 12],  #  Gelegentlich
        [13, 14, 15, 16],  # Selten
        [17, 18, 19, 20],  #  Unwahrscheinlich
        [21, 22, 23, 24],   # Unvorstellbar
    ]

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

    field_nums = [
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9,10],  
        [11, 12, 13, 14, 15],
        [16, 17, 18, 19, 20],
        [21, 22, 23, 24, 25],
    ]

    risk_labels = {1: "Grün", 2: "Gelb", 3: "Rot"}


    risk_colors = ["#92D050", "#FFC000", "#FF0000"]


    y_beschriftungen = ["0-0.2", "0.2-0.4", "0.4-0.6", "0.6-0.8", "0.8-1"]
    x_beschriftungen = ["0-0.2", "0.2-0.4", "0.4-0.6", "0.6-0.8", "0.8-1"]


    matrix = Matrix(matrix_rep, field_nums, risk_labels, risk_colors, x_beschriftungen, y_beschriftungen)

    return matrix