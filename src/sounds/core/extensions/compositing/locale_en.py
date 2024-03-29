
from .keys import *

sentences = {

    k_description : {

        k_glue : {
            k_style_basic :   ["\n\n"],
            k_style_succint :  ["\n\n"],
            k_style_concise :  ["\n\n"],
            k_style_detailed:  ["\n\n"],
            k_style_specification:  ["\n\n"],
        } ,

        k_compositing : {
            k_style_basic :   ["{architectures_desc}"],
            k_style_succint :  ["{architectures_desc}"],
            k_style_concise :  ["{architectures_desc}"],
            k_style_detailed:  ["{architectures_desc}"],
            k_style_specification:  ["{architectures_desc}"],
        },
    },

    k_architecture_sub : {

        k_comp_archs_singular : {
            k_style_basic :   ["{oscs_desc}"],
            k_style_succint :  ["{oscs_desc}"],
            k_style_concise :  ["{oscs_desc}"],
            k_style_detailed:  ["{oscs_desc}"],
            k_style_specification:  ["Oscillators:\n{oscs_desc}"],
        },
        k_comp_archs_plural : {
            k_style_basic :   ["{architecture_name}{architecture_rank}{oscs_desc}"],
            k_style_succint :  ["{architecture_name}{architecture_rank}{oscs_desc}"],
            k_style_concise :  ["{architecture_name}{architecture_rank}{oscs_desc}"],
            k_style_detailed:  ["{architecture_name}{architecture_rank}{oscs_desc}"],
            k_style_specification:  ["**{architecture_name}{architecture_rank}**:\nOscillators:\n{oscs_desc}"],
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

        k_comp_oscs_mix_balanced : {
            k_style_basic: [ "" ] ,
            k_style_succint: [
                "An equal mix of " ,
                "The sum of " ,
                "An equal blend of " ,
                "An equal mixture of " ,
                "An equal dose of ",
                "An equal dosage of ",
            ] ,
            k_style_concise: [
                "An equal mix of " ,
                "The sum of " ,
                "An equal blend of " ,
                "An equal mixture of " ,
                "An equal dose of ",
                "An equal dosage of ",
            ] ,
            k_style_detailed: [
                "An equal mix of " ,
                "The sum of " ,
                "An equal blend of " ,
                "An equal mixture of " ,
                "An equal combo of " ,
            ],
        } ,

        k_comp_oscs_mix_forward : {
            k_style_basic: ["{oscillators_mix}"] ,
            k_style_succint : [
                "A {oscillators_mix} mix of " ,
                "A {oscillators_mix} melange of " ,
                "{oscillators_mix} ",
            ] ,
            k_style_concise: [
                "A {oscillators_mix} mix of " ,
                "A {oscillators_mix} melange of " ,
                "{oscillators_mix} of ",
            ] ,
            k_style_detailed : [
                "A {oscillators_mix} mix of " ,
                "A {oscillators_mix} melange of " ,
            ],
        } ,

        k_comp_oscs_mix_default : {
            k_style_basic: [ "" ] ,
            k_style_succint : [ "" ] ,
            k_style_concise: [
                "A mix of " ,
                "The sum of " ,
                "A blend of " ,
                "A mixture of " ,
                "Mix " ,
                "The combination of ",
                "Combination of " ,
                "Sound with " ,
                "Preset with " ,                
            ] ,
            k_style_detailed : [
                "A mix of " ,
                "The mix of " ,
                "The sum of " ,
                "A blend of " ,
                "A mixture of " ,
                "Mix of " ,
                "A melange of " ,
                "The combination of ",
                "Combination of " ,
                "Sound mixing " ,
                "Preset with " ,                
            ],
        } ,

        k_comp_oscs_tuning_afterwards : {
            k_style_concise: [
                "Oscillators tuning is as follow: {oscillators_tuning}" ,
                "Oscillators tuning: {oscillators_tuning}" ,
                "Oscillators are tuned as follow: {oscillators_tuning}" ,
                "Oscillators are tuned with {oscillators_tuning}" ,
            ] ,
            k_style_detailed : [
                "Oscillators tuning is as follow: {oscillators_tuning}" ,
                "Oscillators tuning: {oscillators_tuning}" ,
                "Oscillators are tuned as follow: {oscillators_tuning}" ,
                "Oscillators are tuned with {oscillators_tuning}" ,
            ],
        } ,
        k_comp_oscs_tuning_glue : {
            k_style_concise: [
                ", " ,
                " and "
            ] ,
            k_style_detailed : [
                ", " ,
                " and "
            ],
        },    
        k_comp_osc_tuning : {
            k_style_concise: [
                "OSC{osc_i} set {tuning_coarse} {tuning_fine}" ,
            ] ,
            k_style_detailed : [
                "OSC{osc_i} set {tuning_coarse} {tuning_fine}" ,
            ],
        },
        k_compositing : {
            k_style_basic : {
                k_comp_oscs_singular : [
                     "{oscillators_desc}. {oscillators_tuning_desc}" ,
                     ]  ,
                k_comp_oscs_plural : [ 
                    "{oscillators_mix_desc} {oscillators_desc}. {oscillators_tuning_desc}" ,
                    ] ,
            },
            k_style_succint : {
                k_comp_oscs_singular : [ 
                    "{oscillators_desc}. {oscillators_tuning_desc}",
                ] ,
                k_comp_oscs_plural : [
                    "{oscillators_mix_desc} {oscillators_desc}. {oscillators_tuning_desc}",
                ] ,
            },
            k_style_concise : {
                k_comp_oscs_singular : [ 
                    "{oscillators_desc}. {oscillators_tuning_desc}",
                ] ,
                k_comp_oscs_plural : [
                    "{oscillators_mix_desc} {oscillators_desc}. {oscillators_tuning_desc}" ,
                ] ,
            },
            k_style_detailed: {
                k_comp_oscs_singular : [
                    "{oscillators_desc}. ",
                ],
                k_comp_oscs_plural : [
                    "{oscillators_mix_desc} {oscillators_desc}. {oscillators_tuning_desc}" ,
                ] ,
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

    k_operator : {
        k_glue : {
            k_style_basic : {
                k_comp_op_one_operand : [ '' ] ,
                k_comp_op_two_operands : [ ', with '  ] ,
                k_comp_op_two_operands_adj : [ ', {op_type_adj} '  ] ,
                k_comp_op_more_operands : [ ' and '  ] ,
                k_comp_op_feedback : [ ' into '  ] ,
            },
            k_style_succint : {
                k_comp_op_one_operand : [ '' ] ,
                k_comp_op_two_operands : [ ', with '  ] ,
                k_comp_op_two_operands_adj : [ ', {op_type_adj} '  ] ,
                k_comp_op_more_operands : [ ' and '  ] ,
                k_comp_op_feedback : [ ' into '  ] ,
            },
            k_style_concise : {
                k_comp_op_one_operand : [ '' ] ,
                k_comp_op_two_operands : [ ', with '  ] ,
                k_comp_op_two_operands_adj : [ ', {op_type_adj} '  ] ,
                k_comp_op_more_operands : [ ' and '  ] ,
                k_comp_op_feedback : [ ' into '  ] ,
            },
            k_style_detailed: {
                k_comp_op_one_operand : [ '' ] ,
                k_comp_op_two_operands : [ ', with '  ] ,
                k_comp_op_two_operands_adj : [ ', {op_type_adj} '  ] ,
                k_comp_op_more_operands : [ ' and '  ] ,
                k_comp_op_feedback : [ ' into '  ] ,
            },
            k_style_specification: {
                k_comp_op_one_operand : [ '' ] ,
                k_comp_op_two_operands : [ ', with '  ] ,
                k_comp_op_two_operands_adj : [ ', {op_type_adj} '  ] ,
                k_comp_op_more_operands : [ ' and '  ] ,
                k_comp_op_feedback : [ ' into '  ] ,
            },
        } ,
        # Constraint: when we have volume_desc_post, we need to always have volume_desc_pre
        k_compositing : {
            k_style_basic : {
                k_comp_op_one_operand : [
                    "the {operator_type} of {operands_desc}" ,
                ] ,
                k_comp_op_two_operands : [
                    "the {operator_type} of {operands_desc}" ,
                ] ,
                k_comp_op_two_operands_adj : [
                    "{operands_desc}" ,
                ] ,
                k_comp_op_more_operands : [
                    "the {operator_type} of {operands_desc}" ,
                ] ,
                k_comp_op_feedback : [
                    "the {operator_type} of {operands_desc}" ,
                ]
            },
            k_style_succint : {
                k_comp_op_one_operand : [
                    "the {operator_type} of {operands_desc}" ,
                ] ,
                k_comp_op_two_operands : [
                    "the {operator_type} of {operands_desc}" ,
                ] ,
                k_comp_op_two_operands_adj : [
                    "{operands_desc}" ,
                ] ,
                k_comp_op_more_operands : [
                    "the {operator_type} of {operands_desc}" ,
                ] ,
                k_comp_op_feedback : [
                    "the {operator_type} of {operands_desc}" ,
                ] ,
            },
            k_style_concise : {
                k_comp_op_one_operand : [
                    "the {operator_type} of {operands_desc}" ,
                ] ,
                k_comp_op_two_operands : [
                    "the {operator_type} of {operands_desc}" ,
                ] ,
                k_comp_op_two_operands_adj : [
                    "{operands_desc}" ,
                ] ,
                k_comp_op_more_operands : [
                    "the {operator_type} of {operands_desc}" ,
                ] ,
                k_comp_op_feedback : [
                    "the {operator_type} of {operands_desc}" ,
                ] ,                    
            },
            k_style_detailed: {
                k_comp_op_one_operand : [
                    "the {operator_type} of {operands_desc}" ,
                ] ,
                k_comp_op_two_operands : [
                    "the {operator_type} of {operands_desc}" ,
                ] ,
                k_comp_op_two_operands_adj : [
                    "{operands_desc}" ,
                ] ,
                k_comp_op_more_operands : [
                    "the {operator_type} of {operands_desc}" ,
                ] ,
                k_comp_op_feedback : [
                    "the {operator_type} of {operands_desc}" ,
                ] ,                            
            },
            k_style_specification: {
                k_comp_op_one_operand : [
                    "- {operator_type} of {operands_desc}" ,
                ] ,
                k_comp_op_two_operands : [
                    "- {operator_type} of {operands_desc}" ,
                ] ,
                k_comp_op_two_operands_adj : [
                    "- {operands_desc}" ,
                ] ,
                k_comp_op_more_operands : [
                    "- {operator_type} of {operands_desc}" ,
                ] ,
                k_comp_op_feedback : [
                    "- {operator_type} of {operands_desc}" ,
                ] ,                         
            }
        } ,        
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
            k_style_concise : [ " at {volume_value}" ,  " at vol. {volume_value}" , " vol. {volume_value}"] ,
            k_style_detailed: [ " at {volume_value}" ,  " at level {volume_value}" ,  " at volume {volume_value}" , " volume {volume_value}"] ,
            k_style_specification: [ " @ {volume_value}" , " {volume_value}" ],
        } ,     
        k_comp_osc_tuning : {
            k_style_basic: [
                " (tuned {tuning_coarse})" ,
                " tuned {tuning_coarse} " ,
            ] ,
            k_style_succint : [
                " (tuned {tuning_coarse} {tuning_fine})" ,
                " tuned {tuning_coarse} {tuning_fine} " ,
            ],
            k_style_concise: [
                " (tuned {tuning_coarse} {tuning_fine})" ,
                " tuned {tuning_coarse} {tuning_fine} " ,
            ] ,
            k_style_detailed : [
                " (tuned {tuning_coarse} {tuning_fine})" ,
                " tuned {tuning_coarse} {tuning_fine} " ,
            ],
            k_style_specification : [
                " (tuning {tuning_coarse} {tuning_fine})" ,
            ],
        },
        # tuples returned
        k_comp_osc_tuning_pitch : {
            k_style_basic: [
                ("with coarse pitch {tune_coarse}", "fine pitch {tune_fine}"),
            ],
            k_style_succint: [
                ("with coarse pitch {tune_coarse}", "fine pitch {tune_fine}"),
            ],
            k_style_concise: [
                ("with coarse pitch {tune_coarse}", "fine pitch {tune_fine}"),
            ] ,
            k_style_detailed : [
                ("with coarse pitch {tune_coarse}", "fine pitch {tune_fine}"),
            ],
            k_style_specification: [
                ("pitch {tune_coarse}", "fine pitch {tune_fine}"),
            ]
        },
        # tuples returned
        k_comp_osc_tuning_oct : {
            k_style_basic: [
                ("{tune_coarse} oct","{tune_fine} cent"),
                ("{tune_coarse} octave","{tune_fine} cent"),
            ],
            k_style_succint: [
                ("{tune_coarse} oct","{tune_fine} cent"),
                ("{tune_coarse} octave","{tune_fine} cent"),
            ],
            k_style_concise: [
                ("{tune_coarse} oct","{tune_fine} cent"),
                ("{tune_coarse} octave","{tune_fine} cent"),
            ] ,
            k_style_detailed : [
                ("{tune_coarse} oct","{tune_fine} cent"),
                ("{tune_coarse} octave","{tune_fine} cent"),
            ],
            k_style_specification: [
                ("{tune_coarse} oct","{tune_fine} cent"),
                ("{tune_coarse} octave","{tune_fine} cent"),
            ]
        },    
        k_comp_osc_id : {
            k_style_basic: {
                k_comp_osc_singular : [
                    " (OSC{rank})",
                ] ,                           
                k_comp_osc_plural : [
                   " (OSC{rank})",
                ] ,                           
                k_comp_osc_for_operator : [
                   " OSC{rank}",
                ]                              
            },
            k_style_succint: {
                k_comp_osc_singular : [
                    " (OSC{rank})",
                ] ,                           
                k_comp_osc_plural : [
                   " (OSC{rank})",
                ] ,                           
                k_comp_osc_for_operator : [
                   " OSC{rank}",
                ]                              
            },

            k_style_concise: {
                k_comp_osc_singular : [
                    " (OSC{rank})",
                ] ,                           
                k_comp_osc_plural : [
                   " (OSC{rank})",
                ] ,                           
                k_comp_osc_for_operator : [
                   " OSC{rank}",
                ]                              
            },

            k_style_detailed :{
                k_comp_osc_singular : [
                    " (OSC{rank})",
                ] ,                           
                k_comp_osc_plural : [
                   " (OSC{rank})",
                ] ,                           
                k_comp_osc_for_operator : [
                   " OSC{rank}",
                ]                              
            },
            k_style_specification: {
                k_comp_osc_singular : [
                    "OSC{rank}: ",
                ] ,                           
                k_comp_osc_plural : [
                   "OSC{rank}: ",
                ] ,                           
                k_comp_osc_for_operator : [
                   " OSC{rank}",
                ]                              
            }
        },
        # Constraint: when we have volume_desc_post, we need to always have volume_desc_pre
        k_compositing : {
            k_style_basic : {
                k_comp_osc_singular : [
                    "{volume_desc_pre}{shapes_desc}{tuning_desc}{volume_desc_post}{osc_id}" ,
                ] ,
                k_comp_osc_plural : [
                    "{volume_desc_pre}{shapes_desc}{tuning_desc}{volume_desc_post}{osc_id}" ,
                ] ,
                k_comp_osc_for_operator : [
                    "the {shapes_desc} of {osc_id} {tuning_desc}" ,
                ]
            },
            k_style_succint : {
                k_comp_osc_singular : [
                    "{volume_desc_pre}{shapes_desc}{tuning_desc}{volume_desc_post}{osc_id}" ,
                ] ,                           
                k_comp_osc_plural : [
                    "{volume_desc_pre}{shapes_desc}{tuning_desc}{volume_desc_post}{osc_id}" ,
                ] ,                           
                k_comp_osc_for_operator : [
                    "the {shapes_desc} of {osc_id} {tuning_desc}" ,
                ]                              
            },
            k_style_concise : {
                k_comp_osc_singular : [
                    "{osc_article} {volume_desc_pre}{shapes_desc} {osc_type}{tuning_desc}{volume_desc_post}{osc_id}",
                    "{volume_desc_pre}{shapes_desc}{tuning_desc}{volume_desc_post}{osc_id}",
                ] ,                            
                k_comp_osc_plural : [
                    "{osc_article} {volume_desc_pre}{osc_type} of {shapes_desc}{tuning_desc}{volume_desc_post}{osc_id}",
                    "{volume_desc_pre}{shapes_desc}{tuning_desc}{volume_desc_post}{osc_id}",
                    "{volume_desc_pre}mix of {shapes_desc}{tuning_desc}{volume_desc_post}{osc_id}",
                    "{volume_desc_pre}blend of {shapes_desc}{tuning_desc}{volume_desc_post}{osc_id}",
                ],
                k_comp_osc_for_operator : [
                    "the {shapes_desc} of {osc_id} {tuning_desc}" ,
                ]                              
            },
            k_style_detailed: {
                k_comp_osc_singular : [
                    "{osc_article} {volume_desc_pre}{shapes_desc} {osc_type}{tuning_desc}{volume_desc_post}{osc_id}",
                ] ,                            
                k_comp_osc_plural : [
                    "{osc_article} {volume_desc_pre}{osc_type} using a combination of {shapes_desc}{tuning_desc}{volume_desc_post}{osc_id}",
                    "{osc_article} {volume_desc_pre}{osc_type} mixing a {shapes_desc}{tuning_desc}{volume_desc_post}{osc_id}",
                ],
                k_comp_osc_for_operator : [
                    "the {shapes_desc} of {osc_id} {tuning_desc}" ,
                ] ,                            
            },
            k_style_specification: {
                k_comp_osc_singular : [
                    "- {osc_id}{osc_article} {volume_desc_pre}{shapes_desc}{volume_desc_post}{tuning_desc}" ,
                ] ,                            
                k_comp_osc_plural : [
                    "- {osc_id}{osc_article} {volume_desc_pre}{shapes_desc}{volume_desc_post}{tuning_desc}" ,
                ] ,                            
                k_comp_osc_for_operator : [
                    "the {shapes_desc} of {osc_id} {tuning_desc}" ,
                ] ,                            
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
        } ,
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
    }    ,
}

cleanup = {
    "(^|\\s+)([aA])(\\s+)([aeiouAEIOU])" : "\\1an\\3\\4",  # 'a' [Vowel] -> 'an'
    "(^|\\s+)([aA]n)(\\s+)([qwrtypsdfghjklzxcvbnmQWRTYPSDFGHJKLZXCVBNM])" : "\\1a\\3\\4" , # 'an' [Consonant] -> 'a'
    "[ ]{2,}" : " " , # replace multiple spaces with a single one
    "\.\s*\." : "." , # replace successive punctuations '.' with a single one
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
    k_wave_fbk_saw : "feedbacked sawtooth",
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

    k_operation_fm : ["FM modulation"] ,
    k_operation_add : ["addition"] ,
    k_operation_substract : ["substraction"] ,
    k_operation_multiply : ["multiplication"],
    k_operation_ringmod : ["ring-modulation"],
    k_operation_feedback : ["feedback"], 

    k_operation_adj_fm : ["FM-modulated with"] ,
    k_operation_adj_add : ["added to"] ,
    k_operation_adj_substract : ["substracted to"] ,
    k_operation_adj_multiply : ["multiplied by"],
    k_operation_adj_ringmod : ["ring-modulated with"],
    k_operation_adj_feedback : ["feedbacked into"], 
}