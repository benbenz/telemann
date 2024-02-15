# Introduction

Telemann (after Georg Philipp Telemann) is an audio dataset generator. 

__Warning__ : this is intended for local use only. No attention has been put to security issues. Especially as it is running remotely plugins libraries (without a secured protocol), one should be very careful about exposing the server to the external world.

# Setup

```
nix-shell
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt 
```