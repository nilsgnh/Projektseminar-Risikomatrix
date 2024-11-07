# main.py
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from logic import simulate_risk_matrix, plot_priority_distribution, heatmap_svg, scatter_svg


main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def main():
    return render_template("index.html")

@main_bp.route('/display', methods=['GET'])
def display():
    n_simulations = 2000
    frequency_mean = 1/3 
    frequency_var = 0.005 
    severity_mean = 0.5 
    severity_var = 0.005
    data = simulate_risk_matrix(n_simulations, frequency_mean, frequency_var, severity_mean, severity_var)
    plot = plot_priority_distribution(data, n_simulations)
    plot2 = heatmap_svg(data, n_simulations)
    plot3 = scatter_svg(data, severity_mean, frequency_mean, n_simulations)
    return render_template("index.html", plot=plot, plot2=plot2, plot3=plot3)