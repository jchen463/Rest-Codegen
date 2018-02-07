import yaml
import sys
from openapi_spec_validator import validate_spec
from openapi_spec_validator import openapi_v3_spec_validator

with open("petstore.yaml", 'r') as stream:
    try:
        json = yaml.load(stream)
        #print(json)
    except yaml.YAMLError as exc:
        print(exc)
        sys.exit("error")

#validate_spec(json)
errors_iterator = openapi_v3_spec_validator.iter_errors(json)
#print(type(errors_iterator))

#l = [_ for _ in errors_iterator]
#if l:
	#print(len(l))
#else:
	#print("no errors")