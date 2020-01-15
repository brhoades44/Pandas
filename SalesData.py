###########################################################################################
# Bruce Rhoades 11/4/2019
#
# Sales Data class. This class serves as a facade over the processing of customer data
# Given a start year, end year and a region, a variety of data can be generated:
# 1.) Customer Data grouped by State and then Date for customer types
# 2.) Customer Data grouped by Date and then State for customer types
# 3.) Totals for each state for customer types
# 4.) Totals for each date for customer types
# 5.) Annual Data relative to Goals including percentage change year over year and next
# year's forecast
#
# Data exported to spreadhseet for all processes and charts displayed for some
#
# TODO: Add Exception Handling
#
# Cheers!
###########################################################################################

import matplotlib
import matplotlib.pyplot as plt
import numpy.random as np
import os
import pandas as pd
import random

class SalesData:
    excelFileName = ''
    region = ''
    startYear = ''
    endYear = ''

    ############################################################################################
    # Method to initialize the processing of data with a new region and date range
    ############################################################################################
    @staticmethod
    def setYearRangeAndRegion(startYear, endYear, region='NE', NumberOfSources=4):
        sYear = int(startYear)
        eYear = int(endYear)
        if(sYear < 2015 or eYear > 2018 or sYear > eYear):
            print("Please Enter a Valid Start and End Year Between 2015 and 2018")
            return False
        
        if(region not in ['NE', 'MA', 'SE']):
            print("Please Enter a Valid Region Value of NE, MA or SE")
            return False        
            
        SalesData.region = region
        SalesData.startYear = startYear
        SalesData.endYear = endYear
        SalesData.excelFileName = SalesData.region + 'SalesData' + SalesData.startYear + '-' + SalesData.endYear + '.xlsx'

        # create a raw data spreadsheet file if one does not already exist for date range and region
        if(os.path.isfile(SalesData.excelFileName) == False):
            SalesData.__generateSalesData(NumberOfSources)
        return True

    ############################################################################################   
    # Function to mimic pulling in sales data for a requested 
    # year range and region and outputting to spreadsheet
    ############################################################################################
    @staticmethod
    def __generateSalesData(NumberOfSources):        
        dataSet = []
        
        # Generate Customer Statuses
        states = []
        status = [1,2,3]

        # Generate regions and their states
        # lower case states to mimic inconsistent data 
        # amonst data "sources"
        if(SalesData.region=='NE'):
            np.seed(111)
            states = ['NY','NJ','PA','nj','CT']
        elif(SalesData.region=='MA'):
            np.seed(110)
            states = ['DE','MD','md','VA','WV']
        elif(SalesData.region=='SE'):
            np.seed(112)
            states = ['NC','nc','SC','GA','FL']
        else:
            print("Invalid Region Entered")
            return

        # Generate data for each data "source"
        for i in range(NumberOfSources):
            
            # Create a weekly (mondays) date range
            startRange = '1/1/' + SalesData.startYear
            endRange = '12/31/' + SalesData.endYear
            rng = pd.date_range(start=startRange, end=endRange, freq='W-MON')
            
            # Create random customer data
            data = np.randint(low=100,high=700,size=len(rng))
            
            # Make a random list of statuses
            random_status = [status[np.randint(low=0,high=len(status))] for i in range(len(rng))]
            
            # Make a random list of states 
            random_states = [states[np.randint(low=0,high=len(states))] for i in range(len(rng))]
        
            dataSet.extend(zip(random_states, random_status, data, rng))

        # export data to spreadsheet file
        SalesData.__exportRawSalesData(dataSet)

    ############################################################################################
    # Method to Read Data from the Raw Data spreadsheet, and "Clean" by upper casing States 
    ############################################################################################
    @staticmethod
    def __cleanSalesData():
        df = pd.read_excel(SalesData.excelFileName, 0, index_col='StatusDate')
        # some states coming in as lower case, so upper them
        df['State'] = df.State.apply(lambda x: x.upper())
        return df

    ############################################################################################
    # Method to export raw sales (customer) data to a spreadsheet file. This file serves as the 
    # Main Data set to be used in the application
    ############################################################################################
    @staticmethod
    def __exportRawSalesData(dataSet):
        dataFrame = pd.DataFrame(data=dataSet, columns=['State','Status','CustomerCount','StatusDate'])
        print("Generating Raw Data Spreadsheet file:", SalesData.excelFileName)
        dataFrame.to_excel(SalesData.excelFileName, index=False)
    
    ############################################################################################
    # Method to export the given dataFrame to a spreadheet with the given file name
    ############################################################################################
    @staticmethod
    def __exportSalesData(dataFrame, fileName):
        filename = SalesData.region + fileName + SalesData.startYear + '-' + SalesData.endYear + '.xlsx'
        print("Generating Spreadsheet file:", filename)
        dataFrame.to_excel(filename, index=True)
    
    
    ############################################################################################
    # Method to group Customer Data By State and then by Date.
    # Parameter status: If not given, data for all Customer Statuses will be used
    ############################################################################################
    @staticmethod
    def __groupByStateDate(status=None):
        # get "clean" data from the raw data file
        df = SalesData.__cleanSalesData()
        if(status != None and status not in [1,2,3]):
            print("Invalid Status Value")
            return

        # group the data by State and then Date
        if(status != None):
            mask = df['Status'] == status
            df = df[mask]
            del df['Status']
            grouped = df.reset_index().groupby(['State','StatusDate']).sum()
        else:
            grouped = df.reset_index().groupby(['State','StatusDate','Status']).sum()
            
        return grouped

    ############################################################################################
    # Helper method to generate chart titles and labels given a DataFrame and a Customer Status
    ############################################################################################
    @staticmethod
    def __getChartNames(df, status):
        chartNames = []
        if(len(df.index) > 0):
            chartNames.append(df.index[0][0])
            temp = chartNames[0]
            for value in df.index:
                if(value[0] != temp):
                    chartNames.append(value[0])
                    temp = value[0]
        # Add titles
        if('NJ' in chartNames):
            chartTitle = 'New Customer Totals for Northeast Region'
        elif('MD' in chartNames):
            chartTitle = 'New Customer Totals for Middle Atlantic Region'
        else:
            chartTitle = 'New Customer Totals for Southeast Region'
        
        chartTitle = chartTitle + " (Customer Type " + str(status) + ")"
        return chartTitle, chartNames

    
    ############################################################################################
    # Method to export customer information to a spreadsheet and, if a status is specified, 
    # a chart, grouped by State and then by date. 
    # Param status to indicate which customer type to report on. If none, all 3 will be reported
    ############################################################################################
    @staticmethod
    def exportGroupedByStateDate(status=None):
        # get the data grouped by State and then Date and output to spreadsheet 
        grouped = SalesData.__groupByStateDate(status)
        fileName = 'GroupedByStateDate'
        if(status != None):
            fileName += '[Status' + str(status) + ']'
        SalesData.__exportSalesData(grouped, fileName)

        # Create graphs for each state if status is specified
        # TODO: show graphs for multiple statuses
        if(status != None):
            fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(20, 10))
            fig.subplots_adjust(hspace=1.0) 

            # Set chart labels and plot the chart data
            chartTitle, chartNames = SalesData.__getChartNames(grouped, status)
            grouped.loc[chartNames[0]]['CustomerCount'][SalesData.startYear:SalesData.endYear].fillna(method='pad').plot(ax=axes[0,0])
            grouped.loc[chartNames[1]]['CustomerCount'][SalesData.startYear:SalesData.endYear].fillna(method='pad').plot(ax=axes[0,1]) 
            grouped.loc[chartNames[2]]['CustomerCount'][SalesData.startYear:SalesData.endYear].fillna(method='pad').plot(ax=axes[1,0])
            if len(chartNames) > 3:
                grouped.loc[chartNames[3]]['CustomerCount'][SalesData.startYear:SalesData.endYear].fillna(method='pad').plot(ax=axes[1,1])

            fig.suptitle(chartTitle, fontsize=16)
            axes[0,0].set_title(chartNames[0])
            axes[0,1].set_title(chartNames[1])
            axes[1,0].set_title(chartNames[2])
            if len(chartNames) < 4:
                axes[1,1].set_title('Intentionally Left Blank')
            else:
                axes[1,1].set_title(chartNames[3])
            plt.show()
    
    
    ############################################################################################
    # Method to group Customer Data By Date and then by State.
    # Parameter status: If not given, data for all Customer Statuses will be used
    ############################################################################################
    @staticmethod
    def __groupByDateState(status=None):
        # pull in clean customer data
        df = SalesData.__cleanSalesData()
        if(status != None and status not in [1,2,3]):
            print("Invalid Status Value")
            return

        # group data by Date and then State, and also Customer Status if given
        if(status != None):
            mask = df['Status'] == status
            df = df[mask]
            del df['Status']
            grouped = df.reset_index().groupby(['StatusDate','State']).sum()
        else:
            grouped = df.reset_index().groupby(['StatusDate','State','Status']).sum()
            
        return grouped


    ############################################################################################
    # Method to export customer information to a spreadsheet and, if a status is specified, 
    # a chart, grouped by Date and then by state. 
    # Param status to indicate which customer type to report on. If none, all 3 will be reported
    ############################################################################################
    @staticmethod
    def exportGroupedByDateState(status=None):
        grouped = SalesData.__groupByDateState(status)
        fileName = 'GroupedByDateState'
        if(status != None):
            fileName += '[Status' + str(status) + ']'

        SalesData.__exportSalesData(grouped, fileName)


    ############################################################################################
    # Method to sum the number of customers relative to State
    ############################################################################################
    @staticmethod
    def __countByState(status=None):
        # group customers by state
        df = SalesData.__groupByStateDate(status)
        
        # Get the count by State
        maxByDateAndMonth = pd.DataFrame(df['CustomerCount'].groupby(df.index.get_level_values(0)).sum())
        return maxByDateAndMonth


    ############################################################################################
    # Method to export customer count data by state to spreadsheet and bar chart
    ############################################################################################
    @staticmethod
    def exportCountByState(status=None):
        # get the customer counts
        df = SalesData.__countByState(status)

        # export data to spreadsheet
        fileName = 'CountByState'
        if(status != None):
            fileName += '[Status' + str(status) + ']'

        SalesData.__exportSalesData(df, fileName)

        # plot on bar graph
        chartTitle = "New Customer Count for " + SalesData.startYear + " - " + SalesData.endYear
        if(status != None):
            chartTitle = chartTitle + " (Customer Type " + str(status) + ")"

        x = []
        lenIndex = len(df.index)
        for i in range(0, lenIndex):
            x.append(i)

        plt.bar(x, df['CustomerCount'])
        plt.title(chartTitle)
        plt.xticks(x, df.index)
        plt.show()


    ############################################################################################
    # Method to sum the number of customers relative to Date and output maximum weekly values
    # for each month
    ############################################################################################
    @staticmethod
    def __countByDate(status=None):
        df = SalesData.__groupByDateState(status)
        # Get the customer count by Date
        maxByDateAndMonth = pd.DataFrame(df['CustomerCount'].groupby(df.index.get_level_values(0)).sum())
        
        # Group by Year and Month
        yearMonth = maxByDateAndMonth.groupby([lambda x: x.year, lambda x: x.month])

        # What is the max customer count per Year and Month
        maxByDateAndMonth['Max'] = yearMonth['CustomerCount'].transform(lambda x: x.max())
        return maxByDateAndMonth

    
    ############################################################################################
    # Method to export maximum weekly values for each month and output to spreadsheet and chart
    ############################################################################################
    @staticmethod
    def exportCountByDate(status=None):
        # get values and export to spreadsheet
        maxed = SalesData.__countByDate(status)
        fileName = 'MaxWeeklyCountByDate'
        if(status != None):
            fileName += '[Status' + str(status) + ']'

        SalesData.__exportSalesData(maxed, fileName)

        # plot on line graph
        chartTitle = "Max Weekly Customer Count"
        if(status != None):
            chartTitle = chartTitle + " (Customer Type " + str(status) + ")"

        maxed['Max'].plot(figsize=(10, 5));plt.title(chartTitle)
        plt.show()
    
    
    ############################################################################################
    # Method to generate Goals per year, annual customer totals, pct change year over year
    # and next year forecasts
    ############################################################################################
    @staticmethod
    def annualGoals(status=None):
        # Create the annual goal dataframe. Use higher goals for when status is None which means
        # for all customer statuses
        data = []
        yearDiff = int(SalesData.endYear) - int(SalesData.startYear) + 1
        if(status==None):
            for i in range(0, yearDiff):
                data.append(80000 + (i*2000))
        else:
            for i in range(0, yearDiff):
                data.append(25000 + (i*5000))

        startRange = '12/31/' + SalesData.startYear
        endRange = '12/31/' + SalesData.endYear
        idx = pd.date_range(start=startRange, end=endRange, freq='A')
        annualGoal = pd.DataFrame(data, index=idx, columns=['AnnualGoal'])

        # Generate pct change data, forecasts and output to console and spreadsheet
        maxByDateAndMonth = SalesData.__countByDate(status)
        del maxByDateAndMonth['Max']
        combined = pd.concat([maxByDateAndMonth,annualGoal], axis=0, sort=False)
        Year = combined.groupby(lambda x: x.year).sum()
        Year['YR_PCT_Change'] = Year['CustomerCount'].pct_change(periods=1)
        print(Year)
        lastYear = int(SalesData.endYear)
        print(lastYear+1, "Forecast:", ((1 + Year.loc[lastYear,'YR_PCT_Change']) * Year.loc[lastYear,'CustomerCount']))

        #TODO: Output to bar chart instead of outputting to command line
        fileName = 'AnnualGoals'
        if(status != None):
            fileName += '[Status' + str(status) + ']'

        SalesData.__exportSalesData(Year, fileName)


