from enum import StrEnum , auto
from ..defs import StyleGuide , WaveformEnum , WaveformWidthEnum

# access keys
k_description	= "k_description"
k_architecture_sub	= "k_architecture_sub"
k_oscillators	= "k_oscillators"
k_oscillator	= "k_oscillator"
k_operator	= "k_operator"
k_shape	= "k_shape"
# global keys
k_compositing	= "k_compositing"
k_glue	= "k_glue"
k_osc_type	= "k_osc_type"
k_osc_article	= "k_osc_article"
# compositing keys
k_comp_archs_singular	= "k_comp_archs_singular"
k_comp_archs_plural	= "k_comp_archs_plural"
k_comp_oscs_singular	= "k_comp_oscs_singular"
k_comp_oscs_plural	= "k_comp_oscs_plural"
k_comp_oscs_mix_balanced	= "k_comp_oscs_mix_balanced"
k_comp_oscs_mix_forward	= "k_comp_oscs_mix_forward"
k_comp_oscs_mix_default	= "k_comp_oscs_mix_default"
k_comp_oscs_tuning_glue	= "k_comp_oscs_tuning_glue"
k_comp_oscs_tuning_afterwards	= "k_comp_oscs_tuning_afterwards"
k_comp_osc_singular	= "k_comp_osc_singular"
k_comp_osc_plural	= "k_comp_osc_plural"
k_comp_osc_for_operator = "k_comp_osc_for_operator"
k_comp_osc_vol_text_post	= "k_comp_osc_vol_text_post"
k_comp_osc_vol_text_pre	= "k_comp_osc_vol_text_pre"
k_comp_osc_vol_number	= "k_comp_osc_vol_number"
k_comp_osc_tuning_pitch	= "k_comp_osc_tuning_pitch"
k_comp_osc_tuning_oct	= "k_comp_osc_tuning_oct"
k_comp_osc_tuning	= "k_comp_osc_tuning"
k_comp_osc_id = "k_comp_osc_id"
k_comp_osc_sub	= "k_comp_osc_sub"
k_comp_osc_sub_not	= "k_comp_osc_sub_not"
k_comp_op_one_operand	= "k_comp_op_one_operand"
k_comp_op_two_operands	= "k_comp_op_two_operands"
k_comp_op_more_operands	= "k_comp_op_more_operands"
k_comp_op_feedback	= "k_comp_op_feedback"

k_comp_shape_default	= "k_comp_shape_default"
k_comp_shape_vol	= "k_comp_shape_vol"

# style guide keys
k_style_basic        = StyleGuide.BASIC.value
k_style_succint      = StyleGuide.SUCCINT.value
k_style_concise      = StyleGuide.CONCISE.value
k_style_detailed     = StyleGuide.DETAILED.value
k_style_specification= StyleGuide.SPECIFICATION.value

# waveform keys
k_wave_sine        = WaveformEnum.SINE.value
k_wave_triangle    = WaveformEnum.TRIANGLE.value
k_wave_trishaped   = WaveformEnum.TRISHAPED.value
k_wave_square      = WaveformEnum.SQUARE.value
k_wave_pulse       = WaveformEnum.PULSE.value
k_wave_pulse_thin  = WaveformEnum.PULSE_THIN.value
k_wave_sawtooth    = WaveformEnum.SAWTOOTH.value
k_wave_sawmulti    = WaveformEnum.SAWMULTI.value
k_wave_sawup       = WaveformEnum.SAWUP.value
k_wave_sawdown     = WaveformEnum.SAWDOWN.value
k_wave_noise       = WaveformEnum.NOISE.value
k_wave_noise_white = WaveformEnum.NOISE_WHITE.value
k_wave_noise_pink  = WaveformEnum.NOISE_PINK.value
k_wave_sample      = WaveformEnum.SAMPLE.value
k_wave_additive    = WaveformEnum.ADDITIVE.value
k_wave_digital     = WaveformEnum.DIGITAL.value
k_wave_fbk_saw    = WaveformEnum.FBK_SAW.value
k_wave_exotic      = WaveformEnum.EXOTIC.value
k_wave_s_h         = WaveformEnum.S_H.value
k_wave_other       = WaveformEnum.OTHER.value

# waveform keys
k_wave_width_narrow  = WaveformWidthEnum.NARROW.value
k_wave_width_thin    = WaveformWidthEnum.THIN.value
k_wave_width_normal  = WaveformWidthEnum.NORMAL.value
k_wave_width_wide    = WaveformWidthEnum.WIDE.value
k_wave_width_very_wide = WaveformWidthEnum.VERY_WIDE.value
k_wave_width_silence = WaveformWidthEnum.SILENCE.value

k_volume_grp0 = "k_volume_grp0" # =0%
k_volume_grp1 = "k_volume_grp1" #  0-20%
k_volume_grp2 = "k_volume_grp2" # 20-40%
k_volume_grp3 = "k_volume_grp3" # 40-60%
k_volume_grp4 = "k_volume_grp4" # 60-80%
k_volume_grp5 = "k_volume_grp5" # 80-100%
k_volume_grp6 = "k_volume_grp6" # =100%

k_operation_fm = "k_operation_fm"
k_operation_add = "k_operation_add"
k_operation_substract = "k_operation_substract"
k_operation_multiply = "k_operation_multiply"
k_operation_ringmod = "k_operation_ringmod"
k_operation_feedback = "k_operation_feedback"
