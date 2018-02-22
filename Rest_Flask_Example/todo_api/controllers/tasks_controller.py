from flask import Blueprint

from flask import jsonify  # puts our data into a json object when we reply back
from flask import abort
from flask import make_response
from flask import request

import json

from models.task import Task

tasks_api = Blueprint('tasks_api', __name__)

tasks = [Task(1, u'Buy groceries', u'Milk, Cheese, Pizza, Fruit, Tylenol', False), Task(
    2, u'Learn Python', u'Need to find a good Python tutorial on the web', False)]

tasks1 = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


# the get response is a 200
@tasks_api.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    # print(tasks[0].__repr__())
    # print(tasks.__dict__) list object does not have __dict__
    # r = json.dumps([task.serialize() for task in tasks])
    # loaded_r = json.loads(r)
    # print(loaded_r)
    return jsonify(tasks)


# here we get the id of the task and flask translates it into task_id that we receive
# "return the familiar error code 404, which according to the HTTP specification means Resource Not Found"
# Flask generates the 404 response as HTML instead of a JSON by default
@tasks_api.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task._id == task_id]
    if len(task) == 0:
        print("rip")
        abort(404)
    return jsonify(task)


# Might have to declare a the query parameters like this instead
'''
from flask import request

@app.route('/api/v1/getQ/', methods=['GET'])
def getQ():
    print request.args.get('a')
    print request.args.get('b')
    return "lalala"


'''
# we need to improve our 404 error handler:
# 404 will now return it as a json object


@tasks_api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@tasks_api.route('/todo/api/v1.0/tasks', methods=['POST'])
def create_task():
    if not request.json or 'title' not in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201


@tasks_api.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get(
        'description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})


@tasks_api.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result': True})
