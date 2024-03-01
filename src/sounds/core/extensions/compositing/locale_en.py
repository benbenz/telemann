
from .keys import *

sentences = {

    k_description : {

        k_compositing : {
            k_style_basic :   ["{oscs_desc}"],
            k_style_succint :  ["{oscs_desc}"],
            k_style_concise :  ["{oscs_desc}"],
            k_style_detailed:  ["{oscs_desc}"],
            k_style_specification:  ["Oscillators:\n{oscs_desc}"],
        }
    },

    k_oscillators : {

        k_glue : {
            k_style_basic :   [ ' + ', ' & '] ,
            k_style_succint : [ ', plus ',', and ' ] ,
            k_style_concise : [ ', plus ',', and ', ', with ' ] ,
            k_style_detailed: [ ', plus ',', and ', ', with ' ] ,
            k_style_specification: [ '\n' ],
        } ,

        k_compositing : {
            k_style_basic : {
                k_comp_oscs_singular : [
                     "{oscillators_desc}" ,
                     ]  ,
                k_comp_oscs_plural : [ 
                    "{oscillators_desc}" ,
                    ] ,
                k_comp_oscs_mix_forward : [
                    "{oscillators_mix} {oscillators_desc}",
                ]                             
            },
            k_style_succint : {
                k_comp_oscs_singular : [ 
                    "{oscillators_desc}",
                ] ,
                k_comp_oscs_plural : [
                    "{oscillators_desc}",
                ] ,
                k_comp_oscs_mix_balanced : [
                    "An equal mix of {oscillators_desc}" ,
                    "The sum of {oscillators_desc}" ,
                    "An equal blend of {oscillators_desc}" ,
                    "An equal mixture of {oscillators_desc}" ,
                    "An equal dose of {oscillators_desc}",
                    "An equal dosage of {oscillators_desc}",
                ],
                k_comp_oscs_mix_forward : [
                    "A {oscillators_mix} mix of {oscillators_desc}" ,
                    "A {oscillators_mix} melange of {oscillators_desc}" ,
                    "{oscillators_mix} {oscillators_desc}",
                ]                             
            },
            k_style_concise : {
                k_comp_oscs_singular : [ 
                    "{oscillators_desc}",
                ] ,
                k_comp_oscs_plural : [
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
                k_comp_oscs_mix_balanced : [
                    "An equal mix of {oscillators_desc}" ,
                    "The sum of {oscillators_desc}" ,
                    "An equal blend of {oscillators_desc}" ,
                    "An equal mixture of {oscillators_desc}" ,
                    "An equal dose of {oscillators_desc}",
                    "An equal dosage of {oscillators_desc}",
                ],
                k_comp_oscs_mix_forward : [
                    "A {oscillators_mix} mix of {oscillators_desc}" ,
                    "A {oscillators_mix} melange of {oscillators_desc}" ,
                    "{oscillators_mix} of {oscillators_desc}",
                ]
            },
            k_style_detailed: {
                k_comp_oscs_singular : [
                    "{oscillators_desc}",
                ],
                k_comp_oscs_plural : [
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
                k_comp_oscs_mix_balanced : [
                    "An equal mix of {oscillators_desc}" ,
                    "The sum of {oscillators_desc}" ,
                    "An equal blend of {oscillators_desc}" ,
                    "An equal mixture of {oscillators_desc}" ,
                    "An equal combo of {oscillators_desc}" ,
                ] ,
                k_comp_oscs_mix_forward : [
                    "A {oscillators_mix} mix of {oscillators_desc}" ,
                    "A {oscillators_mix} melange of {oscillators_desc}" ,
                ]
            },
            k_style_specification: {
                k_comp_oscs_singular : [
                    "{oscillators_desc}",
                ],
                k_comp_oscs_plural : [
                    "{oscillators_desc}",
                ]
            }
        }
    },

    k_oscillator : {

        k_glue : {
            k_style_basic :   [ '-', '|' , '/'] ,
            k_style_succint : [ '-', '|' , '/'] ,
            # k_style_concise : [ ' and ' ] ,
            # k_style_detailed: [ ' and ', ' plus ' , ' blended with '] ,
            k_style_concise : [ '-', '|' , '/' ] ,
            k_style_detailed: [ '-', '|' , '/' , ' blended with '] ,
            k_style_specification: [ '/' ],
        } ,
        k_comp_osc_vol_text_post : {
            k_style_basic :   [" @ {volume_text} "] ,
            k_style_succint : [ " at {volume_text}"] ,
            k_style_concise : [ " at {volume_text}"] ,
            k_style_detailed: [ " at {volume_text}"] ,
            k_style_specification: [ " @ {volume_text}" ],
        } ,
        k_comp_osc_vol_text_pre : {
            k_style_basic :   ["{volume_text} "] ,
            k_style_succint : [ "{volume_text} "] ,
            k_style_concise : [ "{volume_text} "] ,
            k_style_detailed: [ "{volume_text} "] ,
            k_style_specification: [ "{volume_text} " ],
        } ,
        k_comp_osc_vol_number: {
            k_style_basic :   ["@{volume_value}"] ,
            k_style_succint : [ " at {volume_value}"] ,
            k_style_concise : [ " at {volume_value}" ,  " at vol. {volume_value}"] ,
            k_style_detailed: [ " at {volume_value}" ,  " at level {volume_value}" ,  " at volume {volume_value}"] ,
            k_style_specification: [ " @ {volume_value}" ],
        } ,     
        # Constraint: when we have volume_desc_post, we need to always have volume_desc_pre
        k_compositing : {
            k_style_basic : {
                k_comp_osc_singular : [
                    "{volume_desc_pre}{shapes_desc}{volume_desc_post}" ,
                ] ,
                k_comp_osc_plural : [
                    "{volume_desc_pre}{shapes_desc}{volume_desc_post}" ,
                ] ,
            },
            k_style_succint : {
                k_comp_osc_singular : [
                    "{volume_desc_pre}{shapes_desc}{volume_desc_post}" ,
                ] ,                           
                k_comp_osc_plural : [
                    "{volume_desc_pre}{shapes_desc}{volume_desc_post}" ,
                ]                              
            },
            k_style_concise : {
                k_comp_osc_singular : [
                    "{osc_article} {volume_desc_pre}{shapes_desc} {osc_type}{volume_desc_post}",
                    "{volume_desc_pre}{shapes_desc}{volume_desc_post}",
                ] ,                            
                k_comp_osc_plural : [
                    "{osc_article} {volume_desc_pre}{osc_type} of {shapes_desc}{volume_desc_post}",
                    "{volume_desc_pre}{shapes_desc}{volume_desc_post}",
                    "{volume_desc_pre}mix of {shapes_desc}{volume_desc_post}",
                    "{volume_desc_pre}blend of {shapes_desc}{volume_desc_post}",
                ]                            
            },
            k_style_detailed: {
                k_comp_osc_singular : [
                    "{osc_article} {volume_desc_pre}{shapes_desc} {osc_type}{volume_desc_post}",
                ] ,                            
                k_comp_osc_plural : [
                    "{osc_article} {volume_desc_pre}{osc_type} using a combination of {shapes_desc}{volume_desc_post}",
                    "{osc_article} {volume_desc_pre}{osc_type} mixing a {shapes_desc}{volume_desc_post}",
                ]                                
            },
            k_style_specification: {
                k_comp_osc_singular : [
                    "- {osc_article} {volume_desc_pre}{shapes_desc}{volume_desc_post}" ,
                ] ,                            
                k_comp_osc_plural : [
                    "- {osc_article} {volume_desc_pre}{shapes_desc}{volume_desc_post}" ,
                ]                               
            }
        } ,
        k_osc_type : {
            k_comp_osc_sub : [
                "sub-oscillator",
            ] ,
            k_comp_osc_sub_not : [
                "oscillator",
            ]
        } ,
        k_osc_article : {
            k_comp_osc_sub : [
               "a" ,
            ] ,
            k_comp_osc_sub_not : [
                "an",
            ]
        }
    } ,

    k_shape : {
        k_comp_shape_vol: {
            k_style_basic :   [""] ,
            k_style_succint : [ "({volume_value})"] ,
            k_style_concise : [ "({volume_value})" ] ,
            k_style_detailed: [ "({volume_value})"] ,
            k_style_specification: [ " @{volume_value}" ],
        } ,    
        k_compositing : {
            k_style_basic : {
                k_comp_shape_default: ["{waveform_width}{waveform_name}"] ,
            } ,
            k_style_succint : {
                k_comp_shape_default: ["{waveform_width}{waveform_name}{volume_desc}"] ,
            } ,
            k_style_concise : {
                k_comp_shape_default: ["{waveform_width}{waveform_name}{volume_desc}"] ,
            } ,
            k_style_detailed: {
                k_comp_shape_default: ["{waveform_width}{waveform_name}{volume_desc}"] ,
            } ,                          
            k_style_specification: {
                k_comp_shape_default: ["{waveform_width}{waveform_name}{volume_desc}"] ,
            } ,                                                     
        }
    }    
}

cleanup = {
    "(^|\\s+)([aA])(\\s+)([aeiouAEIOU])" : "\\1an\\3\\4",
    "(^|\\s+)([aA]n)(\\s+)([qwrtypsdfghjklzxcvbnmQWRTYPSDFGHJKLZXCVBNM])" : "\\1a\\3\\4" ,
    "[ ]{2,}" : " " ,
}

words = {

    k_wave_sine : ["sine" , "sine-wave"],
    k_wave_triangle : ["triangle" , "triangle-wave"],
    k_wave_trishaped : ["trishape","trishape-wave"],
    k_wave_square : ["square","square-wave"],
    k_wave_pulse : ["pulse","pulse-wave"],
    k_wave_pulse_thin : "thin-pulse",
    k_wave_sawtooth : ["sawtooth","saw","sawtooth-wave"],
    k_wave_sawmulti : "multisaw",
    k_wave_sawup : ["sawup","upward sawtooth"],
    k_wave_sawdown : ["sawdown","downward sawtooth"],
    k_wave_noise : "noise",
    k_wave_noise_white : "white noise",
    k_wave_noise_pink : "pink noise",
    k_wave_sample : "sample",
    k_wave_additive : "additive",
    k_wave_digital : ["digital","digital wave"],
    k_wave_feedback : "feedback",
    k_wave_exotic : "exotic",
    k_wave_s_h : ["s/h","sample & hold"],
    k_wave_other : ["generic","some waveform"] ,

    k_wave_width_narrow : "narrow" ,
    k_wave_width_thin : "thin" ,
    k_wave_width_normal : None ,
    k_wave_width_wide : "wide" ,
    k_wave_width_very_wide : "wide" ,
    k_wave_width_silence : "silenced" ,

    k_volume_grp0 : ["minimum level","minimum volume"],
    k_volume_grp1 : ["really low level","really low volume"],
    k_volume_grp2 : ["low level","low volume"],
    k_volume_grp3 : ["medium level","medium volume"],
    k_volume_grp4 : ["high level","high volume"],
    k_volume_grp5 : ["really high level","really high volume"],
    k_volume_grp6 : ["maximum level","maximum volume"],
}