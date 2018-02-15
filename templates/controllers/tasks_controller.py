import json
import jsonify

from flask import Blueprint 
from flask import jsonify 

@tasks_api.route('/todo/api/v1.0/tasks', methods['GET'])
def get_tasks (task_id):
	return jsonify({'task': task[0].serialize()})

@tasks_api.route('/todo/api/v1.0/tasks', methods['POST'])
def create_task ():
	return jsonify({'task': task})

