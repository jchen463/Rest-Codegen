# Rest-Codegen

These files are meant to be pip installed

Go to the directory that contains this codegen project (dir/codegen/codegen) be in dir

make sure virtualenv is on or else you'll do global install (source codegen-env/bin/activate)

first time:  pip install codegen/ 

other times: pip install codegen/ --upgrade

verify installation: pip freeze

uninstall: pip uninstall codegen

usage:

`$codegen`

runs code generation reading in 'swagger.yaml' from cwd and outputting to cwd

`$codegen user_config.py`

runs code generation reading in config/build file. Uses spec and outputs to directory specified in build file.


