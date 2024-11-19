# main.py
from flask import Blueprint, render_template, request
from model import simulate_risk_matrix, plot_priority_distribution, heatmap_svg, scatter_svg, conv_perc_std, conv_perc_var
from simulation import *
from matrix import *
from plot import *

main_bp = Blueprint('main', __name__)

# Erste Route (set_parameters)
@main_bp.route('/', methods=['GET'])
def main():
    return render_template("index.html")

@main_bp.route('/submit2', methods=['GET', 'POST'])
def set_parameters_v1():
    if request.method == 'POST':
        n_simulations = int(request.form['n_simulations'])
        frequency_mean = float(request.form['frequency_mean'])
        frequency_perc = float(request.form['frequency_perc'])
        severity_mean = float(request.form['severity_mean'])
        severity_perc = float(request.form['severity_perc'])

    frequency_var = conv_perc_var(95, frequency_perc)
    severity_var = conv_perc_var(95, severity_perc)

    data = simulate_risk_matrix(n_simulations, frequency_mean, frequency_var, severity_mean, severity_var)

    frequencies = data[0]
    severities = data[1]
    priorities = data[2]
    matrix_felder = data[3]

    bar_plot = plot_priority_distribution(priorities)
    heat_plot = heatmap_svg(matrix_felder)
    scatter_plot = scatter_svg(severity_mean, frequency_mean, priorities, severities, frequencies)
    return render_template("index.html", plot=bar_plot, plot2=heat_plot, plot3=scatter_plot)


# Zweite Route (set_parameters)
@main_bp.route('/submit', methods=['GET', 'POST'])
def set_parameters_v2():
    if request.method == 'POST':
        n_simulations = int(request.form['n_simulations'])
        frequency_mean = float(request.form['frequency_mean'])
        frequency_perc = float(request.form['frequency_perc'])
        severity_mean = float(request.form['severity_mean'])
        severity_perc = float(request.form['severity_perc'])

    frequency_var = convertPercentToStandardDeviation(95, frequency_perc)
    severity_var = convertPercentToVariance(95, severity_perc)

    matrix_rep = np.array([
        [3, 4, 4, 4],   # Häufig
        [2, 3, 4, 4],   # Wahrscheinlich
        [2, 3, 3, 4],   # Gelegentlich
        [1, 2, 3, 3],   # Selten
        [1, 1, 2, 2],   # Unwahrscheinlich
        [1, 1, 1, 1],    # Unvorstellbar
        [5,5,5,5]
    ])

    field_nums = [
        [1, 2, 3, 4],  # Häufig 
        [5, 6, 7, 8],  # Wahrscheinlich
        [9, 10, 11, 12],  #  Gelegentlich
        [13, 14, 15, 16],  # Selten
        [17, 18, 19, 20],  #  Unwahrscheinlich
        [21, 22, 23, 24],   # Unvorstellbar
        [25,26,27,28]

    ]

    risk_labels = {1: "Vernachlässigbar", 2: "Tolerabel", 3: "Unerwünscht", 4: "Intolerabel", 5:"tst"}

    risk_colors = ["#92D050", "#8EB4E3", "#FFC000", "#FF0000", "#9e34eb"]

    y_beschriftungen = ["Häufig", "Wahrscheinlich", "Gelegentlich", "Selten", "Unwahrscheinlich", "Unvorstellbar", "test"]
    x_beschriftungen = ["Unbedeutend", "Marginal", "Kritisch", "Katastrophal"]

    # Instantiate the Matrix class with sample data
    matrix = Matrix(matrix_rep, field_nums, risk_labels, risk_colors, x_beschriftungen, y_beschriftungen)

    data = simulateRiskMatrix(n_simulations, frequency_mean, frequency_var, severity_mean, severity_var, matrix)

    frequencies = data[0]
    severities = data[1]
    priorities = data[2]
    matrix_felder = data[3]

    bar_plot = plotPriorityDistribution(priorities, matrix)
    heat_plot = plotHeatmap(matrix_felder, matrix)
    scatter_plot = plotScatter(severity_mean, frequency_mean, priorities, severities, frequencies, matrix)
    return render_template("index.html", plot=bar_plot, plot2=heat_plot, plot3=scatter_plot)
