from common import Function
from common import Settings

import xmlrpclib
import pickle
import datetime

s = xmlrpclib.ServerProxy('http://localhost:8000/RPC2')

class ClockDay:
	### This is pretty much a list with awesome powers.
	Times = []
	def save(self):
		return pickle.dumps(self.Times)
	def load(self,pickleTimes):
		#print "printing pickle times"
		#print str( pickleTimes )
		try:
			self.Times = pickle.loads( str( pickleTimes ) )
		except EOFError:
			self.Times = []
	def clockNow(self):
		self.Times.append(Function.getTime())
	def clock(self,time):
		self.Times.append(time)
	def __init__(self,times):
		self.load(times)
		return

class UserTimeCard:
	userData={}
	cardData = [] #a list of All the card data found in the time cards.
	
	def checkFinalFour(self,given):
		### Validates the Final Four of the SSN and returns True or False
		check = self.userData['SSN'][-4:]
		if  check == str(given):
			return True
		return False
	
	def clockNow(period,day):
		### Wrapper for ClockDay.clockNow()
		cardData[period][day].clockNow()
		
	def clock(period,day,time):
		### Wrapper for ClockDay.clock()
		cardData[period][day].cock(time)
		
	def initializeFromDB(self,userid):
		### Get all existing time card data and store it in an array.
		self.cardData = s.searchCards('admin',Settings.users['admin'],userid)
		### Check the date. If the latest card is out of date make cards until the latest card is up to date.
		currentDate = datetime.datetime.now()
		periods = Function.getPeriodStart( Function.getYear(), Settings.startDay )
		### itterate over periods
		for period in periods:
			if period.month < currentDate.month or (period.day <= currentDate.day and period.month == currentDate.month):
				if not self.checkCard(period): #see if period is already in cardData
					data = {
						'StartDate':period.strftime(Settings.timeformat) 
					}
					s.createTimeCard('admin',Settings.users['admin'],userid,data)
					self.cardData = s.searchCards('admin',Settings.users['admin'],userid)
	
		### unpack data
		for day in Settings.days:
			for data in self.cardData:
				data[day] = ClockDay(data[day])
		return
		
	def __init__(self,userid):
		self.userData = s.getUserData('admin',Settings.users['admin'],userid)
		###TODO: Remove this with GUI
		#final = raw_input("Enter Final Four of SSN: ")
		#if self.checkFinalFour(final):# This is what you need to change.
		self.initializeFromDB(userid)
		self.commit()
			
	def checkCard(self,period):
		for card in self.cardData:
			timeData = Function.parseTime(card['StartDate'])
			if timeData.day == period.day and timeData.month == period.month:
				return True
		return False
		
	def commit(self):
		### TODO: pickle data ###
		for day in Settings.days:
			for data in self.cardData:
				data[day] = data[day].save()
		### TODO: Commit all data to database. ###
		s.updateUser('admin', Settings.users['admin'], self.userData['id'], self.userData)
		for card in self.cardData:
			s.updateTimeCard('admin',Settings.users['admin'],card['id'],card)
		return
