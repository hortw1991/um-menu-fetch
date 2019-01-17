import requests
import time
from bs4 import BeautifulSoup


def format_url():
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

	if cur_time < 1630:
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





def main():
	url = format_url()
	r = get_request(url)
	if not r:
		raise ConnectionError
	
	food = parse_contents(r.content)

	for item in food: print(item)



if __name__ == "__main__":
	main()