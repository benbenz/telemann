# Introduction

Telemann (after Georg Philipp Telemann) is an audio dataset generator. 

__Warning__ : this is intended for local use only. No attention has been put to security issues. Especially as it is running remotely plugins libraries (without a secured protocol), one should be very careful about exposing the server to the external world.

# Setup

```
# setup bin environment
nix-shell
# setup python environment
python -m venv .venv
# activte python environment
source .venv/bin/activate
# add modules to python env
pip install -r requirements.txt 
# prepare tailwind/assets
./deploy.sh
# init the database
python src/manage.py migrate
# populate the database
python src/manage.py initgenerators
# run the server
# note the '--nothreading' option - this is to avoid locks with pedalboard (to be debugged)
python src/manage.py runserver --nothreading
```

You can now use the labeller at http://localhost:8000


