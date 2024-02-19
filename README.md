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
python src/manage.py initsources
# run the server
# note the '--nothreading' option - this is to avoid locks with pedalboard (to be debugged)
python src/manage.py runserver --nothreading
```

You can now use the labeller at http://localhost:8000

# Setup plugins for MIDI Program Change

__IMPORTANT NOTE__: There could be a bug with VST3 and program changes (cf. [here][(https://forum.ableton.com/viewtopic.php?t=247288]) even if it applies to Ableton, I've noticed this also occured with telemann ...). 

## Diva

Check Diva [user guide](https://u-he.com/downloads/manuals/plugins/diva/Diva-user-guide.pdf) page 11.


The ‘Local’ folder
Diva’s factory presets are sorted into folders 1 to 8. We recommend that you do not add or remove
any Local presets, but save all your creations and third party soundsets in ‘User’ (see below).
MIDI Programs
‘Local’ also contains a special folder called ‘MIDI Programs’ which is normally empty. When the first
instance of Diva starts, up to 128 presets from that folder are loaded into memory, to be selected
via MIDI Program Change messages. As they are accessed in alphabetical order it makes sense
to prefix each name with an index: ‘000 rest-of-name’ to ‘127 rest-of-name’.
But that’s not all: the ‘MIDI Programs’ folder can contain up to 127 sub-folders, switched via MIDI
Bank Select messages (CC#0). Send Bank Select first, then Program Change. ‘MIDI Programs’ is
bank 0, sub-folders are addressed in alphabetical order starting with bank 1.
IMPORTANT: Changes to the MIDI Programs folder are only updated after the host application is
restarted: files cannot be added, removed or renamed on the fly!
When Diva receives a program change, it will display the bank and program numbers to the left of
the preset name e.g. “0:0” for the first preset in the first bank. In certain hosts e.g. Ableton Live,
however, the first bank / preset is designated “1” instead of the correct “0”.
To avoid another possible source of confusion, make sure that there are no junked presets in the
MIDI Programs folder. All files there are indexed, whether they are visible or not"


## SynthMaster

Check SynthMaster [user manual](http://www.kv331audio.com/synthmaster/downloads/synthmasterusermanual.pdf) page 19.

SynthMaster supports MIDI Bank Change and MIDI Program Change messages. Especially during live
performances, changing presets using MIDI messages is a real necessity.
To be able to use program change messages, you should assign presets to a MIDI bank first. To do that,
follow these steps:
1. Filter the presets you’d like to add to the MIDI bank. For instance, the screenshot on the right shows Brass Factory Presets.
2. Move mouse over the Presets list and right click. From the context menu, choose “Assign presets to MIDI bank” sub menu and then choose an empty bank.



