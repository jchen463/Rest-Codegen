import pytest, os, sys

@pytest.fixture(scope="module")
def genServerFiles():

    #specify custom build file here
    build_file = ''
    
    try:
        os.system('codegen ' + build_file)
    except:
        assert 0
      
