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
    if request.method == 'POST':
        n_simulations = int(request.form['n_simulations'])
        frequency_mean = float(request.form['frequency_mean'])
        frequency_perc = float(request.form['frequency_perc'])
        severity_mean = float(request.form['severity_mean'])
        severity_perc = float(request.form['severity_perc'])


    frequency_var = conv_perc_var(95, frequency_perc)
    severity_var = conv_perc_var(95, severity_perc)

    matrix = optimalMatrix()

    points = generatePoints(n_simulations, frequency_mean, frequency_var, severity_mean, severity_var)
    frequencies = points[0]
    severities = points[1]

    pointsInMatrix = simulateRiskMatrix(frequencies, severities, matrix)
    priorities = pointsInMatrix[0]
    matrix_felder = pointsInMatrix[1]

    bar_plot = plotPriorityDistribution(priorities, matrix)
    heat_plot = plotHeatmap(matrix_felder, matrix)
    scatter_plot = plotScatter(severity_mean, frequency_mean, priorities, severities, frequencies, matrix)

    return render_template("index.html", plot=bar_plot, plot2=heat_plot, plot3=scatter_plot)


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


def optimalMatrix():
    matrix_rep = np.array([
        [1, 1, 2, 3, 3],   # Häufig
        [1, 1, 2, 2, 3],   # Wahrscheinlich
        [1, 1, 1, 2, 2],   # Gelegentlich
        [1, 1, 1, 1, 1 ],   # Selten
        [1, 1, 1, 1, 1],   # Unwahrscheinlich
    ])

    field_nums = [
        [1, 2, 3, 4, 5],  # Häufig 
        [6, 7, 8, 9,10],  # Wahrscheinlich
        [11, 12, 13, 14, 15],  #  Gelegentlich
        [16, 17, 18, 19, 20],  # Selten
        [21, 22, 23, 24, 25],  #  Unwahrscheinlich
    ]

    risk_labels = {1: "Grün", 2: "Gelb", 3: "Rot"}


    risk_colors = ["#92D050", "#FFC000", "#FF0000"]


    y_beschriftungen = ["0-0.2", "0.2-0.4", "0.4-0.6", "0.6-0.8", "0.8-1"]
    x_beschriftungen = ["0-0.2", "0.2-0.4", "0.4-0.6", "0.6-0.8", "0.8-1"]


    matrix = Matrix(matrix_rep, field_nums, risk_labels, risk_colors, x_beschriftungen, y_beschriftungen)

    return matrix