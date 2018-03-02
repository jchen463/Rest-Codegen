
import unittest
import sys
sys.path.append("../Rest-Codegen")

from codegen.classes.info import *
from codegen.classes.path_item import *
from codegen.classes.paths import *
from codegen.classes.specification import *

class Test_Specification(unittest.TestCase):
  
  def setUp(self):
    global test_in 
    test_in = {'openapi': '3.0.0', 'info': 
                {'title': 'Pet Store', 'version': '1.0.0'
                },'paths': 
                  {'/pets': 
                    {'get': 
                      {'responses': 
                        {'200': 
                          {'description': 'array of pets'}}}}}}
    testInfo = Info({'title': 'Pet Store','version':'1.0.0'})
    
    testPaths = Paths({'/pets':{'get':{'responses':{'200':{'description':'array of pets'}}}}})
    
    global should_output
    should_output = {'openapi': '3.0.0', 'info': testInfo, 'paths': testPaths, 'servers':None, 'components': None,'security': None, 'tags':None, 'externalDocs': None}

  def test_Specification(self):
    print('spec')
    spc = Specification(test_in)
    out = {}
    out['openapi'] = spc.openapi
    out['info'] = spc.info
    out['servers'] = spc.servers
    out['paths'] = spc.paths
    out['components'] = spc.components
    out['security'] = spc.security
    out['tags'] = spc.tags
    out['externalDocs'] = spc.externalDocs
    self.assertEqual(out, should_output)

if __name__ == '__main__':
  unittest.main()
