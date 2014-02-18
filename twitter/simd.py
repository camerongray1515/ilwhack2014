from csv import *

class Data():

    def accessData(self):
        with open("access.csv","rb") as csv_file:
          d = DictReader(csv_file)
          return list(d)

    def crimeData(self):
        with open("crime.csv","rb") as csv_file:
          d = DictReader(csv_file)
          return list(d)

    def educationData(self):
        with open("education.csv","rb") as csv_file:
          d = DictReader(csv_file)
          return list(d)

    def employmentData(self):
        with open("employment.csv","rb") as csv_file:
          d = DictReader(csv_file)
          return list(d)

    def healthData(self):
        with open("health.csv","rb") as csv_file:
          d = DictReader(csv_file)
          return list(d)

    def housingData(self):
        with open("housing.csv","rb") as csv_file:
          d = DictReader(csv_file)
          return list(d)

    def incomeData(self):
        with open("income.csv","rb") as csv_file:
          d = DictReader(csv_file)
          return list(d)

    def overallData(self):
        with open("overall.csv","rb") as csv_file:
          d = DictReader(csv_file)
          return list(d)