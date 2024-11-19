import numpy as np


class Matrix:

      def __init__(self, representation, fieldNums, riskLabels, riskColors, xLabels, yLabels):
            self.representation = representation
            self.rows, self.cols = representation.shape
            self.fieldNums = fieldNums
            self.riskLabels = riskLabels #erwartet wird Dict zB priority_labels = {1: "Vernachlässigbar", 2: "Tolerabel", 3: "Unerwünscht", 4: "Intolerabel"}
            self.riskColors = riskColors
            self.xLabels = xLabels
            self.yLabels = yLabels
            
      def computeDataPoint(self, pointFrequency, pointSeverity):

            # Berechnung der Häufigkeitsklasse des Punkts (1=am Häufigsten)
            for i in range(self.rows):  # Beginnt bei 0
                  lowerBound = i / self.rows
                  upperBound = (i + 1) / self.rows

                  if pointFrequency < 1/self.rows:
                        frequencyCategory = self.rows
                        break

                  if pointFrequency >= (self.rows - 1)/self.rows:
                        frequencyCategory = 1
                        break

                  if lowerBound <= pointFrequency < upperBound:
                        frequencyCategory = self.rows - i
                        break

            # Berechnung der Schwere des Punkts
            for i in range(self.cols):  # Beginnt bei 0
                  lowerBound = i / self.cols
                  upperBound = (i + 1) / self.cols

                  if pointSeverity < 1/self.cols:
                        severityCategory = 1
                        break

                  if pointFrequency >= (self.cols - 1)/self.cols:
                        severityCategory = self.cols
                        break

                  if lowerBound <= pointSeverity < upperBound:
                        severityCategory = self.cols - i
                        break


            riskClass = self.representation[frequencyCategory-1][severityCategory-1]
            fieldNum = self.fieldNums[frequencyCategory-1][severityCategory-1]

            print (riskClass, fieldNum)

            return riskClass, fieldNum

