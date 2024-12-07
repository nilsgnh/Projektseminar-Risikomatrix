import numpy as np
from matrix import *


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