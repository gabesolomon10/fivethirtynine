import requests
import urllib
from bs4 import BeautifulSoup
import csv
import datetime
import time

# TRENDOGATE BEAUTIFUL SOUP

# Open/Create a file to append Twitter data
csvFile = open('nyt_headlines2.csv', 'a')
#Use csv Writer
csvWriter = csv.writer(csvFile)

# set the base URL
base_url = 'https://www.nytimes.com/issue/todayspaper/'

# set the start date
start = datetime.datetime.strptime("2018/05/22", '%Y/%m/%d')


# set the end date
end = datetime.datetime.strptime("2018/11/05", '%Y/%m/%d')

# find the date range
date_range = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

# iterate through dates
for date in date_range:
	current_date = str(date.strftime('%Y/%m/%d'))

	final_url = base_url + current_date + '/todays-new-york-times'

	# open the page
	page = urllib.request.urlopen(final_url)

	# create the soup!
	soup = BeautifulSoup(page, 'html.parser')

	# find all headers
	headers = soup.find_all('h2', attrs={'class': 'css-l2vidh e4e4i5l1'})

	# find corresponding sub-headers
	sub_headers = soup.find_all('p', attrs={'class': 'css-1gh531 e4e4i5l4'})

	i = 0

	for i in range(len(headers)):
		csvWriter.writerow([current_date, headers[i].text, sub_headers[i].text])

	print('done with date:', current_date)

	# wait for 2 seconds so we don't overload the servers
	time.sleep(2)