import numpy as np


class Matrix:

      def __init__(self, matrixRepresentation, fieldNums, riskLabels, riskColors, xLabels, yLabels):
            self.matrixRepresentation = matrixRepresentation
            self.rows, self.cols = matrixRepresentation.shape
            self.fieldNums = fieldNums
            self.riskLabels = riskLabels
            self.riskColors = riskColors
            self.xLabels = xLabels
            self.yLabels = yLabels
            
      def computeDataPoint(self, pointFrequency, pointSeverity):

            # Berechnung der Häufigkeitsklasse des Punkts (1=am Häufigsten)
            for i in range(1, self.rows):
                  lowerBound = i / self.rows
                  upperBound = (i + 1) / self.rows

                  if (pointFrequency < 1/self.rows):
                       frequencyCategory = self.rows
                       break
                  
                  if (pointFrequency >= (self.rows - 1)/self.rows):
                       frequencyCategory = 1
                       break

                  if (lowerBound <= pointFrequency < upperBound):
                        frequencyCategory = self.rows - i
                        break

            # Berechnung der Schwere des Punkts
            for i in range(1, self.cols):
                  lowerBound = i / self.cols
                  upperBound = (i + 1) / self.cols

                  if (pointSeverity < 1/self.cols):
                       severityCategory = 1
                       break
                  
                  if (pointFrequency >= (self.rows - 1)/self.rows):
                       severityCategory = self.cols
                       break

                  if (lowerBound <= pointFrequency < upperBound):
                        severityCategory = self.rows - i
                        break

            riskClass = self.matrixRepresentation[frequencyCategory-1][severityCategory-1]
            fieldNum = self.fieldNums[frequencyCategory-1][severityCategory-1]

            print (riskClass, fieldNum)

            return riskClass, fieldNum




def main():
    # Example matrixRepresentation and fieldNums
    matrix_rep = np.array([
        [3, 4, 4, 4],   # Häufig
        [2, 3, 4, 4],   # Wahrscheinlich
        [2, 3, 3, 4],   # Gelegentlich
        [1, 2, 3, 3],   # Selten
        [1, 1, 2, 2],   # Unwahrscheinlich
        [1, 1, 1, 1]    # Unvorstellbar
    ])

    field_nums = [
        [1, 2, 3, 4],  # Häufig 
        [5, 6, 7, 8],  # Wahrscheinlich
        [9, 10, 11, 12],  #  Gelegentlich
        [13, 14, 15, 16],  # Selten
        [17, 18, 19, 20],  #  Unwahrscheinlich
        [21, 22, 23, 24]   # Unvorstellbar
    ]

    # Instantiate the Matrix class with sample data
    matrix = Matrix(matrix_rep, field_nums, [], [], [], [])

    # Test with some sample frequencies and severities
    # Sample frequency and severity values (both between 0 and 1)
    test_cases = [
        (0.1, 0.2),  # Lower values
        (0.6, 0.5),  # Mid-range values
        (0.9, 0.8),  # Higher values
        (0.0, 0.0),  # Edge case: both 0
        (1.0, 1.0)   # Edge case: both 1
    ]
    
    # Iterate through the test cases and print the result
    for pointFrequency, pointSeverity in test_cases:
        print(f"Testing with pointFrequency={pointFrequency} and pointSeverity={pointSeverity}:")
        riskClass, fieldNum = matrix.computeDataPoint(pointFrequency, pointSeverity)
        print(f"Risk Class: {riskClass}, Field Number: {fieldNum}\n")

# Run the main function
if __name__ == "__main__":
    main()
