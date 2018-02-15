import jinja2
from collections import namedtuple
import os

FileRender = namedtuple('FileRender', ['template', 'output', 'params_dicts'])

controller_lib = {
            'libraries': [
                {'name': 'json'},
                {'name': 'jsonify'}
            ]
        }

controller_dep = {
            'dependencies': [
                {'location': 'flask', 'object': 'Blueprint'}, 
                {'location': 'flask', 'object': 'jsonify'}
            ]
        }
        
controller_func = {  
            'tag': 'tasks_api',
            'api_calls': [
                {'name': 'get_tasks',
                'path': '/todo/api/v1.0/tasks', 'method': 'GET',
                'arguments': ['task_id'], 'json_object': '{\'task\': task[0].serialize()}'
                },
                {'name': 'create_task', 
                'path': '/todo/api/v1.0/tasks', 'method': 'POST',
                'arguments': [], 'json_object': '{\'task\': task}'
                }
            ]
        }

model_lib = {
                'libraries': [
                    {'name': 'json'},
                    {'name': 'jsonify'}
                ]
            }

model_dep = {
                'dependencies': [
                    {'location': 'flask', 'object': 'Blueprint'}, 
                    {'location': 'flask', 'object': 'jsonify'}
                ]
            }

model_class = { 
                'classes': [
                    {
                        'name': 'Task',
                        'arguments': ['JsonSerializable'], 
                        'init_args': [ 
                            {'name': 'id', 'type': 'int'}, 
                            {'name': 'title', 'type': 'str'},
                            {'name': 'description', 'type': 'str'},
                            {'name': 'done', 'type': 'str'}
                        ],
                        'class_methods': [
                            {
                                'name': 'from_dict',
                                'class_method_args': ['cls', 'dikt'],
                                'ret_type': 'Category'
                            }
                        ],
                        'functions': [
                            {
                                'name': 'id',
                                'args': [
                                    {'name': 'id', 'type': 'int'}
                                ],
                                'ret_type': 'int',
                                'ret_val': 'id'
                            },
                            {
                                'name': 'name',
                                'args': [
                                    {'name': 'name', 'type': 'str'}
                                ],
                                'ret_type': 'str',
                                'ret_val': 'name'
                            }
                        ]
                    }
                ]
            }

def do_renders(renders, template_dir, output_dir):

    # Create the Jinja2 environment using custom options and loader, see sections below.
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(''), trim_blocks=True, lstrip_blocks=True, line_comment_prefix='//*')

    for render in renders:

        # Merge the dictionnaries
        params = {}
        for param_dict in render.params_dicts:
            params.update(param_dict)

        # Render the template
        output = env.get_template(render.template).render(**params)

        # Output the file, creating directories if needed.
        output_file = output_dir + os.path.sep + render.output
        directory = os.path.dirname(output_file)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(output_file, 'w') as outfile:
            outfile.write(output)

# Few builtin function are present by default in the templates, add some.

renders = [FileRender('controllers.tmpl', 'tasks_controller.py', [controller_lib, controller_dep, controller_func])]
do_renders(renders, 'templates/', 'controllers')

renders = [FileRender('models.tmpl', 'tasks.py', [model_lib, model_dep, model_class])]
do_renders(renders, 'templates/', 'models')
