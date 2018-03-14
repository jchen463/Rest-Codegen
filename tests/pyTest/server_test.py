import pytest, os, sys
    
def test_files_not_empty(genServerFiles):
    path = os.path.join(os.getcwd(),'flask-server-generated')
    for (path, dirs, files) in os.walk(path):
        for f in files:
            fp = os.path.join(path, f)
            print(fp)
            size = os.path.getsize(fp)
            print(size)
            if f != '__init__.py':
                assert size > 0
    assert 0
    
