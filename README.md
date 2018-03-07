

# Codegen (name tbd)

# Virtual Environment Setup
### Linux Users:
1. `sudo pip3 install virtualenv`
2. Create virtual environment: 
`virtualenv venv`
- Activate virtual environment: 
`source venv/bin/activate`
- Deactivate virtual environment:
`deactivate`
# Installation:
1. Clone this project (Rest-Codegen)
2. Activate virtualenv
3. Two options to install: 
	- Using setup.py:
		- `cd Rest-Codegen`
		- `python3 setup.py develop`
	- Using pip3:
		- `pip3 install Rest-Codegen/`
- Uninstall:
	- `pip3 uninstall rest-codegen`
# Usage:
1. Create a python build file and a yaml OpenAPI 3.0 specification (sample can be found in the repo under `samples/`)
2. `codegen [buildfile.py]`  if no build file exists, Rest-Codegen will look for a specification named **swagger.yaml** in the current working directory. By default, generated code will appear in a folder named **generated** in the current working directory
3. To start server: 
	- `cd generated`
	- `pip3 install -r requirements.txt`
	- `python3 -m generated`
