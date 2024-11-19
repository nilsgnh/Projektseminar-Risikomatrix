import numpy as np

class Matrix:
    def __init__(self, representation, fieldNums, riskLabels, riskColors, xLabels, yLabels):
        self.representation = representation
        self.rows, self.cols = representation.shape
        self.fieldNums = fieldNums
        self.riskLabels = riskLabels
        self.riskColors = riskColors
        self.xLabels = xLabels      
        self.yLabels = yLabels

        print(self.rows, self.cols)

    def computeDataPoint(self, pointFrequency, pointSeverity):
      # Berechnung der Häufigkeitsklasse
      for i in range(1, self.rows + 1):
            lowerBound = (i - 1) / self.rows
            upperBound = i / self.rows

            if pointFrequency == 1:
                  frequencyCategory = 1
                  break

            if lowerBound <= pointFrequency < upperBound:
                  frequencyCategory = self.rows - (i - 1)
                  break
      else:
            raise ValueError("Frequency value could not be categorized.")

      # Berechnung der Schwereklasse
      for i in range(1, self.cols + 1):
            lowerBound = (i - 1) / self.cols
            upperBound = i / self.cols

            if pointSeverity == 1:
                  severityCategory = self.cols
                  break

            if lowerBound <= pointSeverity < upperBound:
                  severityCategory = i
                  break
      else:
            raise ValueError("Severity value could not be categorized.")

      riskClass = self.representation[frequencyCategory - 1][severityCategory - 1]
      fieldNum = self.fieldNums[frequencyCategory - 1][severityCategory - 1]

      return riskClass, fieldNum
