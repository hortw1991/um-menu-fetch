#!usr/bin/env

"""
Fetches a simple text menu for the day.  Currently only supports today's menu.

Cmd Line Arguments:
	None (or invalid): returns lunch if time < 4:30pm otherwise dinner
	Hours: returns a list of all hours
	Lunch: returns lunch menu
	Dinner: returns dinner menu
	Breakfast: returns breakfast menu
"""

import requests
import time
import sys
from bs4 import BeautifulSoup


def format_url(flag=None):
	"""
	Returns a formatted URL for lunch or dinner with current date.
	"""

	# Var order: meal, month, day, date, year
	#    Lunch: 1683
	#    Dinner: 1685
	#    Months and days do NOT have a leading 0
	#    Year is all 4 digits
	url = "https://memphis.campusdish.com/LocationsAndMenus/TigerDenFoodCourt/TigerDen?locationId=7029&storeId=&mode=Daily&periodId={}&date={}%2F{}%2F{}"

	month = time.strftime('%m')
	day = time.strftime('%d')
	year = str(time.strftime('%Y'))
	lunch = '1683'
	dinner = '1685'

	# Remove leading 0s
	if month.startswith('0'):
		month = month.strip('0')
	if day.startswith('0'):
		day = day.strip('0')

	# Set lunch or dinner flag
	cur_time = int(time.strftime('%H'))

	# Check for lunch override
	if flag == 'lunch':
		meal = lunch
	elif flag == 'dinner':
		meal = dinner
	elif flag == 'breakfast':  # hidden option
		meal = '1681'
	elif cur_time < 1630:
		meal = lunch
	else:
		meal = dinner

	return url.format(meal, month, day, year)


def get_request(url):
	""" Returns response session or error code. """
	r = requests.get(url)

	if r.status_code != 200:
		return False
	else:
		return r


def parse_contents(content):
	b = BeautifulSoup(content, 'html.parser')
	c = b.find_all('a', {'class': 'viewItem'})

	return [item.text for item in c]


def print_menu(food):
	""" Prints general and daily info. """
	for item in food: print(item)


def display_hours():
	""" Displays information about location and hours of all fooderies. """
	with open('tiger_den_hours.txt', 'r') as hours:
		for line in hours: print(line.strip())

def main():
	"""
	Checks for any optional arg and displays that requested info
	"""
	flag = ''

	try:
		if sys.argv[1].lower() == 'hours':
			display_hours()
			quit()
		elif sys.argv[1].lower() == 'lunch':
			flag = 'lunch'
		elif sys.argv[1].lower() == 'dinner':
			flag = 'dinner'
		elif sys.argv[1].lower() == 'breakfast':
			flag = 'breakfast'
		
	except IndexError:
		flag = None

	url = format_url(flag)
	r = get_request(url)
	if not r:
		raise ConnectionError

	print_menu(parse_contents(r.content))




if __name__ == "__main__":
	main()

