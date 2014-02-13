#program wide imports
from common import Function
from common import Settings

from SimpleXMLRPCServer import SimpleXMLRPCServer 
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler # Restrict to a particular path. 
from TimeSQL import TimeSQL
import pickle
import time



def authorize(user,password):
	if user in Settings.users:
		if Settings.users[user] == password:
			return True
	return False

class RPCLayer():
	### USER RELATED QUERIES ###
	def createUser(self,usr,pwd,userData):
		if not authorize(usr,pwd): return False
		### TODO: automatically attach him to a department_tracking if department is set.
		newId = self.sql.insert('users',userData)
		
		if newId:
			if 'DefaultDeptId' in userData:
				self.joinUsertoDept(usr,pwd,newId,userData['DefaultDeptId'])
			return newId
		else: return False
	def getUserData(self,usr,pwd,userId):
		if not authorize(usr,pwd): return False
		
		return self.sql.select('users',userId)
	
	def searchUsers(self,usr,pwd,args):
		if not authorize(usr,pwd): return False
		
		return self.sql.search('users',args)
		
	def updateUser(self,usr,pwd,userId,userData):
		if not authorize(usr,pwd): return False
		
		args = [('id','=',userId)]
		return self.sql.update('users',userData,args)	
		
	def deleteUser(self,usr,pwd,userId):
		if not authorize(usr,pwd): return False
		
		### clear his data out of departments_tracking
		if not self.sql.delete('departments_tracking',[('UserId','=',userId)]): 
			return False
		### clear his data out of jobs_tracking
		if not self.sql.delete('jobs_tracking',[('UserId','=',userId)]): 
			return False
		### clear his data out of cards
		if not self.sql.delete('cards',[('UserId','=',userId)]): 
			return False
		
		return self.sql.delete('users',[('id','=',userId)])

	def printAllUsers(self):
		for row in self.sql.selectAll('users'):
			print row
		return True
	### TIMECARD RELATED QUERIES ###	
	def createTimeCard(self,usr,pwd,cardUserId,cardData):
		if not authorize(usr,pwd): return False
		
		cardData['UserId'] = str(cardUserId)
		return self.sql.insert('cards',cardData)
		
	def updateTimeCard(self,usr,pwd,cardId,cardData):
		if not authorize(usr,pwd): return False
		
		args = [('id','=',cardId)]
		return self.sql.update('cards',cardData,args)	
		
	def getCardData(self,usr,pwd,cardId):
		if not authorize(usr,pwd): return False
		
		return self.sql.select('cards',cardId)
	
	def searchCards(self,usr,pwd,userId):
		if not authorize(usr,pwd): return False
		cards = []
		#get IDs.
		ids = self.sql.search('cards',[('UserId','=',str(userId))])
		
		for i in ids:
			cards.append( self.sql.select('cards',i) )
		return cards
	### JOB ASSIGNMENT AND TRACKING QUERIES ###
	def createJob(self,usr,pwd,jobData):
		if not authorize(usr,pwd): return False
		
		return self.sql.insert('jobs',jobData)
	
	def searchJob(self,usr,pwd,jobName):
		if not authorize(usr,pwd): return False
		print jobName
		return self.sql.search('jobs',[('JobName','like',jobName)])
	
	def searchDuplicateJobs(self,usr,pwd,jobId,userId):
		if not authorize(usr,pwd): return False
		return 
	
	def joinUsertoJob(self,usr,pwd,userId,JobId):
		if not authorize(usr,pwd): return False
		### TODO: prevent multiple joining on a job, by searching for existing job entries for this user on that job. ###
		data = {'UserId':userId,'JobId':JobId,'HoursWorked':0}
		return self.sql.insert('Jobs_Tracking',data)
	
	def removeUserfromJob(self,usr,pwd,userId,jobId):
		if not authorize(usr,pwd): return False
		
		args = [('JobId','=',jobId),('UserId','=',userId)]
		return self.sql.delete('jobs_tracking',args)
	
	def deleteJob(self,usr,pwd,jobId):
		if not authorize(usr,pwd):return False
		args = [('id','=',jobId)]
		
		### delete all job_trackings attached to job.
		
		tracks = self.sql.search('jobs_tracking',[('JobId','=',jobId)])
		for track in tracks:
			self.sql.delete('jobs_tracking',[('id','=',track)])
		
		return self.sql.delete('jobs',args)
	
	### DEPARTMENT, AND TRACKING QUERIES ###
	def createDepartment(self,usr,pwd,deptData):
		if not authorize(usr,pwd): return False
		
		return self.sql.insert('departments',deptData)
	
	def joinUsertoDept(self,usr,pwd,userId,deptId):
		if not authorize(usr,pwd): return False
		
		data = {'DepartmentId':deptId,'UserId':userId,'HoursWorked':0,}
		return self.sql.insert('departments_tracking',data)
	
	def updateDept(self,usr,pwd,deptId,data):
		if not authorize(usr,pwd): return False
		
		args= [('id','=',deptId)]
		return self.sql.update('departments',data,args)
		
	def deleteDept(self,usr,pwd,deptId):
		
		if not authorize(usr,pwd): return False
		### you can only delete departments to which no users are assigned..
		res = self.sql.search('users',[('DefaultDeptId','=',deptId)])
		if not res:
			# Delete department
			self.sql.delete('departments',[('id','=',deptId)])
			# scrub the database of any tracking associated with this department.
			tracks = self.sql.search('departments_tracking',[('DepartmentId','=',deptId)])
			for track in tracks:
				self.sql.delete('departments_tracking',[('id','=',track)])
			return True
		### Else, throw an error and pout.
		return False
			


	def __init__(self):
		self.sql = TimeSQL()
		return

class RequestHandler(SimpleXMLRPCRequestHandler): 
    rpc_paths = ('/RPC2',) # Create server 

server = SimpleXMLRPCServer(("localhost", 8000), requestHandler=RequestHandler) 

server.register_instance(RPCLayer()) # Run the server's main loop 
server.serve_forever()
