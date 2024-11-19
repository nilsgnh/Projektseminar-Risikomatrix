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



def plotPriorityDistribution(priorities, matrix):
      priorityCategories = pd.Series(priorities).map(matrix.riskLabels)
      priorityCounts = priorityCategories.value_counts().reindex(matrix.riskLabels.values()).fillna(0)

      fig = Figure(figsize=(8, 6))
      FigureCanvas(fig)
      ax = fig.add_subplot(111)

      sns.barplot(
            ax=ax, x=priorityCounts.index, y=priorityCounts.values, 
            hue=priorityCounts.index, 
            palette=matrix.riskColors, dodge=False, legend=False
      )

      for i, count in enumerate(priorityCounts.values):
            ax.text(i, count + 0.5, f'{int(count)}', ha='center', va='bottom', fontweight='bold')


      ax.set_title("Verteilung der Risikoprioritäten in der Simulation")
      ax.set_xlabel("Priorität")
      ax.set_ylabel("Häufigkeit")


      img = io.StringIO()
      fig.savefig(img, format='svg')
      img.seek(0)

      # Extract only the <svg> part of the image
      svg_img = '<svg' + img.getvalue().split('<svg')[1]
      
      return svg_img



def plotHeatmap(matrixFelder, matrix):
      
      feldCounts = np.zeros(matrix.rows*matrix.cols, dtype=int)  
      unique_feld, counts_feld = np.unique(matrixFelder, return_counts=True)
      feldCounts[unique_feld - 1] = counts_feld  

      matrixReshaped = feldCounts.reshape(matrix.rows, matrix.cols)

      risiko_matrix_df = pd.DataFrame(matrixReshaped, index=matrix.yLabels, columns=matrix.xLabels)

      fig = Figure(figsize=(10, 6))
      FigureCanvas(fig) 
      ax = fig.add_subplot(111)


      sns.heatmap(risiko_matrix_df, annot=True, cmap="YlGnBu", cbar_kws={'label': 'Anzahl'}, ax=ax)
      ax.set_title("Absolute Häufigkeit der spezifischen Felder in der Risikomatrix")
      ax.set_xlabel("Schwere")
      ax.set_ylabel("Häufigkeit")

      # Save the plot to a StringIO buffer in SVG format
      img = io.StringIO()
      fig.savefig(img, format='svg')
      img.seek(0)

      # Extract only the <svg> part of the image
      svg_img = '<svg' + img.getvalue().split('<svg')[1]
      
      return svg_img


def plotScatter(sev_mean, freq_mean, priorities, severities, frequencies, matrix):

      chartColors = ListedColormap(matrix.riskColors)

      fig = Figure(figsize=(10, 6))
      FigureCanvas(fig)
      ax = fig.add_subplot(111)

      X = np.linspace(0, 1, matrix.representation.shape[1] + 1)
      Y = np.linspace(0, 1, matrix.representation.shape[0] + 1)

      ax.pcolormesh(X, Y, matrix.representation[::-1], cmap=chartColors, edgecolors='k', shading='auto', alpha=0.5)

      norm = BoundaryNorm([1, 2, 3, 4, 5], chartColors.N)

      scatter = ax.scatter(severities, frequencies, c=priorities, cmap=chartColors, norm=norm, alpha=0.6, edgecolor='black')


      ax.scatter([sev_mean], [freq_mean], color='lightgrey', s=200, label='Erwartungswert', edgecolor='black')

      # Set plot title, labels, limits, and legend
      ax.set_title('Scatterplot der simulierten Häufigkeit und Schwere')
      ax.set_xlabel('Normierte Schwere (0-1)')
      ax.set_ylabel('Normierte Häufigkeit (0-1)')
      ax.set_xlim(0, 1)
      ax.set_ylim(0, 1)
      ax.legend()
      ax.grid(False)

      # Save the plot to a StringIO buffer in SVG format
      img = io.StringIO()
      fig.savefig(img, format='svg')
      img.seek(0)

      # Extract only the <svg> part of the image
      svg_img = '<svg' + img.getvalue().split('<svg')[1]
      
      return svg_img

