import json
import jsonify

from flask import Blueprint 
from flask import jsonify 

class Pet():
	def __init__(self, id: integer, tags: array, name: string, photoUrls: array, status: string):
 
		self._id = id  
		self._tags = tags  
		self._name = name  
		self._photoUrls = photoUrls  
		self._status = status 

	
	@property
	def id(self):
		return self._id

	@id.setter
	def id(self, id):
        self._id = init_arg.name
	@property
	def tags(self):
		return self._tags

	@tags.setter
	def tags(self, tags):
        self._tags = init_arg.name
	@property
	def name(self):
		return self._name

	@name.setter
	def name(self, name):
        self._name = init_arg.name
	@property
	def photoUrls(self):
		return self._photoUrls

	@photoUrls.setter
	def photoUrls(self, photoUrls):
        self._photoUrls = init_arg.name
	@property
	def status(self):
		return self._status

	@status.setter
	def status(self, status):
        self._status = init_arg.name
