# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 16:21:16 2020
"""

import os
import math
import pandas
import matplotlib.pyplot as plt

class stateAnalysis():
    def __init__(self, stateName, data):
        """
        This function initializes each of the states that are being analyzed.
        
        :param stateName: A string of the state's name. The first letter needs to be capialized
        :param data: A dictionary of dataframes of all of the data for that day
        """
        self.stateName = stateName
        self.confirmedCasesTrend, self.recoveredCasesTrend, self.deathsTrend = self.statistics(data)
            
        
    def statistics(self, dataframeDict):
        """
        This function extracts the confirmed cases, recovered cases, and death
        cases for each of the states. If the information for a certain day is
        not a number, it will be replaced with a zero.
        
        :param dataframeDict: A dictionary of dataframes of all of the data for that day
        :return: A tuple of lists of confirmed cases, recovered cases, and death counts per day
        """
        countOfConfirmedCasesOverTime = list()
        countOfRecoveredCasesOverTime = list()
        countOfDeathsOverTime = list()           
        for key, value in dataframeDict.items():
            if value.columns[0] == r"Province/State":
                for row in value.itertuples():
                    if row[2] == "US" and row[1] == self.stateName:
                        if math.isnan(row[4]):
                            countOfConfirmedCasesOverTime.append(0)
                        else:
                            countOfConfirmedCasesOverTime.append(row[4])
                        if math.isnan(row[5]):
                            countOfDeathsOverTime.append(0)
                        else:
                            countOfDeathsOverTime.append(row[5])
                        if math.isnan(row[6]):
                            countOfRecoveredCasesOverTime.append(0)
                        else:
                            countOfRecoveredCasesOverTime.append(row[6])
            elif value.columns[2] == r"Province_State":
                subtotalConfirmed = 0
                subtotalDeaths = 0
                subtotalRecovered = 0
                for row in value.itertuples():
                    if row[4] == "US" and row[3] == self.stateName:
                        if math.isnan(row[8]):
                            pass
                        else:
                            subtotalConfirmed = subtotalConfirmed + row[8]
                        if math.isnan(row[9]):
                            pass
                        else:
                            subtotalDeaths = subtotalDeaths + row[9]
                        if math.isnan(row[10]):
                            pass
                        else:
                            subtotalRecovered = subtotalRecovered + row[10]
                countOfConfirmedCasesOverTime.append(subtotalConfirmed)
                countOfRecoveredCasesOverTime.append(subtotalRecovered)
                countOfDeathsOverTime.append(subtotalDeaths)
            else:
                raise IOError("Unknown CSV data structure. This script can handle the "
                              "first two types of the data structure from John Hopkins "
                              "University.")
        return countOfConfirmedCasesOverTime, countOfRecoveredCasesOverTime, countOfDeathsOverTime

    
    def plotConfirmedCases(self):
        """
        This function plots the confirmed cases for this state.
        """
        data = self.confirmedCasesTrend.copy()
        self.plottingData(f"Confirmed Cases over Time ({self.stateName})", data)

    
    def plotRecoveredCases(self):
        """
        This function plots the recovered cases for this state.
        """
        data = self.recoveredCasesTrend
        self.plottingData(f"Recovered Cases over Time ({self.stateName})", data)

    
    def plotDeathCases(self):
        """
        This function plots the death cases for this state.
        """
        data = self.deathsTrend
        self.plottingData(f"Death Cases over Time ({self.stateName})", data)

    
    def plottingData(self, title, data, xLabel = "Days", yLabel = "Cases"):
        """
        This function plots the data for each of the cases above.
        
        :param title: A string oof the title for the graph.
        :param data: A list of the number of cases confirmed over time
        :param xLabel: A string of the x-axis label
        :param yLabel: A string of the y-axis label
        """
        plt.figure()
        plt.title(title)
        plt.xlabel(xLabel)
        plt.ylabel(yLabel)
        plt.plot(data)
        plt.grid(b = True, which = "both")
        
        
def collectData(dataPath = r".\COVID-19\csse_covid_19_data\csse_covid_19_daily_reports"):
    """
    This function collects the daily csv updates.
    
    :param dataPath: A string to the path to the directory holding the daily reports
    :return: A dictionary of dataframes for the csv for each of the days
    """
    dataframeDict = dict()
    for root, _, files in os.walk(dataPath):
        for file in files:
            if file.endswith(".csv"):
               dataframe = pandas.read_csv(os.path.join(root,file))
               date = os.path.splitext(file)[0]
               dataframeDict[date] = dataframe
    return dataframeDict


            
if __name__ == "__main__":
    counter = 0
    stateObjs = dict()
    dataframeDict = collectData()
    statesList = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
              "Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois",
              "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
              "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
              "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
              "North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
              "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
              "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]
    for state in statesList:
        stateObjs[state] = stateAnalysis(state, dataframeDict)
    fig, axs = plt.subplots(7, 8)
    for rowNumber in range(7):
        for columnNumber in range(8):
            axs[rowNumber, columnNumber].plot(stateObjs[statesList[counter]].confirmedCasesTrend)
            axs[rowNumber, columnNumber].text(0.1, 0.75, 
                                              stateObjs[statesList[counter]].stateName,
                                              transform = axs[rowNumber, columnNumber].transAxes)
            axs[rowNumber, columnNumber].grid(b = False, which = "both")
            counter = counter + 1
            if counter > 49:
                break
        if counter > 49:
            break
    for ax in axs.flat:
        ax.set(xlabel="Days", ylabel="Cases")
    fig.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.6, hspace=0.3)
    fig.show()