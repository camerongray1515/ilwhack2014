from csv import *

class Data():

	def incomeData(self):
		return csv.DictWriter("crime.csv", ["Data Zone","Local Authority Code","Total Population (SAPE 2010)","Income domain 2012 rank","Income domain 2012 rate (%)","Number of Income Deprived People 2012"])

	def employmentData(self):
		return csv.DictWriter("employment.csv", ["Data Zone","Local Authority Code","Best-fit Working Age Population** (men 16-64, women 16-60 SAPE 2010)","Employment domain 2012 rank","Employment domain 2012 rate (%)","Number of Employment Deprived People 2012 "])

	def healthData(self):
		return csv.DictWriter("health.csv", ["Data Zone","Local Authority Code","Health domain 2012 rank","Standardised mortality ratio (ISD, 2007-2010) ","Comparative illness factor: standardised ratio (DWP, 2011)2","Hospital stays related to alcohol misuse: standardised ratio","Hospital stays related to drug misuse: standardised ratio (ISD, 2007-2010)","Emergency stays in hospital: standardised ratio ","Estimated proportion of population being prescribed drugs for anxiety, depression or psychosis ","Proportion of live singleton births of low birth weight"])