# Rest-Codegen

These files are meant to be pip installed

Go to the directory that contains this codegen project (dir/codegen/codegen) be in dir

make sure virtualenv is on or else you'll do global install (source codegen-env/bin/activate)

first time:  sudo pip install codegen/ 
other times: sudo pip install codegen/ --upgrade
sudo pip install codegen/ again will not update it if it's already been installed
(at least it didn't for me)

verify installation: pip freeze
uninstall: sudo pip uninstall codegen
