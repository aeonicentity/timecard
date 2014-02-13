### GUI for timecard
from common import Settings
from UserTimeCard import UserTimeCard

import kivy
import xmlrpclib


from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.listview import ListView
from kivy.uix.textinput import TextInput
from kivy.lang import Builder

Builder.load_string('''
<TCUElem_Project>
	canvas.before:
		BorderImage:
			border:2,2,2,2
			source: 'border.png'
			pos: self.pos
			size: self.size
''')

s = xmlrpclib.ServerProxy('http://localhost:8000/RPC2')

class TCUElem_Project(GridLayout):
	def startTimer(self,e):
		print "Starting Timer"
		return
	def endTimer(self,e):
		print "Ending Timer"
		return
	def leaveProject(self,e):
		print "Leaving Project"
		return
	def __init__(self,projId):
		self.cols=1
		
		super(TCUElem_Project,self).__init__()
		leaveBtn = Button(text="Leave Project")
		leaveBtn.bind(on_press=self.leaveProject)
		self.add_widget(leaveBtn)
		self.add_widget(Label(text="[color=000000]Project[/color]", markup=True))
		self.add_widget(Label(text="[color=000000]Hour[/color]", markup=True))
		self.add_widget(Label(text="[color=000000]00:00[/color]", markup=True))
		startBtn = Button(text="Start Timer")
		startBtn.bind(on_press = self.startTimer)
		self.add_widget(startBtn)
		endBtn = Button(text="Stop Timer")
		endBtn.bind(on_press = self.endTimer)
		self.add_widget(endBtn)
		return
		
class TCUElem_TimeField(GridLayout):
	def onEntry(self,e):
		### TODO: Once unfocused, send this data to the UserTimeCard object ###
		return
	def __init__(self):
		super(TCUElem_TimeField,self).__init__()
		self.cols=2
		self.add_widget(Label(text="In"))
		self.add_widget(Label(text="Out"))
		for i in range(10):
			self.add_widget(TextInput(text="", size_hint_y=None, height=30))
		#self.add_widget(layout)
		return

class TimeCardUiProject(ScrollView):
	def joinProject(self,e):
		print "Joining Project "+self.txt_ProjectName.text
		### TODO: search the projects for a project named projectname.text
		job = s.searchJob('admin', Settings.users['admin'], self.txt_ProjectName.text)
		if not job:
			print "job not found"
			return
		# if project not found, throw an error message to user. Offer to make the Project.
		# join the project in the database
		projId = s.joinUsertoJob('admin',Settings.users['admin'],self.TimeCard.userData['id'],job[0])
		# create the project tile from database data.
		projTile = TCUElem_Project(projId)
			# add tile to UI.
		return
	def __init__(self,TimeCard):
		self.TimeCard = TimeCard
		super(TimeCardUiProject,self).__init__()
		self.size_hint = (None,None)
		#self.size = (145,400)
		self.pos_hint={'center_x':.5, 'center_y':.5}
		btn_joinProject = Button(text="Join Project", size_hint_y=None, height=30)
		btn_joinProject.bind(on_press=self.joinProject)
		self.txt_ProjectName = TextInput(size_hint_y=None, height=30)
		layout = GridLayout(cols=1)
		layout.add_widget(self.txt_ProjectName)
		layout.add_widget(btn_joinProject)
		layout.bind(minimum_height=layout.setter('height'))
		for i in range(0,4):
			### TODO: search for projects which you're already a part of, and add them.
			#layout.add_widget(TCUElem_Project(None))
			pass
		
		self.add_widget(layout)
		return
		
class TimeCardUiCard(GridLayout):
	def clockIn(self,e):
		print "Clock In"
		return
	def clockOut(self,e):
		print "Clock Out"
		return
	def saveAndQuit(self,e):
		print "Quitting"
		TimeCardApp.stop()
		return
	def __init__(self,TimeCard):
		self.TimeCard = TimeCard
		self.cols=1
		super(TimeCardUiCard, self).__init__()
		name = self.TimeCard.userData['FirstName'] + " " + self.TimeCard.userData['LastName']
		self.add_widget(Label(text="Hello "+name))
		self.add_widget(Label(text="Select A Day", size_hint_y=None, height=30))
		self.add_widget(Label(text="Select Department", size_hint_y=None, height=30))
		self.add_widget(TCUElem_TimeField())
		btn_ClockIn =Button(text="Clock In Now",size_hint_y=None, height=30)
		btn_ClockOut=Button(text="Clock Out Now",size_hint_y=None, height=30)
		btn_Save = Button(text="Save and Close",size_hint_y=None, height=30)
		
		btn_ClockIn.bind(on_press=self.clockIn)
		btn_ClockOut.bind(on_press=self.clockOut)
		btn_Save.bind(on_press=self.saveAndQuit)
		
		self.add_widget(btn_ClockIn)
		self.add_widget(btn_ClockOut)
		self.add_widget(btn_Save)
		return
	

class TimeCardUiTimeCard(GridLayout):
	def login(self,e):
		final = 6734
		print "Logging In"
		### TODO: search database by like final four ###
			# select first result.
			# create UserTimeCard Object based on result
			# switchs screens
		result = s.searchUsers('admin', Settings.users['admin'], [('SSN','like',final)])
		uId = result[0]
		self.TimeCard = UserTimeCard(uId)
		print result
		self.switchScreens('TimeCard')
		return
		
	def screen_TimeCard(self):
		self.cols = 2

		project_column = TimeCardUiProject(self.TimeCard)
		card_column = TimeCardUiCard(self.TimeCard)
		self.add_widget(Label(text="Projects", size_hint_x=None, width=150,size_hint_y=None, height=30))
		self.add_widget(Label(text="Time Card",size_hint_y=None,height=30))
		self.add_widget(project_column)
		self.add_widget(card_column)
		return
	def screen_Login(self):
		self.cols=1
		self.add_widget(Label(text="Login with 4 Digit Code:"))
		self.add_widget(TextInput())
		btn_Login = Button(text="Login")
		btn_Login.bind(on_press=self.login)
		self.add_widget(btn_Login)
		return
	def switchScreens(self,arg):
		screens = {
			'TimeCard':self.screen_TimeCard,
			'Login':self.screen_Login
			}
		self.clear_widgets()
		screens[arg]()
		return
	def __init__(self,**kwargs):
		super(TimeCardUiTimeCard, self).__init__(**kwargs)
		self.screen_Login()
		return

class TimeCardApp(App):
	def build(self):
		return TimeCardUiTimeCard()

if __name__=='__main__':
	app = TimeCardApp().run()
