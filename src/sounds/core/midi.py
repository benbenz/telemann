import mido
from mido import Message
from ..models import SoundSource
import math
from .defs import MIDIInterface , MIDIPattern , MIDIRange

def get_midi_output_ports():
    devices = mido.get_output_names()
    result = list()
    result.extend([
        (-2,MIDIInterface.NONE),
        (-1,MIDIInterface.INTERNAL)
    ])
    for idx,device in enumerate(devices):
        result.append(
            (idx,device)
        )
    return result 

def get_midi_input_ports():
    devices = mido.get_input_names()
    result = list()
    result.extend([
        (MIDIInterface.NONE,MIDIInterface.NONE),
        (MIDIInterface.INTERNAL,MIDIInterface.INTERNAL)
    ])
    for device in devices:
        result.append(
            (device,device)
        )
    return result 


def get_midi_pattern(source:SoundSource,pattern:MIDIPattern,preset_offset=0.5):
    velocity = source.midi_velocity_pref if source.midi_velocity_pref is not None else 100

    length = 10
    notes = [Message("note_on",
                        velocity=velocity,
                        note=60,
                        time=preset_offset),
            Message("note_off", velocity=velocity,note=60, time=length+preset_offset)]    

    if pattern == MIDIPattern.SUSTAINED_MIDDLE_C:
        pass # default pattern
    elif pattern == MIDIPattern.SUSTAINED_LOW_C:
        notes = [Message("note_on",
                        velocity=velocity,
                        note=36,
                        time=preset_offset),
            Message("note_off", velocity=velocity,note=60, time=length+preset_offset)]    
    elif pattern == MIDIPattern.SUSTAINED_HIGH_C:
        notes = [Message("note_on",
                        velocity=velocity,
                        note=84,
                        time=preset_offset),
            Message("note_off", velocity=velocity,note=60, time=length+preset_offset)]    
    elif pattern == MIDIPattern.ARPEGGIATED:
        length = 20
        num_notes = 20 
        notes = []
        time_inc = length / num_notes
        note_range = [0,127]
        notes_values = [ note_range[0]+ math.floor( (note_range[1]-note_range[0])/num_notes*i) for i in range(num_notes)]
        for i in range(num_notes):
            notes.extend([ Message("note_on",
                            velocity=velocity,
                            note=notes_values[i],
                            time=time_inc*i+preset_offset),
                        Message("note_off", velocity=velocity,note=notes_values[i], time=time_inc*i+1+preset_offset)])     

    elif pattern == MIDIPattern.ARPEGGIATED_FAST:
        length = 20
        num_notes = 60
        notes = []
        time_inc = length / num_notes
        note_range = [0,127]
        notes_values = [ note_range[0]+ math.floor( (note_range[1]-note_range[0])/num_notes*i) for i in range(num_notes)]
        for i in range(num_notes):
            notes.extend([ Message("note_on",
                            velocity=velocity,
                            note=notes_values[i],
                            time=time_inc*i+preset_offset),
                        Message("note_off", velocity=velocity,note=notes_values[i], time=time_inc*i+1+preset_offset)])    

    elif pattern == MIDIPattern.ARPEGGIATED_SUPER_FAST:
        length = 20
        num_notes = 100
        notes = []
        time_inc = length / num_notes
        note_range = [0,127]
        notes_values = [ note_range[0]+ math.floor( (note_range[1]-note_range[0])/num_notes*i) for i in range(num_notes)]
        for i in range(num_notes):
            notes.extend([ Message("note_on",
                            velocity=velocity,
                            note=notes_values[i],
                            time=time_inc*i+preset_offset),
                        Message("note_off", velocity=velocity,note=notes_values[i], time=time_inc*i+1+preset_offset)])                                 

    return notes , length



def parse_new_program_value(source:SoundSource,bank_msb:int,bank_lsb:int|None,program:int):
    if source.parameters and source.parameters.get('midi') and source.parameters.get('midi').get('num_programs'):
        num_programs = source.parameters.get('midi').get('num_programs')
    else:
        if source.midi_bank_num is not None:
            num_programs = [128] * source.midi_bank_num
        else:
            num_programs = [128] * 128
    
    num_bank_programs = num_programs[bank_msb]
    
    # increment
    if program>=num_bank_programs:
        program_offset = program - num_bank_programs
        while program_offset >= 0:
            program = program_offset
            bank_msb += 1
            bank_msb = bank_msb % source.midi_bank_num
            num_bank_programs = num_programs[bank_msb]
            program_offset = program - num_bank_programs
        
        # we know, the new bank_msb and the target program value
        # we just have to write it in terms of LSB/program values now    
        if source.midi_bank_use_lsb:
            bank_lsb = math.floor( (program - program%128)/128 )
            program = program % 128
        else:
            program = program % 128
    # decrement
    elif program<0:
        program_offset = program 
        while program_offset < 0:
            program = program_offset
            bank_msb -= 1
            bank_msb = bank_msb % source.midi_bank_num
            num_bank_programs = num_programs[bank_msb]
            program_offset = program + num_bank_programs
        
        program = program_offset
        
        # we know, the new bank_msb and the target program value
        # we just have to write it in terms of LSB/program values now    
        if source.midi_bank_use_lsb:
            bank_lsb = math.floor( (program - program%128)/128 )
            program = program % 128
        else:
            program = program % 128        
    else:
        if source.midi_bank_use_lsb:
            bank_lsb = math.floor( (program - program%128)/128 )
            program = program % 128
        else:
            program = program % 128

    return bank_msb , bank_lsb , program


def get_midi_program_key(bank_msb,bank_lsb,program):
    return f"{bank_msb}:{bank_lsb}:{program}"