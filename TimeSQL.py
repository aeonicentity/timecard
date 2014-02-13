from SQLiteAdapter import SQL
from common import Settings

class TimeSQL(SQL):
	def initializeDB(self):
		userTableValues = (
							'id',
							'FirstName',
							'MiddleName',
							'LastName',
							'SSN',
							'Email',
							'Age',
							'Wage',
							'PTO',
							'SickLeave',
							'DefaultDeptId',
							)
		query = """
				CREATE TABLE IF NOT EXISTS users(
											%s integer PRIMARY KEY AUTOINCREMENT,
											%s varchar(80),
											%s varchar(80),
											%s varchar(80),
											%s varchar(12),
											%s varchar(100),
											%s integer,
											%s float,
											%s float,
											%s float,
											%s integer
											);""" % userTableValues
		self.c.execute(query)
		
		timecardTableValues = (
							'id',
							'UserId',
							Settings.days[0],
							Settings.days[1],
							Settings.days[2],
							Settings.days[3],
							Settings.days[4],
							Settings.days[5],
							Settings.days[6],
							'PTOHours',
							'SickLeave',
							'StartDate',
							)
		query = """
				CREATE TABLE IF NOT EXISTS cards(
											%s integer PRIMARY KEY AUTOINCREMENT,
											%s integer,
											%s blob,
											%s blob,
											%s blob,
											%s blob,
											%s blob,
											%s blob,
											%s blob,
											%s float,
											%s float,
											%s int
											);""" % timecardTableValues
		self.c.execute(query)
		
		jobTableValues = (
						'id',
						'JobName',
						'DepartmentId',
						)
		
		query = """
				CREATE TABLE IF NOT EXISTS jobs(
												%s integer PRIMARY KEY AUTOINCREMENT,
												%s varchar(160),
												%s integer
												);""" % jobTableValues
		
		self.c.execute(query)
		
		jobtrackingTableValues = (
								'id',
								'UserId',
								'JobId',
								'HoursWorked',
								)
		query = """
				CREATE TABLE IF NOT EXISTS jobs_tracking(
												%s integer PRIMARY KEY AUTOINCREMENT,
												%s integer,
												%s integer,
												%s float
												);""" % jobtrackingTableValues
		
		self.c.execute(query)
														
		departmentTableValues = (
								'id',
								'DepartmentName',
								)
		
		query = """
				CREATE TABLE IF NOT EXISTS departments(
												%s integer PRIMARY KEY AUTOINCREMENT,
												%s varchar(160)
												);""" % departmentTableValues
		
		self.c.execute(query)
		
		departmentTrackingValues = (
									'id',
									'DepartmentId',
									'UserId',
									'HoursWorked',
									)
		query = """
				CREATE TABLE IF NOT EXISTS departments_tracking(
												%s integer PRIMARY KEY AUTOINCREMENT,
												%s integer,
												%s integer,
												%s float
												);""" % departmentTrackingValues
		
		self.c.execute(query)
