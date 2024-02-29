
from .keys import *

sentences = {

    k_oscillators : {

        k_glue : {
            k_style_basic :   [ ' + ', ' & '] ,
            k_style_succint : [ ' + ', ' plus ',' and ' , ' & '] ,
            k_style_concise : [ ' + ', ' plus ',' and ', ' with ' , ' , '] ,
            k_style_detailed: [ ' + ', ' plus ',' and ', ' with '] ,
            k_style_specification: [ '\n' ],
        } ,

        k_compositing : {
            k_style_basic : {
                k_oscs_singular : [
                     "{oscillators_desc}" ,
                     ]  ,
                k_oscs_plural : [ 
                    "{oscillators_desc}" ,
                    ] ,
                k_oscs_mix_forward : [
                    "{oscillators_mix}  {oscillators_desc}",
                ]                             
            },
            k_style_succint : {
                k_oscs_singular : [ 
                    "{oscillators_desc}",
                ] ,
                k_oscs_plural : [
                    "{oscillators_desc}",
                ] ,
                k_oscs_mix_balanced : [
                    "An equal mix of {oscillators_desc}" ,
                    "The sum of {oscillators_desc}" ,
                    "An equal blend of {oscillators_desc}" ,
                    "An equal mixture of {oscillators_desc}" ,
                    "An equal dose of  {oscillators_desc}",
                    "An equal dosage of  {oscillators_desc}",
                ],
                k_oscs_mix_forward : [
                    "A {oscillators_mix} mix of {oscillators_desc}" ,
                    "A {oscillators_mix} melange of {oscillators_desc}" ,
                    "{oscillators_mix}  {oscillators_desc}",
                ]                             
            },
            k_style_concise : {
                k_oscs_singular : [ 
                    "{oscillators_desc}",
                ] ,
                k_oscs_plural : [
                    "A mix of {oscillators_desc}" ,
                    "The sum of {oscillators_desc}" ,
                    "A blend of {oscillators_desc}" ,
                    "A mixture of {oscillators_desc}" ,
                    "Mix {oscillators_desc}" ,
                    "The combination of {oscillators_desc}",
                    "Combination of {oscillators_desc}" ,
                    "Sound with {oscillators_desc}" ,
                    "Preset with {oscillators_desc}" ,
                ] ,
                k_oscs_mix_balanced : [
                    "An equal mix of {oscillators_desc}" ,
                    "The sum of {oscillators_desc}" ,
                    "An equal blend of {oscillators_desc}" ,
                    "An equal mixture of {oscillators_desc}" ,
                    "An equal dose of  {oscillators_desc}",
                    "An equal dosage of  {oscillators_desc}",
                ],
                k_oscs_mix_forward : [
                    "A {oscillators_mix} mix of {oscillators_desc}" ,
                    "A {oscillators_mix} melange of {oscillators_desc}" ,
                    "{oscillators_mix}  {oscillators_desc}",
                ]
            },
            k_style_detailed: {
                k_oscs_singular : [
                    "{oscillators_desc}",
                ],
                k_oscs_plural : [
                    "A mix of {oscillators_desc}" ,
                    "The mix of {oscillators_desc}" ,
                    "The sum of {oscillators_desc}" ,
                    "A blend of {oscillators_desc}" ,
                    "A mixture of {oscillators_desc}" ,
                    "Mix of {oscillators_desc}" ,
                    "A melange of {oscillators_desc}" ,
                    "The combination of {oscillators_desc}",
                    "Combination of {oscillators_desc}" ,
                    "Sound mixing {oscillators_desc}" ,
                    "Preset with {oscillators_desc}" ,
                ] ,
                k_oscs_mix_balanced : [
                    "An equal mix of {oscillators_desc}" ,
                    "The sum of {oscillators_desc}" ,
                    "An equal blend of {oscillators_desc}" ,
                    "An equal mixture of {oscillators_desc}" ,
                    "An equal combo of {oscillators_desc}" ,
                ] ,
                k_oscs_mix_forward : [
                    "A {oscillators_mix} mix of {oscillators_desc}" ,
                    "A {oscillators_mix} melange of {oscillators_desc}" ,
                ]
            },
            k_style_specification: {
                k_oscs_singular : [
                    "Oscillators:\n{oscillators_desc}",
                ],
                k_oscs_plural : [
                    "Oscillators:\n{oscillators_desc}",
                ]
            }
        }
    },

    k_oscillator : {

        k_glue : {
            k_style_basic :   [ '+', '|' , '/'] ,
            k_style_succint : [ '+', '|' , '/'] ,
            k_style_concise : [ ' and ' ] ,
            k_style_detailed: [ ' and ', ' plus ' , ' blended with '] ,
            k_style_specification: [ '/' ],
        } ,

        k_compositing : {
            k_style_basic : {
                k_osc_singular : [ 
                    "{shapes_desc}",
                ] ,
                k_osc_plural : [
                    "{shapes_desc}",
                ] ,    
                k_osc_vol_singular : [
                    "{shapes_desc}@{volume_desc}" ,
                ] ,
                k_osc_vol_plural : [
                    "{shapes_desc}@{volume_desc}" ,
                ]
            },
            k_style_succint : {
                k_osc_singular : [ 
                    "{shapes_desc}",
                ] ,
                k_osc_plural : [
                    "{shapes_desc}",
                ] ,    
                k_osc_vol_singular : [
                    "{shapes_desc} at {volume_desc}" ,
                ] ,                           
                k_osc_vol_plural : [
                    "{shapes_desc} at {volume_desc}" ,
                ]                              
            },
            k_style_concise : {
                k_osc_singular : [ 
                    "{shapes_desc} {osc_type}",
                ] ,
                k_osc_plural : [
                    "{osc_article} {osc_type} of {shapes_desc}",
                    "{osc_article} {osc_type} of {shapes_desc}",
                ] ,
                k_osc_vol_singular : [
                    "{shapes_desc} {osc_type} at {volume_desc}",
                ] ,                            
                k_osc_vol_plural : [
                    "{osc_article} {osc_type} of {shapes_desc} at {volume_desc}",
                    "{osc_article} {osc_type} of {shapes_desc} at level {volume_desc}",
                ]                            
            },
            k_style_detailed: {
                k_osc_singular : [
                    "{shapes_desc} {osc_type}",
                ],
                k_osc_plural : [
                    "{osc_article} {osc_type} using a combination of {shapes_desc}",
                ] ,
                k_osc_vol_singular : [
                    "{shapes_desc} {osc_type} at level {volume_desc}",
                ] ,                            
                k_osc_vol_plural : [
                    "{osc_article} {osc_type} using a combination of {shapes_desc} at level {volume_desc}",
                ]                                
            },
            k_style_specification: {
                k_osc_singular : [
                    "- {shapes_desc} oscillator",
                ],
                k_osc_plural : [
                    "- {shapes_desc} oscillator",
                ] ,
                k_osc_vol_singular : [
                    "- {shapes_desc} @ {volume_desc}" ,
                ] ,                            
                k_osc_vol_plural : [
                    "- {shapes_desc} @ {volume_desc}" ,
                ]                               
            }
        } ,
        k_osc_type : {
            k_osc_sub : [
                "sub-oscillator",
            ] ,
            k_osc_sub_not : [
                "oscillator",
            ]
        } ,
        k_osc_article : {
            k_osc_sub : [
               "a" ,
            ] ,
            k_osc_sub_not : [
                "an",
            ]
        }
    } ,

    k_shape : {

        k_compositing : {
            k_style_basic : {
                k_shape_no_vol : [ 
                    "{waveform_name}",
                ] ,
                # lets never show the volume in BASIC mode
                k_shape_w_vol : [
                    "{waveform_name}" ,
                ] ,
            },
            k_style_succint : {
                k_shape_no_vol : [ 
                    "{waveform_name}",
                ] ,
                k_shape_w_vol : [
                    "{waveform_name}({volume_desc})" ,
                ] ,
                         
            },
            k_style_concise : {
                k_shape_no_vol : [ 
                    "{waveform_name}",
                ] ,
                k_shape_w_vol : [
                    "{waveform_name}({volume_desc})" ,
                ] ,
            },
            k_style_detailed: {
                k_shape_no_vol : [ 
                    "a {waveform_name}",
                ] ,
                k_shape_w_vol : [
                    "a {waveform_name}({volume_desc})" ,
                ] ,                          
            },
            k_style_specification: {
                k_shape_no_vol : [ 
                    "{waveform_name}",
                ] ,
                k_shape_w_vol : [
                    "{waveform_name}@{volume_desc}" ,
                ] ,                                                     
            }
        }
    }    
}


words = {

    k_wave_sine : "Sine",
    k_wave_triangle : "Triangle",
    k_wave_trishaped : "Triangle-Shape",
    k_wave_square : "Square",
    k_wave_pulse : "Pulse",
    k_wave_pulse_thin : "ThinPulse",
    k_wave_sawtooth : "SawTooth",
    k_wave_sawmulti : "MultiSaw",
    k_wave_sawup : "SawUp",
    k_wave_sawdown : "SawDown",
    k_wave_noise : "Noise",
    k_wave_noise_white : "White Noise",
    k_wave_noise_pink : "Pink Noise",
    k_wave_sample : "Sample",
    k_wave_additive : "Additive",
    k_wave_digital : "Digital",
    k_wave_feedback : "Feedback",
    k_wave_exotic : "Exotic",
    k_wave_s_h : "S/H",
    k_wave_other : "Generic"

}
