

# Codegen (name tbd)

# Virtual Environment Setup
### Linux Users
1. `sudo pip3 install virtualenv`
2. Create virtual environment: 
`virtualenv venv`
- Activate virtual environment: 
`source venv/bin/activate`
- Deactivate virtual environment:
`deactivate`
# Installation
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
# Usage
### Server:
1. Create a python build file and a yaml OpenAPI 3.0 specification (sample can be found in the repo under **SAMPLE/**)
2. `codegen [buildfile.py]`  if no build file exists, Rest-Codegen will look for a specification named **swagger.yaml** in the current working directory. By default, generated code will appear in a folder in the current working directory
3. To start server: 
    - `cd generated-folder`
    - `pip3 install -r requirements.txt`
    - `python3 -m generated-folder`

### Client:
1. Create a new Angular2 project using angular-cli:
`ng new myproject`
2. Specify the language in the build file:
`LANGUAGE = 'typescript'
3. `codegen buildfile.py`
4. Move the generated **services** folder into **myproject/src**
5. Modify **app.component.ts** and **app.module.ts** to include the generated files. An example of these two files modified to work with the petstore example can be found in the repo under **SAMPLE/**
- modify __providers__ in **app.module.ts** to be the same url as the server you are trying to connect to
6. `ng serve` and then go to the url that the client is being served to (ex. http://localhost:4200)
- if also running a server on localhost, you will run into a CORS issue which can be solved using a google chrome extension (https://chrome.google.com/webstore/detail/allow-control-allow-origi/nlfbmbojpeacfghkpbjhddihlkkiljbi?utm_source=chrome-app-launcher-info-dialog)
7. If using our modified angular2 component files, open console (f12) and you should see **getPetById(0)**

