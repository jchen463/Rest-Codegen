import json
import jsonify

from flask import Blueprint 
from flask import jsonify 

class Category():
	def __init__(self, name: string, id: integer):
 
		self._name = name  
		self._id = id 

	
	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, name):
        self._name = init_arg.name
	@property
	def id(self):
		return self._id

	@id.setter
	def id(self, id):
        self._id = init_arg.name
