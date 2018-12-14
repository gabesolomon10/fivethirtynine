import requests
import urllib
from bs4 import BeautifulSoup
import csv
import datetime
import time

# TRENDOGATE BEAUTIFUL SOUP

# Open/Create a file to append Twitter data
csvFile = open('trending_tweets4.csv', 'a')
#Use csv Writer
csvWriter = csv.writer(csvFile)

# set the base URL
base_url = 'https://trendogate.com/placebydate/23424977/'

# set the start date
start = datetime.datetime.strptime("2017-07-06", "%Y-%m-%d")
# set the end date
end = datetime.datetime.strptime("2018-11-05", "%Y-%m-%d")

# find the date range
date_range = [start + datetime.timedelta(days=x) for x in range(0, (end-start).days)]

# iterate through dates
for date in date_range:
	current_date = str(date.strftime("%Y-%m-%d"))

	final_url = base_url + current_date

	# open the page
	page = urllib.request.urlopen(final_url)

	# create the soup!
	soup = BeautifulSoup(page, 'html.parser')

	name_box = soup.find('ul', attrs={'class': 'list-group'})
	name_box = str(name_box)
	name_box = list(name_box.split('<li class="list-group-item">'))

	for i in name_box:
		if i[:2] == '<a':
			i = i[i.index('>') + 2:i.index('</a>')]
			csvWriter.writerow([current_date, i])

	print('date completed: ', current_date)

	# wait for 2 seconds so we don't overload the servers
	time.sleep(2)