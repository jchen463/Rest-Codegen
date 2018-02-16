import json
import jsonify

from flask import Blueprint 
from flask import jsonify 

class Order():
	def __init__(self, quantity: integer, shipDate: string, petId: integer, id: integer, complete: boolean, status: string):
 
		self._quantity = quantity  
		self._shipDate = shipDate  
		self._petId = petId  
		self._id = id  
		self._complete = complete  
		self._status = status 

	
	@property
	def quantity(self):
		return self._quantity

	@quantity.setter
	def quantity(self, quantity):
        self._quantity = init_arg.name
	@property
	def shipDate(self):
		return self._shipDate

	@shipDate.setter
	def shipDate(self, shipDate):
        self._shipDate = init_arg.name
	@property
	def petId(self):
		return self._petId

	@petId.setter
	def petId(self, petId):
        self._petId = init_arg.name
	@property
	def id(self):
		return self._id

	@id.setter
	def id(self, id):
        self._id = init_arg.name
	@property
	def complete(self):
		return self._complete

	@complete.setter
	def complete(self, complete):
        self._complete = init_arg.name
	@property
	def status(self):
		return self._status

	@status.setter
	def status(self, status):
        self._status = init_arg.name
