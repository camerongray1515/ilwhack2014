from csv import *

class Data():

    def accessData(self):
        with open("access.csv","rb") as csv_file:
          return csv.reader(csv_file)

    def crimeData(self):
        with open("crime.csv","rb") as csv_file:
          return csv.reader(csv_file)

    def educationData(self):
        with open("education.csv","rb") as csv_file:
          return csv.reader(csv_file)

    def employmentData(self):
        with open("employment.csv","rb") as csv_file:
          return csv.reader(csv_file)

    def healthData(self):
        with open("health.csv","rb") as csv_file:
          return csv.reader(csv_file)

    def housingData(self):
        with open("housing.csv","rb") as csv_file:
          return csv.reader(csv_file)

    def incomeData(self):
        with open("income.csv","rb") as csv_file:
          return csv.reader(csv_file)

    def overallData(self):
        with open("overall.csv","rb") as csv_file:
          return csv.reader(csv_file)