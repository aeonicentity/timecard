#script tester
import xmlrpclib
import pickle
import pprint
from common import Function
from common import Settings

from UserTimeCard import UserTimeCard


s = xmlrpclib.ServerProxy('http://localhost:8000/RPC2')

data = {
	'FirstName':'David',
	'MiddleName':'Lee',
	'LastName':'Brilliant',
	'SSN':'614-54-6734',
	'Email':'david.brilliant@novak-adapt.com',
	'Age':'23',
	'Wage':'14.5',
	'PTO':'10.25',
	'SickLeave':'0',
	'DefaultDeptId': '8',
}
lastid = s.createUser('admin','123456',data)
#s.deleteUser('admin','123456',lastid)
print lastid

deptA = {
	'DepartmentName': 'IT'
	}
deptB = {'DepartmentName':'Manufacturing'}
#s.createDepartment('admin','123456',deptA)
#s.createDepartment('admin','123456',deptB)

#print s.deleteDept('admin','123456',8)

#user = UserTimeCard(1)

'''func = Function()

dates = func.getPeriodStart(2014,0) # this will get all mondays in 2014

#print func.parseToUnix(dates[0])
u = func.parseTime(str(func.getTime()))
print u


data = {
	'FirstName':'David',
	'MiddleName':'Lee',
	'LastName':'Brilliant',
	'SSN':'614-54-6734',
	'Email':'david.brilliant@novak-adapt.com',
	'Age':'23',
	'Wage':'14.5',
	'PTO':'10.25',
	'SickLeave':'0',
}
#s.createUser('admin','123456',data)
#s.deleteUser('admin','123456',3)

#args = [('FirstName','=',u'David')]
#print s.searchUsers('admin','123456',args)
#s.printAllUsers()'''


