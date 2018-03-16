import pytest
import os
import sys


@pytest.fixture(scope="module")
def serverFiles():
    return server_gen('flask-server-generated')

@pytest.fixture(scope="module")
def clientFiles():
    return client_gen('myproject', 'build.py', 'swagger.yaml')
     

class server_gen():
    
    def __init__(self, project_name, build, spec):
        self.name = project_name
        self.build_file = build
        self.yaml_file = spec
        assert os.path.split(os.getcwd())[1] == 'tests'
        assert os.system('codegen ' + build) == 0
    
    def __del__(self):
        assert os.system('rm -rf ' + self.name)
        
        
class client_gen():
    
    def __init__(self, project_name, build, spec):
        self.name = project_name
        self.build_file = build
        self.yaml_file = spec

        assert os.system('cp specs/' + spec + ' ' + build + ' myproject/src') == 0
        try:
            os.chdir('myproject/src')
        except:
            assert 0
        assert os.system('codegen ' + 'builds/' + build) == 0
        try:
            os.chdir('../..')
        except:
            assert 0
            
    def __del__(self):
        assert os.system('rm -rf ' + self.name)

