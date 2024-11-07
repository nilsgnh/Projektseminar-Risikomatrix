# main.py
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from model import simulate_risk_matrix, plot_priority_distribution, heatmap_svg, scatter_svg


main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def main():
    return render_template("index.html")

@main_bp.route('/submit', methods=['GET', 'POST'])
def set_parameters():
    if request.method == 'POST':
        n_simulations = int(request.form['n_simulations'])
        frequency_mean = float(request.form['frequency_mean'])
        frequency_var = float(request.form['frequency_var'])
        severity_mean = float(request.form['severity_mean'])
        severity_var = float(request.form['severity_var'])

    data = simulate_risk_matrix(n_simulations, frequency_mean, frequency_var, severity_mean, severity_var)

    frequencies = data[0]
    severities = data[1]
    priorities = data[2]
    matrix_felder = data[3]


    bar_plot = plot_priority_distribution(priorities)
    heat_plot = heatmap_svg(matrix_felder)
    scatter_plot = scatter_svg(severity_mean, frequency_mean, priorities, severities, frequencies)
    return render_template("index.html", plot=bar_plot, plot2=heat_plot, plot3=scatter_plot)