# StockData.py
# Andrew Dinh
# Python 3.6.1
# Description: Returns all available dates and prices for each stock requested.

'''
Available API's: Can it do mutual funds?
IEX: No
Alpha Vantage (AV): Yes
Tiingo: Yes
Barchart: No
'''

# Alpha Vantage API Key: O42ICUV58EIZZQMU
# Barchart API Key: a17fab99a1c21cd6f847e2f82b592838 # Possible other one? f40b136c6dc4451f9136bb53b9e70ffa
# Tiingo API Key: 2e72b53f2ab4f5f4724c5c1e4d5d4ac0af3f7ca8
# Tradier API Key: n26IFFpkOFRVsB5SNTVNXicE5MPD
# If you're going to take these API keys and abuse it, you should really reconsider your life priorities

apiAV = 'O42ICUV58EIZZQMU'
#apiBarchart = 'a17fab99a1c21cd6f847e2f82b592838'        # 150 getHistory queries per day
apiBarchart = 'f40b136c6dc4451f9136bb53b9e70ffa'
apiTiingo = '2e72b53f2ab4f5f4724c5c1e4d5d4ac0af3f7ca8'
apiTradier = 'n26IFFpkOFRVsB5SNTVNXicE5MPD'
'''
Monthly Bandwidth = 5 GB
Hourly Requests = 500
Daily Requests = 20,000
Symbol Requests = 500
'''

import requests, json
from datetime import datetime

class StockData:

  def __init__(self, newName = '', newAbsFirstLastDates = [], newFinalDatesAndClose = [], newFinalDatesAndClose2 = [],newAllLists = []):
    self.name = newName                             # Name of stock
    self.absFirstLastDates = newAbsFirstLastDates   # Absolute first and last dates from all sources
    self.finalDatesAndClose = newFinalDatesAndClose # All available dates with corresponding close values
    self.finalDatesAndClose2 = newFinalDatesAndClose2 # After some consideration, I decided to keep what I had already done here and make a new list that's the same except dates are in datetime format
    self.allLists = newAllLists
    '''
    Format:
    # List from each source containing: [firstDate, lastDate, allDates, values, timeFrame]
    # firstDate & lastDate = '2018-12-18' (year-month-date)
    allDates = ['2018-12-17', '2018-12-14'] (year-month-date)
    values (close) = ['164.6307', 164.6307]
    timeFrame = [days, weeks, years]
    '''

  def set(self, newName, newFirstLastDates, newAbsFirstLastDates, newFinalDatesAndClose, newAllLists):
    self.name = newName                             # Name of stock
    self.firstLastDates = newFirstLastDates         # Dates that at least 2 sources have (or should it be all?) - Maybe let user decide
    self.absFirstLastDates = newAbsFirstLastDates   # Absolute first and last dates from all sources
    self.finalDatesAndClose = newFinalDatesAndClose
    self.allLists = newAllLists

  def setName(self, newName):
    self.name = newName
  def returnName(self):
    return self.name
  def returnAllLists(self):
    return self.allLists
  def returnAbsFirstLastDates(self):
    return self.absFirstLastDates
  def returnAllLists(self):
    return self.allLists
  def returnFinalDatesAndClose(self):
    return self.finalDatesAndClose
  def returnFinalDatesAndClose2(self):
    return self.finalDatesAndClose2

  def getIEX(self):
    url = ''.join(('https://api.iextrading.com/1.0/stock/', self.name, '/chart/5y'))
    #link = "https://api.iextrading.com/1.0/stock/spy/chart/5y"
    print("\nSending request to:", url)
    f = requests.get(url)
    json_data = f.text
    #print(json_data)
    if (json_data == 'Unknown symbol'):
      print("IEX not available")
      return 'Not available'
    loaded_json = json.loads(json_data)
    listIEX = []

    print("\nFinding first and last date")
    # Adding (firstDate, lastDate) to listIEX
    # Find firstDate (comes first)
    firstLine = loaded_json[0]
    #print("firstLine:", firstLine)
    firstDate = firstLine['date']
    #print("firstDate:",firstDate)
    # Find lastDate (comes last)
    lastLine = loaded_json[-1] # Returns last value of the list (Equivalent to len(loaded_json)-1)
      #print("lastLine:", lastLine)
    lastDate = lastLine['date']
    #print("last date:", lastDate)
    listIEX.append(firstDate)
    listIEX.append(lastDate)
    print(listIEX[0], ',', listIEX[1])

    print("\nFinding all dates given")
    allDates = []
#   for i in range(0, len(loaded_json), 1): # If you want to do oldest first
    for i in range(len(loaded_json)-1, -1, -1):
      line = loaded_json[i]
      date = line['date']
      allDates.append(date)
    listIEX.append(allDates)

    #print(listIEX[2])
    print(len(listIEX[2]), "dates")

    print("\nFinding close values for each date")
    values = []
#   for i in range(0, len(loaded_json), 1): # If you want to do oldest first
    for i in range(len(loaded_json)-1, -1, -1):
      line = loaded_json[i]
      value = line['close']
      values.append(value)
    listIEX.append(values)
    #print(listIEX[3])
    print(len(listIEX[3]), "close values")

    print("\nFinding time frame given [days, weeks, years]")
    timeFrame = []
    d1 = datetime.strptime(firstDate, "%Y-%m-%d")
    d2 = datetime.strptime(lastDate, "%Y-%m-%d")
    timeFrameDays = abs((d2 - d1).days)
    #print(timeFrameDays)
    timeFrameYears = float(timeFrameDays / 365)
    timeFrameWeeks = float(timeFrameDays / 7)
    timeFrame.append(timeFrameDays)
    timeFrame.append(timeFrameWeeks)
    timeFrame.append(timeFrameYears)
    listIEX.append(timeFrame)
    print(listIEX[4])

    return listIEX

  def getAV(self):
    listAV = []
    #url = ''.join(('https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=', self.name, '&apikey=', apiAV))
    # https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=MSFT&apikey=demo

    #url = ''.join(('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=', self.name, '&outputsize=full&apikey=', apiAV))
    # https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=MSFT&outputsize=full&apikey=demo

    url = ''.join(('https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=', self.name, '&outputsize=full&apikey=', apiAV))
    # https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=MSFT&outputsize=full&apikey=demo

    print("\nSending request to:", url)
    print("(This will take a while)")
    f = requests.get(url)
    json_data = f.text
    loaded_json = json.loads(json_data)
    #print(loaded_json)

    #print(type(loaded_json)) # Dictionary
    #print(len(loaded_json))
    if len(loaded_json) == 1:
      print("Alpha Vantage not available")
      return 'Not available'

    #print(loaded_json['Monthly Time Series'])
    dailyTimeSeries = loaded_json['Time Series (Daily)']
    #print(monthlyTimeSeries)
    listOfDates = list(dailyTimeSeries)
    #print(listOfDates)

    firstDate = listOfDates[-1]
    lastDate = listOfDates[0]
    #print("firstDate:", firstDate)
    #print("lastDate:", lastDate)
    listAV.append(firstDate)
    listAV.append(lastDate)
    listAV.append(listOfDates)

    print("\nFinding first and last date")
    print(listAV[0], ',', listAV[1])
    print("\nFinding all dates given")
    #print(listAV[2])
    print(len(listAV[2]), "dates")

    print("\nFinding close values for each date")
    values = []
    for i in range(0, len(listOfDates), 1):
      temp = listOfDates[i]
      loaded_json2 = dailyTimeSeries[temp]
      #value = loaded_json2['4. close']
      value = loaded_json2['5. adjusted close']
      values.append(value)
    listAV.append(values)
    #print(listOfDates[0])
    #i = listOfDates[0]
    #print(monthlyTimeSeries[i])
    #print(listAV[3])
    print(len(listAV[3]), "close values")

    print("\nFinding time frame given [days, weeks, years]")
    timeFrame = []
    d1 = datetime.strptime(firstDate, "%Y-%m-%d")
    d2 = datetime.strptime(lastDate, "%Y-%m-%d")
    timeFrameDays = abs((d2 - d1).days)
    #print(timeFrameDays)
    timeFrameYears = float(timeFrameDays / 365)
    timeFrameWeeks = float(timeFrameDays / 7)
    timeFrame.append(timeFrameDays)
    timeFrame.append(timeFrameWeeks)
    timeFrame.append(timeFrameYears)
    listAV.append(timeFrame)
    print(listAV[4])

    return listAV

  def getTiingo(self):
    '''
    #OR we can use the token directly in the url
    headers = {
       'Content-Type': 'application/json'
       }
    requestResponse = requests.get("https://api.tiingo.com/api/test?token=<TOKEN>",
                                  headers=headers)
    print(requestResponse.json())
    '''
    token = ''.join(('Token ', apiTiingo))
    headers = {
      'Content-Type': 'application/json',
      'Authorization' : token
       }
    url = ''.join(('https://api.tiingo.com/tiingo/daily/', self.name))
    print("\nSending request to:", url)
    requestResponse = requests.get(url, headers=headers)
    #print(requestResponse.json())
    loaded_json = requestResponse.json()
    #print(len(loaded_json))
    if len(loaded_json) == 1:
      print("Tiingo not available")
      return 'Not available'
    #print(loaded_json)
    '''
    list1 = list(loaded_json)
    for i in range (0, len(list1), 1):
      if list1[i] == 'startDate':
        startNum = i
      elif list1[i] == 'endDate':
        endNum = i
    print(list1[startNum])
    print(list1[endNum])
    '''
    listTiingo = []

    print("\nFinding first and last date")
    firstDate = loaded_json['startDate']
    lastDate = loaded_json['endDate']
    #print(firstDate)
    #print(lastDate)
    listTiingo.append(firstDate)
    listTiingo.append(lastDate)
    print(listTiingo[0], ',', listTiingo[1])

    print("\nFinding all dates given")
    dates = []
    values = [] # Used loop for finding values
    url2 = ''.join((url, '/prices?startDate=', firstDate, '&endDate=', lastDate))
    # https://api.tiingo.com/tiingo/daily/<ticker>/prices?startDate=2012-1-1&endDate=2016-1-1
    print("\nSending request to:", url2)
    requestResponse2 = requests.get(url2, headers=headers)
    loaded_json2 = requestResponse2.json()
    #print(loaded_json2)
    #print(len(loaded_json2))
    for i in range(len(loaded_json2)-1, -1, -1):
      line = loaded_json2[i]
      dateWithTime = line['date']
      temp = dateWithTime.split('T00:00:00.000Z')
      date = temp[0]
      dates.append(date)

      value = line['close']
      values.append(value)
    listTiingo.append(dates)
    #print(listTiingo[2])
    print(len(listTiingo[2]), "dates")

    print("Finding close values for each date")
    # Used loop from finding dates
    listTiingo.append(values)
    #print(listTiingo[3])
    print(len(listTiingo[3]), "close values")

    print("Finding time frame given [days, weeks, years]")
    timeFrame = []
    d1 = datetime.strptime(firstDate, "%Y-%m-%d")
    d2 = datetime.strptime(lastDate, "%Y-%m-%d")
    timeFrameDays = abs((d2 - d1).days)
    #print(timeFrameDays)
    timeFrameYears = float(timeFrameDays / 365)
    timeFrameWeeks = float(timeFrameDays / 7)
    timeFrame.append(timeFrameDays)
    timeFrame.append(timeFrameWeeks)
    timeFrame.append(timeFrameYears)
    listTiingo.append(timeFrame)
    print(listTiingo[4])

    return listTiingo

  def getFirstLastDate(self, listOfFirstLastDates):
    listOfFirstDates = []
    listOfLastDates = []
    #print(len(listOfFirstLastDates))
    for i in range (0, len(listOfFirstLastDates), 1):
      firstLastDates = listOfFirstLastDates[i]
      firstDate = firstLastDates[0]
      lastDate = firstLastDates[1]
      listOfFirstDates.append(firstDate)
      listOfLastDates.append(lastDate)
    #print(listOfFirstDates)
    #print(listOfLastDates)
    for i in range (0, len(listOfFirstDates), 1):
      date = listOfFirstDates[i]
      if i == 0:
        firstDate = date
        yearMonthDay = firstDate.split('-')
        firstYear = yearMonthDay[0]
        firstMonth = yearMonthDay[1]
        firstDay = yearMonthDay[2]
      else:
        yearMonthDay = date.split('-')
        year = yearMonthDay[0]
        month = yearMonthDay[1]
        day = yearMonthDay[2]
        if year < firstYear or (year == firstYear and month < firstMonth) or (year == firstYear and month == firstMonth and day < firstDay):
          firstDate = date
          firstYear = year
          firstMonth = month
          firstDay = day
    #print(firstDate)
    if len(listOfFirstDates) > 1:
      for i in range(0, len(listOfLastDates),1):
        date = listOfLastDates[i]
        if i == 0:
          lastDate = date
          yearMonthDay = lastDate.split('-')
          lastYear = yearMonthDay[0]
          lastMonth = yearMonthDay[1]
          lastDay = yearMonthDay[2]
        else:
          yearMonthDay = date.split('-')
          year = yearMonthDay[0]
          month = yearMonthDay[1]
          day = yearMonthDay[2]
        if year > lastYear or (year == lastYear and month > lastMonth) or (year == lastYear and month == lastMonth and day > lastDay):
          lastDate = date
          lastYear = year
          lastMonth = month
          lastDay = day
    #print(lastDate)
    absFirstLastDates = []
    absFirstLastDates.append(firstDate)
    absFirstLastDates.append(lastDate)
    return absFirstLastDates

  def getFinalDatesAndClose(self):
    # finalDates and finalClose will coincide (aka i = 1 will correspond to one another)
    finalDatesAndClose = [] # Will combine finalDates then finalClose
    finalDates = []
    finalClose = []
    #print(self.absFirstLastDates)
    absFirstDate = self.absFirstLastDates[0]
    absLastDate = self.absFirstLastDates[1]
    date = absFirstDate

    allLists = self.allLists
    while date != absLastDate: # DOESN'T DO LAST DATE
      tempListOfClose = []
      found = False
      for j in range(0, len(allLists), 1):      # Look for date in all lists
        list1 = allLists[j]
        listOfDates = list1[2]
        listOfClose = list1[3]
        for k in range(0, len(listOfDates), 1):
          if listOfDates[k] == date:
            if found == False:
              finalDates.append(date)
              found = True
            #print(listOfDates[k])
            #print(listOfClose[k])
            #print(listOfClose)
            tempListOfClose.append(float(listOfClose[k]))
            k = len(listOfDates) # Dates don't repeat

      if found == True:
        sum = 0
        for r in range(0, len(tempListOfClose), 1):
          sum = sum + tempListOfClose[r]
        close = sum/len(tempListOfClose)

        finalClose.append(close)
        #print(close)

      # Go to the next day
      yearMonthDay = date.split('-')
      year = int(yearMonthDay[0])
      month = int(yearMonthDay[1])
      day = int(yearMonthDay[2])

      day = day + 1
      if day == 32 and month == 12: # Next year
        day = 1
        month = 1
        year = year + 1
      elif day == 32:              # Next month
        month = month + 1
        day = 1
      if day < 10:
        day = ''.join(('0', str(day)))
      if month < 10:
        month = ''.join(('0', str(month)))
      date = ''.join((str(year), '-', str(month), '-', str(day)))
      #print(date)

    # For last date
    finalDates.append(date)
    tempListOfClose = []
    for j in range(0, len(allLists), 1):      # Look for date in all lists
      list1 = allLists[j]
      listOfDates = list1[2]
      listOfClose = list1[3]
      for k in range(0, len(listOfDates), 1):
        if listOfDates[k] == date:
          tempListOfClose.append(float(listOfClose[k]))
          k = len(listOfDates) # Dates don't repeat
    sum = 0
    for r in range(0, len(tempListOfClose), 1):
      sum = sum + tempListOfClose[r]
    close = sum/len(tempListOfClose)
    finalClose.append(close)
    #print(finalDates)
    #print(finalClose)

    # Want lists from most recent to oldest, comment this out if you don't want that
    finalDates = list(reversed(finalDates))
    finalClose = list(reversed(finalClose))

    finalDatesAndClose.append(finalDates)
    finalDatesAndClose.append(finalClose)
    return finalDatesAndClose

  def datetimeDates(self):
      finalDatesAndClose2 = []
      finalDatesAndClose = self.finalDatesAndClose
      finalDatesStrings = finalDatesAndClose[0]
      finalClose = finalDatesAndClose[1]
      finalDates = []

      from Functions import Functions
      for i in range(0, len(finalDatesStrings), 1):
          temp = Functions.stringToDate(finalDatesStrings[i])
          finalDates.append(temp)
      #print(finalDates)

      finalDatesAndClose2.append(finalDates)
      finalDatesAndClose2.append(finalClose)
      return(finalDatesAndClose2)

  def is_connected():
    import socket # To check internet connection
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("www.andrewkdinh.com", 80))
        return True
    except OSError:
        #pass
        print("\nNo internet connection!")
    return False

  def main(self):
    print('Beginning StockData.py')
    
    import importlib.util, sys # To check whether a package is installed

    packages = ['requests']
    for i in range(0, len(packages), 1):
      package_name = packages[i]
      spec = importlib.util.find_spec(package_name)
      if spec is None:
        print(package_name +" is not installed\nPlease type in 'pip install -r requirements.txt' to install all required packages")

    # Test internet connection
    internetConnection = StockData.is_connected()
    if internetConnection == False:
      return

    listOfFirstLastDates = []
    self.allLists = []

    print('\nNOTE: Only IEX and Alpha Vantage support adjusted returns')
    print('NOTE: Only Alpha Vantage and Tiingo support mutual fund data')

    # IEX
    print("\nIEX")
    listIEX = StockData.getIEX(self)
    #print(listIEX)
    if listIEX != 'Not available':
      listOfFirstLastDates.append((listIEX[0], listIEX[1]))
      self.allLists.append(listIEX)

    # Alpha Vantage
    print("\nAlpha Vantage (AV)")
    listAV = StockData.getAV(self)
    #print(listAV)
    if listAV != 'Not available':
      listOfFirstLastDates.append((listAV[0], listAV[1]))
      self.allLists.append(listAV)

    # COMMENTED OUT FOR NOW B/C LIMITED
    '''
    print("\nTiingo")
    print("NOTE: Tiingo does not return adjusted returns!!")
    listTiingo = StockData.getTiingo(self)
    #print(listTiingo)
    if listTiingo != 'Not available':
      listOfFirstLastDates.append((listTiingo[0], listTiingo[1]))
      self.allLists.append(listTiingo)
    '''

    #print(self.allLists)
    #print(listOfFirstLastDates)
    if (len(self.allLists) > 0):
      print("\n", end='')
      print(len(self.allLists), "available source(s) for", self.name)
      self.absFirstLastDates = StockData.getFirstLastDate(self, listOfFirstLastDates)
      print("\nThe absolute first date with close values is:", self.absFirstLastDates[0])
      print("The absolute last date with close values is:", self.absFirstLastDates[1])

      print("\nCombining dates and averaging close values")
      self.finalDatesAndClose = StockData.getFinalDatesAndClose(self) # Returns [List of Dates, List of Corresponding Close Values]
      #print("All dates available:", self.finalDatesAndClose[0])
      #print("All close values:\n", self.finalDatesAndClose[1])
      finalDates = self.finalDatesAndClose[0]
      finalClose = self.finalDatesAndClose[1]
      print(len(finalDates), "unique dates:", finalDates[len(finalDates)-1], "...", finalDates[0])
      print(len(finalClose), "close values:", finalClose[len(finalClose)-1], "...", finalClose[0])

      print("\nConverting list of final dates to datetime\n")
      self.finalDatesAndClose2 = StockData.datetimeDates(self)
      #print(self.finalDatesAndClose2[0][0])

    else:
      print("No sources have data for", self.name)

def main(): # For testing purposes
  stockName = 'spy'
  stock1 = StockData(stockName)
  print("Finding available dates and close values for", stock1.name)
  StockData.main(stock1)

if __name__ == "__main__":
  main()
