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
python src/manage.py initwords
# run the server
# IT IS ESSENTIAL to run the server without threading NOR reload if you want to use the IMAGE CAPTURE feature
python src/manage.py runserver --nothreading --noreload
```

You can now use the labeller at http://localhost:8000

# Notes on pedalboard + JUCE

If you want to point to pedalboard that is at the same level of your telemann project, use requirements-dev.txt
This will import the files from the local pedalboard project (cf. its build instructions in BUILD.md) aka ../pedalboard

If you just want to get going, use requirements.txt and this will import the pedalboard_benbenz from pypi.

The pedalboard_benbenz repository is a modified repository to expose different functions like program name, as well as a capture function.
Moreover, some changes have been made to the underlying JUCE library to fix a bug with the parameters names of the audio units being conflicted when the audio unit uses clumps. 

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


The parameters in the fixtures match the following preset organization, which basically consist in copying all presets in MIDI Pograms and flattening+splitting them (keeping the main presets at the root of MIDI Programs):

```
/Library/Audio/Presets/u-he/Diva/MIDI Programs/1 BASS
/Library/Audio/Presets/u-he/Diva/MIDI Programs/2 LEAD
/Library/Audio/Presets/u-he/Diva/MIDI Programs/3 POLY SYNTH
/Library/Audio/Presets/u-he/Diva/MIDI Programs/4 DREAM SYNTH
/Library/Audio/Presets/u-he/Diva/MIDI Programs/5 PERCUSSIVE
/Library/Audio/Presets/u-he/Diva/MIDI Programs/6 RHYTHMIC
/Library/Audio/Presets/u-he/Diva/MIDI Programs/7 EFFECTS
/Library/Audio/Presets/u-he/Diva/MIDI Programs/8 TEMPLATES
/Library/Audio/Presets/u-he/Diva/MIDI Programs/Basari
/Library/Audio/Presets/u-he/Diva/MIDI Programs/Bigtone eco bank
/Library/Audio/Presets/u-he/Diva/MIDI Programs/BrontoScorpio
/Library/Audio/Presets/u-he/Diva/MIDI Programs/Fernando's hardware factory - A
/Library/Audio/Presets/u-he/Diva/MIDI Programs/Fernando's hardware factory - B
/Library/Audio/Presets/u-he/Diva/MIDI Programs/Ingo Weidner
/Library/Audio/Presets/u-he/Diva/MIDI Programs/MCnoone
/Library/Audio/Presets/u-he/Diva/MIDI Programs/Mr Wobble
/Library/Audio/Presets/u-he/Diva/MIDI Programs/Sjoerd van Geffen
/Library/Audio/Presets/u-he/Diva/MIDI Programs/Tasmodia
/Library/Audio/Presets/u-he/Diva/MIDI Programs/TREASURE TROVE! - A
/Library/Audio/Presets/u-he/Diva/MIDI Programs/TREASURE TROVE! - B
/Library/Audio/Presets/u-he/Diva/MIDI Programs/TREASURE TROVE! - C
/Library/Audio/Presets/u-he/Diva/MIDI Programs/BS Deep Space Diva.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/BS THXish.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/BT dotted afterhour 01 (mw).h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/BT flex butter seq (mw+vel).h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/BT juno hoovered bass (mw).h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/BT the master himself (at+mw+pb).h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/HS Albert Hall Mini.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/HS All Processors.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/HS Bass Nine.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/HS Canterbury Creeper.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/HS Chango Clique.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/HS Chili Paste duo.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/HS Divanity.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/HS Duduwap 1.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/HS Fatima poly.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/HS Gammond.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/HS Hail Bob 1.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/HS High StraDIVAri.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/HS House Dust.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/HS I cant believe its not analogue.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/HS Kit 1 acoustic.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/HS Kit 2 electro.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/HS Kromosaur.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/HS Lounge Dust.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/HS Model K12.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/HS Modular Bells.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/HS Protocol.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/HS Sparkle.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/HS Strumpet.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/HS Switched On Voicing.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/HS Sync Hangar.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/HS Trans-Uranian Express.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/HS Vulcan Pigs.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/IW BP Strings Ensemble 1.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/IW Jump Brass.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/IW Jupiter High Strings.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/IW Mini Detuned Saw Lead.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/IW Poly6 Strings.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/JA WashingMachine.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/JS Bud Pluck.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/MK Bass In Tube.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/MK Bass Pack Leader.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/MK Brass Straight Up.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/MK FX Scaled Resonance.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/MK FX Wind.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/MK Joy.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/MK Pattern Grammaphone.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/MK Pattern Metal Works.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/MK Planet Earth.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/MK Strings Short PWM.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/MK Syncopat.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/MM Choir In The Clouds.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/PAK Karinanthon EP.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/PG FilterConToUrs.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/ROY EXPERIMENTAL God Particle.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/ROY FX Cold December.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/ROY FX Rewinding the Tape.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/ROY Old Recipe.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/SG Chica Go.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/SG Crackpipe Organ.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/SG Miss Duality.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/SG Practicing Paganini.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/SG Rotterdam.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/SG Stra Diva Rius.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/SG What The Pluck.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/SM Schnarrer.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/SW Bonk.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/SW Magic Flute.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/TUC Bubbler.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/TUC Knock It!.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/TUC Single Cell Worm.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/XH MONO (fx) Alien Biosymmetry.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/XS Analog Clavinova.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/XS Analog E. Piano.h2p
/Library/Audio/Presets/u-he/Diva/MIDI Programs/XS Juno Hoover.h2p
```

## SynthMaster

Check SynthMaster [user manual](http://www.kv331audio.com/synthmaster/downloads/synthmasterusermanual.pdf) page 19.

SynthMaster supports MIDI Bank Change and MIDI Program Change messages. Especially during live
performances, changing presets using MIDI messages is a real necessity.
To be able to use program change messages, you should assign presets to a MIDI bank first. To do that,
follow these steps:
1. Filter the presets you’d like to add to the MIDI bank. For instance, the screenshot on the right shows Brass Factory Presets.
2. Move mouse over the Presets list and right click. From the context menu, choose “Assign presets to MIDI bank” sub menu and then choose an empty bank.


The parameters in the sources.json fixture match when each category is matched to a MIDI bank (in order of appearance in the browser).
Bank0. Bass
Bank1. Bowed Strings
Bank2. Brass
etc. 



