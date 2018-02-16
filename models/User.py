import json
import jsonify

from flask import Blueprint 
from flask import jsonify 

class User():
	def __init__(self, userStatus: integer, username: string, id: integer, phone: string, firstName: string, password: string, lastName: string, email: string):
 
		self._userStatus = userStatus  
		self._username = username  
		self._id = id  
		self._phone = phone  
		self._firstName = firstName  
		self._password = password  
		self._lastName = lastName  
		self._email = email 

	
	@property
	def userStatus(self):
		return self._userStatus

	@userStatus.setter
	def userStatus(self, userStatus):
        self._userStatus = init_arg.name
	@property
	def username(self):
		return self._username

	@username.setter
	def username(self, username):
        self._username = init_arg.name
	@property
	def id(self):
		return self._id

	@id.setter
	def id(self, id):
        self._id = init_arg.name
	@property
	def phone(self):
		return self._phone

	@phone.setter
	def phone(self, phone):
        self._phone = init_arg.name
	@property
	def firstName(self):
		return self._firstName

	@firstName.setter
	def firstName(self, firstName):
        self._firstName = init_arg.name
	@property
	def password(self):
		return self._password

	@password.setter
	def password(self, password):
        self._password = init_arg.name
	@property
	def lastName(self):
		return self._lastName

	@lastName.setter
	def lastName(self, lastName):
        self._lastName = init_arg.name
	@property
	def email(self):
		return self._email

	@email.setter
	def email(self, email):
        self._email = init_arg.name
