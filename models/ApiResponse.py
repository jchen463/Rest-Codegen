import json
import jsonify

from flask import Blueprint 
from flask import jsonify 

class ApiResponse():
	def __init__(self, type: string, message: string, code: integer):
 
		self._type = type  
		self._message = message  
		self._code = code 

	
	@property
	def type(self):
		return self._type

	@type.setter
	def type(self, type):
        self._type = init_arg.name
	@property
	def message(self):
		return self._message

	@message.setter
	def message(self, message):
        self._message = init_arg.name
	@property
	def code(self):
		return self._code

	@code.setter
	def code(self, code):
        self._code = init_arg.name
