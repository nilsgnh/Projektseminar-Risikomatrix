import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend to avoid GUI
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from matplotlib.colors import ListedColormap
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import io

# Creates a bar chart showing the distribution of risk classes
def plotPriorityDistribution(priorities, matrix):
    # Map numerical priorities to their label names
    priorityCategories = pd.Series(priorities).map(matrix.riskLabels)
    # Count occurrences of each priority and fill missing values with 0
    priorityCounts = priorityCategories.value_counts().reindex(matrix.riskLabels.values()).fillna(0)
    
    # Create figure and canvas for plotting
    fig = Figure(figsize=(6, 4))
    FigureCanvas(fig)
    ax = fig.add_subplot(111)
    
    # Create bar plot with custom colors for each priority level
    sns.barplot(
        ax=ax, x=priorityCounts.index, y=priorityCounts.values,
        hue=priorityCounts.index,
        palette=matrix.riskColors, dodge=False, legend=False
    )
    
    # Add value labels on top of each bar
    for i, count in enumerate(priorityCounts.values):
        ax.text(i, count + 0.5, f'{int(count)}', ha='center', va='bottom', fontweight='bold')
    
    # Set chart title and labels
    ax.set_title("Verteilung der Risikoprioritäten in der Simulation")
    ax.set_xlabel("Priorität")
    ax.set_ylabel("Häufigkeit")
    
    # Convert plot to SVG format
    img = io.StringIO()
    fig.savefig(img, format='svg')
    img.seek(0)
    svg_img = '<svg' + img.getvalue().split('<svg')[1]
    return svg_img

# Creates a heatmap showing the frequency of occurrences in each matrix field
def plotHeatmap(matrixFelder, matrix):
    # Initialize array to store field counts
    feldCounts = np.zeros(matrix.rows*matrix.cols, dtype=int)
    # Count unique occurrences of each field
    unique_feld, counts_feld = np.unique(matrixFelder, return_counts=True)
    # Assign counts to corresponding field positions (subtract 1 for 0-based indexing)
    feldCounts[unique_feld - 1] = counts_feld
    
    # Reshape counts into matrix form
    matrixReshaped = feldCounts.reshape(matrix.rows, matrix.cols)
    # Create DataFrame with proper labels
    risiko_matrix_df = pd.DataFrame(matrixReshaped, index=matrix.yLabels, columns=matrix.xLabels)
    
    # Create figure and canvas
    fig = Figure(figsize=(6, 4))
    FigureCanvas(fig)
    ax = fig.add_subplot(111)
    
    # Create heatmap with annotations and color bar
    sns.heatmap(risiko_matrix_df, annot=True, cmap="YlGnBu", cbar_kws={'label': 'Anzahl'}, ax=ax)
    
    # Set chart title and labels
    ax.set_title("Absolute Häufigkeit der spezifischen Felder in der Risikomatrix")
    ax.set_xlabel("Schwere")
    ax.set_ylabel("Häufigkeit")
    
    # Convert plot to SVG format
    img = io.StringIO()
    fig.savefig(img, format='svg')
    img.seek(0)
    svg_img = '<svg' + img.getvalue().split('<svg')[1]
    return svg_img

# Creates a scatter plot showing severity vs frequency with risk priorities as colors
def plotScatter(sev_mean, freq_mean, priorities, severities, frequencies, matrix):
    # Create color map from matrix risk colors
    chartColors = ListedColormap(matrix.riskColors)
    
    # Create figure and canvas
    fig = Figure(figsize=(6, 4))
    FigureCanvas(fig)
    ax = fig.add_subplot(111)
    
    # Create grid lines for matrix boundaries
    X = np.linspace(0, 1, matrix.representation.shape[1] + 1)
    Y = np.linspace(0, 1, matrix.representation.shape[0] + 1)
    
    # Plot matrix background with risk colors
    ax.pcolormesh(X, Y, matrix.representation[::-1], cmap=chartColors, edgecolors='k', shading='auto', alpha=0.5)
    
    # Set up color normalization for scatter plot points
    unique_classes = np.unique(matrix.representation)
    boundaries = np.arange(min(unique_classes), max(unique_classes) + 2)
    norm = BoundaryNorm(boundaries, chartColors.N)
    
    # Create scatter plot of points colored by priority
    scatter = ax.scatter(severities, frequencies, c=priorities, cmap=chartColors, norm=norm, alpha=0.6, edgecolor='black')
    
    # Add mean point as large grey circle
    ax.scatter([sev_mean], [freq_mean], color='lightgrey', s=200, label='Erwartungswert', edgecolor='black')
    
    # Set chart title and labels
    ax.set_title('Scatterplot der simulierten Häufigkeit und Schwere')
    ax.set_xlabel('Normierte Schwere (0-1)')
    ax.set_ylabel('Normierte Häufigkeit (0-1)')
    
    # Set axis limits and display options
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.legend()
    ax.grid(False)
    
    # Convert plot to SVG format
    img = io.StringIO()
    fig.savefig(img, format='svg')
    img.seek(0)
    svg_img = '<svg' + img.getvalue().split('<svg')[1]
    return svg_img