
from .keys import *

sentences = {

    k_oscillators : {

        k_glue : {
            k_basic :   [ ' + ', ' plus '] ,
            k_succint : [ ' + ', ' plus ',' and '] ,
            k_concise : [ ' + ', ' plus ',' and ', ' with '] ,
            k_detailed: [ ' + ', ' plus ',' and ', ' with ']
        } ,

        k_compositing : {
            k_basic : {
                k_singular : [
                     "{oscillators_desc}" 
                     ]  ,
                k_plural : [ 
                    "{oscillators_desc}" 
                    ]                 
            },
            k_succint : {
                k_singular : [ 
                    "{oscillators_desc}"
                ] ,
                k_plural : [
                    "{oscillators_desc}"
                ] ,
                k_balanced_mix : [
                    "An equal mix of {oscillators_desc}" ,
                    "The sum of {oscillators_desc}" ,
                    "An equal blend of {oscillators_desc}" ,
                    "An equal mixture of {oscillators_desc}" ,
                    "An equal dose of  {oscillators_desc}",
                    "An equal dosage of  {oscillators_desc}",
                ],
                k_forward_mix : [
                    "A {oscillators_mix} mix of {oscillators_desc}" ,
                    "A {oscillators_mix} melange of {oscillators_desc}" ,
                    "{oscillators_mix}  {oscillators_desc}",
                ]                             
            },
            k_concise : {
                k_singular : [ 
                    "{oscillators_desc}"
                ] ,
                k_plural : [
                    "A mix of {oscillators_desc}" ,
                    "The sum of {oscillators_desc}" ,
                    "A blend of {oscillators_desc}" ,
                    "A mixture of {oscillators_desc}" ,
                    "Mix {oscillators_desc}" ,
                    "A combination of {oscillators_desc}",
                    "Combination of {oscillators_desc}" ,
                    "Sound with {oscillators_desc}" ,
                    "Preset with {oscillators_desc}" 
                ] ,
                k_balanced_mix : [
                    "An equal mix of {oscillators_desc}" ,
                    "The sum of {oscillators_desc}" ,
                    "An equal blend of {oscillators_desc}" ,
                    "An equal mixture of {oscillators_desc}" ,
                    "An equal dose of  {oscillators_desc}",
                    "An equal dosage of  {oscillators_desc}",
                ],
                k_forward_mix : [
                    "A {oscillators_mix} mix of {oscillators_desc}" ,
                    "A {oscillators_mix} melange of {oscillators_desc}" ,
                    "{oscillators_mix}  {oscillators_desc}",
                ]
            },
            k_detailed: {
                k_singular : [
                    "{oscillators_desc}"
                ],
                k_plural : [
                    "A mix of {oscillators_desc}" ,
                    "The mix of {oscillators_desc}" ,
                    "The sum of {oscillators_desc}" ,
                    "A blend of {oscillators_desc}" ,
                    "A mixture of {oscillators_desc}" ,
                    "Mix of {oscillators_desc}" ,
                    "A melange of {oscillators_desc}" ,
                    "A combination of {oscillators_desc}",
                    "Combination of {oscillators_desc}" ,
                    "Sound mixing {oscillators_desc}" ,
                    "Preset with {oscillators_desc}" 
                ] ,
                k_balanced_mix : [
                    "An equal mix of {oscillators_desc}" ,
                    "The sum of {oscillators_desc}" ,
                    "An equal blend of {oscillators_desc}" ,
                    "An equal mixture of {oscillators_desc}" ,
                    "An equal combo of {oscillators_desc}" ,
                ]
            }
        }
    }
}
