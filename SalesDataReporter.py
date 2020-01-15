###########################################################################################
# Bruce Rhoades
#
# Sales Data Report
#
# Driver program for SalesData facade class to interface to mock customer data for XYX
# Corporation. 
###########################################################################################

import SalesData as sd

def intro():
    print("""XYZ Corporation started in the begining of 2015 and has expanded across the eastern seaboard. 
    They have expanded their customer base across that area and have maintained customer data from 2015-2018.
    2019 data will be release shortly after the new year. This program provides access to that data and is 
    organized in a variety of ways and in a variety of formats - spreadseets, charts and on screen info. 

    Please select views of data through the menuing system below. Spreadsheets will be outputted to the folder
    that this script exists in and their filenames will be outputted to the console. 

    Enter q at any time to quit. Cheers!\n""")

############################################################################################
# Method to prompt user for Region Selection - Validates for selections of 1, 2, 3 or q only
############################################################################################
def getRegionSelection():
    regions = { '1' : ['Northeast','NE'],  '2' : ['Middle Atlantic','MA'], '3' : ['Southeast','SE']}
    regionSelection = ''
    while (regionSelection != 'q'):
        for key, value in regions.items():
            print(key, value[0])
        
        regionSelection = input("Please select from the above regions: ")
        if(regionSelection not in ['1', '2', '3']):
            if(regionSelection != 'q'):
                print("\nINVALID SELECTION!\n")
            continue
        else:
            regionName = regions[regionSelection]
            regionSelection = regionName[1]
            break

    return regionSelection

############################################################################################
# Method to prompt user for Start Year and End Year Selection - 
# Validates for selections of years 2015-2018, q,  and for Start Year being less than End Year
############################################################################################
def getDateRangeSelection():
    startDateSelection = ''
    endDateSelection = ''
    while (startDateSelection != 'q' and endDateSelection != 'q'):
        startDateSelection = input("Please enter a start year in the range of 2015-2018: ")
        endDateSelection = input("Please enter an end year in the range of 2015-2018: ")
        if(startDateSelection not in ['2015', '2016', '2017', '2018'] or endDateSelection not in ['2015', '2016', '2017', '2018']):
            if(startDateSelection != 'q' and endDateSelection != 'q'):
                print("\nINVALID SELECTION!\n")
            continue
        elif int(startDateSelection) > int(endDateSelection):
            print("\nSTART YEAR MUST BE BEFORE END YEAR")
            continue
        else:
            break

    return startDateSelection, endDateSelection

############################################################################################
# Method to prompt user for Customer Type Selection - Validates for selections of 1, 2, 3 or q only
############################################################################################
def getCustomerTypeSelection():
    customerTypeSelection = ''
    while (customerTypeSelection != 'q'):
        customerTypeSelection = input("Please enter a Customer Type (1, 2, 3 or a for all): ")
        if(customerTypeSelection not in ['1', '2', '3', 'a']):
            if(customerTypeSelection != 'q'):
                print("\nINVALID SELECTION!\n")
            continue
        else:
            break

    return customerTypeSelection


############################################################################################
# Method to prompt user for Process Selection - Validates for selections 
# of 1, 2, 3, 4, 5 or q only
############################################################################################
def getProcessSelection():
    processSelection = ''
    while (processSelection != 'q'):
        processSelection = input("""Please enter a Process to Run: 
        1. Group Customer Data by State
        2. Group Customer Data by Date
        3. Count Customers Data by State
        4. Max Weekly Customer Count
        5. Totals relative to goals, Pct change to prior year, Next Year Forecast\n""")
        if(processSelection not in ['1', '2', '3', '4', '5']):
            if(processSelection != 'q'):
                print("\nINVALID SELECTION!\n")
            continue
        else:
            break

    return processSelection

############################################################################################
# Method to take in several parameters to initialize and parameterize SalesData facade
# regionSelection: NE, MA, SE variables to pass to SalesData
# processTypeSelection: to determine which function within SalesData
# startYearSelection: the beginning year for which to pull data from SalesData
# endYearSelection: the end year for which to pull data from SalesData
# customerTypeSelection: The customer type for which to pull data from SalesData
############################################################################################
def getSalesData(regionSelection, processTypeSelection, startYearSelection, endYearSelection, customerTypeSelection):
    if(sd.SalesData.setYearRangeAndRegion(startYearSelection, endYearSelection, regionSelection) == True):
        custType = 0
        if(customerTypeSelection == 'a'):
            custType = None
        else:
            custType = int(customerTypeSelection)

        if(processTypeSelection == '1'):
            sd.SalesData.exportGroupedByStateDate(custType)
        elif(processTypeSelection == '2'):
            sd.SalesData.exportGroupedByDateState(custType)
        if(processTypeSelection == '3'):
            sd.SalesData.exportCountByState(custType)
        elif(processTypeSelection == '4'):
            sd.SalesData.exportCountByDate(custType)
        if(processTypeSelection == '5'):
            sd.SalesData.annualGoals(custType)


############################################################################################
## Main section to kick off retrieval of options from the user
############################################################################################
intro()
regionSelection = ''
processTypeSelection = ''
startYearSelection = ''
endYearSelection = ''
customerTypeSelection = ''
while((regionSelection != 'q') and (processTypeSelection != 'q') and (startYearSelection != 'q') and 
(endYearSelection != 'q') and (customerTypeSelection != 'q')):
    print("\n\n")
    regionSelection = getRegionSelection()
    if(regionSelection != 'q'):
        processTypeSelection = getProcessSelection()
        if(processTypeSelection != 'q'):
            startYearSelection, endYearSelection = getDateRangeSelection()
            if(startYearSelection != 'q') and (endYearSelection != 'q'):
                customerTypeSelection = getCustomerTypeSelection()
                if(customerTypeSelection != 'q'):
                    getSalesData(regionSelection, processTypeSelection, startYearSelection, endYearSelection, customerTypeSelection)
