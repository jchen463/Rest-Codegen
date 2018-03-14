import pytest, os, sys

@pytest.fixture(scope="module")
def serverFiles():

    #specify custom build file here
    build_file = ''
    
    assert os.system('codegen ' + build_file) == 0
    
    return project_info('flask-server-generated')
        
@pytest.fixture(scope="module")
def clientFiles():

    #specify custom build file here
    build_file = 'build.py'
    
    assert os.system('ng new myproject') == 0
    assert os.system('cp swagger.yaml build.py myproject/src') == 0
    try:
        os.chdir('myproject/src')
    except:
        assert 0
    assert os.system('codegen ' + build_file) == 0
    try:
        os.chdir('../..')
    except:
        assert 0
    
    return project_info('myproject')
    
class project_info():
    def __init__(self, root_dir):
        self.root_dir = root_dir
