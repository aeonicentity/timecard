#functions for timecard. These functions should be included at the head
#of any python function which needs them.
import datetime
import pytz
import pickle

class Settings:
	users = {
		'admin':'123456',
	}
	timezone = "MST"
	timeformat = '%m-%d-%Y %H:%M:%S '
	# monday 0, sunday 6
	startDay = 0
	days = [
		'Monday',
		'Tuesday',
		'Wednesday',
		'Thursday',
		'Friday',
		'Saturday',
		'Sunday',
	]
	writeSettings(self):
		with open("settings.dat","w") as f:
			f.write(pickle.dumps(users))
			f.write(pickle.dumps(timezone))
			f.write(pickle.dumps(timeformat))
			f.write(pickle.dumps(startDay))
			f.write(pickle.dumps(days))
		return

class Function:
	@staticmethod
	def getPeriodStart(yr,day):
		# this function will return tupple of  all the days of day N 
		# (see python Datetime) within given year.
		StartTupple = []
		for i in range(1,13):
			for j in range (1,32):
				try:
					d = datetime.date(yr,i,j)
				except ValueError, e:
					break
				if d.weekday() == day:
					StartTupple.append( d )
				
		return StartTupple
	@staticmethod	
	def parseToUnix(date):
		print date
		#return datetime.time()
		return None
	@staticmethod
	def getTime():
		u = datetime.datetime.utcnow()
		u = u.replace(tzinfo = pytz.utc)
		return datetime.datetime.astimezone(u,pytz.timezone(Settings.timezone)).strftime(Settings.timeformat)
	@staticmethod
	def getYear():
		u = datetime.datetime.utcnow()
		u = u.replace(tzinfo = pytz.utc)
		return int( datetime.datetime.astimezone(u,pytz.timezone(Settings.timezone)).strftime("%Y") )
	@staticmethod
	def parseTime(t):
		return datetime.datetime.strptime(t,Settings.timeformat)
		
