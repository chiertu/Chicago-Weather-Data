import csv
import urllib2
import sys

#set this to a really big number to reach all days between now and Jan 1 1948
top_of_range = 6150
start_year = 2001

all_data = []

header_info = ["TimeCST","TemperatureF","Dew PointF","Humidity","Sea Level PressureIn","VisibilityMPH","Wind Direction","Wind SpeedMPH","Gust SpeedMPH","PrecipitationIn","Events","Conditions","WindDirDegrees","DateUTC"]

for item in range(1, top_of_range):
	downloaded_data  = urllib2.urlopen('http://www.wunderground.com/history/airport/KMDW/' + str(start_year) + '/1/' + str(item) + '/DailyHistory.html?req_city=Chicago&req_state=IL&req_statename=Illinois&reqdb.zip=60290&reqdb.magic=1&reqdb.wmo=99999&format=1')
	csv_data = list(csv.reader(downloaded_data))

	#removes blank rows
	if(csv_data[0] == []):
		del csv_data[0]
	
	#removes extra headers from each file
	if(csv_data[0][0] == "TimeCST" or csv_data[0][0] == "TimeCDT"):
		del csv_data[0]

	#this will end it automatically once the top bound is reached
	if(csv_data[1][0] == "No daily or hourly history data available<br />" or csv_data[0][0] == "Time"):
		sys.stdout.write("You've reached the end!")
		break

	for line in csv_data:
		for char in '<br/>':
			line[13] = line[13].replace(char, '')
		line[13] = line[13].strip()

	all_data.extend(csv_data)

	#Console progress output
	percent = float(item) / top_of_range
	sys.stdout.write("\rDone with day: {0} {1}%".format(item, round((percent) * 100, 2)))
	sys.stdout.flush()

all_data.insert(0, header_info)

print("\nthe total number of rows is {}.".format(len(all_data)))

with open("chicago_weather_data.csv", "w+") as f:
    writer = csv.writer(f)
    writer.writerows(all_data)
