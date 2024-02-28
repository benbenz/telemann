# TODOs

Tasks to do ...

### Todo

- [ ] https://github.com/bensonruan/Speech-Command 
- [ ] https://github.com/bensonruan/Chrome-Web-Speech-API
- [ ] Locks when skipping: disable the thRender timeout: the rendering will block after few skips ...
      The thRender doesnt solve the issue. It just avoids it in usual use cases where the user is skipping reltively fast
- [ ] Analysis:
  - [ ] Envelope: turn arpegiator off and render audio >> envelope analysis
  - [ ] Preset/OSC+Fitler+Amp:
     - [ ] OSC  >> rule by looking at parameters
     - [ ] FILT >> rule by looking at parameters 
     - [ ] ENV  >> rule by looking at parameters 

- [ ] Issue with Collapsing "model" in Diva: not the case in the VST plugin: Problem with AU parameters parsing ? in pedalboard or JUCE ?
- [ ] Use Diva.vst if not resolved
- [ ] Issue with VST Preset Name being offset with SynthMaster ... (not Diva VST ...) No idea why
- [ ] This one should be moved to the Sound bite so that we can randomize across soundbites during génération time 
- [x] compare landing program for prev,next,current,capture and analyze
- [x] more robust landing program comparison with header
- [x] fetching objects with program data + payload

- [ ] Generation:
  - [ ] Randomize decription tech for each soundbite
  - [ ] save note(s) played separately

- [ ] At generation, use sometimes paraphrasing with ChatGPT (for the technical and human description)

### In Progress 🕑

- [x] Implement PedalBoard VST (v1) handling: https://forum.juce.com/t/midi-program-change-forwarding-for-vst3/47161
      Issue with VST3 and program changes all over the place ...


- [ ] Pydantic:
  - [ ] use custom validation for range 0.0....0.1
  - [ ] use native json() serialization 
  - [ ] add abstract .desc() as well
  - [ ] Use des( style_guide :StyleGuideEnum )
  - [ ] Use pedantic classes to describe the result of the analysis 
    - SoundtoneDescription
    - SoundtoneOscillators
    - SoundtoneOscillator ....
    - SoundtoneFilters ...
    - OscShape = List[Waveforms]
    - Oscillator = OscShape + sub + pwm
    - And each of those has the following method:
    - .json() = return the json value 
    - .des() = return the description value (randomized)



### Done ✓

