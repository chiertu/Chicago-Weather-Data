import csv
import urllib2
import sys

#set this to a really big number to reach all days between now and Jan 1 1948
top_of_range = 13

all_data = []

header_info = ["TimeCST","TemperatureF","Dew PointF","Humidity","Sea Level PressureIn","VisibilityMPH","Wind Direction","Wind SpeedMPH","Gust SpeedMPH","PrecipitationIn","Events","Conditions","WindDirDegrees","DateUTC"]

for item in range(1, top_of_range):
	downloaded_data  = urllib2.urlopen('http://www.wunderground.com/history/airport/KMDW/1948/1/' + str(item) + '/DailyHistory.html?req_city=Chicago&req_state=IL&req_statename=Illinois&reqdb.zip=60290&reqdb.magic=1&reqdb.wmo=99999&format=1')
	csv_data = list(csv.reader(downloaded_data))
	#removes blank rows
	if(csv_data[0] == []):
		del csv_data[0]
	#removes extra headers from each file
	if(csv_data[0][0] == "TimeCST"):
		del csv_data[0]
	all_data.extend(csv_data)
	#this will end it automatically once the top bound is reached
	#24271 represents the number of days from Jan 1 1948 to Jan 1 2014
	#checking for greater than 24271 ensures that if a date in history has no data, it won't be skipped
	if(all_data[-1][0] == "No daily or hourly history data available<br />" and item > 24271):
		sys.stdout.write("You've reached the end!")
		break
	#todo: remove header and blank row from the top of each page
	percent = float(item) / top_of_range
	sys.stdout.write("\rDone with day: {0} {1}%".format(item, round((percent) * 100, 2)))
	sys.stdout.flush()

all_data.insert(0, header_info)

print("\nthe total number of rows is {}.".format(len(all_data)))

with open("chicago_weather_data.csv", "w+") as f:
    writer = csv.writer(f)
    writer.writerows(all_data)
