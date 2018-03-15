import pytest
import os
import sys


@pytest.fixture(scope="module")
def serverFiles():
 
    assert os.path.split(os.getcwd())[1] == 'tests'

    # specify custom build file here
    build_file = ''

    assert os.system('codegen ' + build_file) == 0

    return project('flask-server-generated')


@pytest.fixture(scope="module")
def clientFiles():

    # specify custom build file here
    build_file = 'build.py'
    yaml_file = 'swagger.yaml'

    assert os.system('cp specs/' + yaml_file + ' ' + build_file + ' myproject/src') == 0
    try:
        os.chdir('myproject/src')
    except:
        assert 0
    assert os.system('codegen ' + 'builds/' + build_file) == 0
    try:
        os.chdir('../..')
    except:
        assert 0

    return project('myproject')
     



class project():
    
    def __init__(self, root_dir):
        self.root_dir = root_dir
    
    def __del__(self):
        assert os.system('rm -rf ' + self.root_dir)
      

