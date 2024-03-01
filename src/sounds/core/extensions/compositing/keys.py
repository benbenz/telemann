from enum import StrEnum , auto
from ..defs import StyleGuide , WaveformEnum , WaveformWidthEnum, CompositingKey

# access keys
k_description       = CompositingKey.DESCRIPTION.value
k_oscillators       = CompositingKey.OSCILLATORS.value
k_oscillator        = CompositingKey.OSCILLATOR.value
k_shape             = CompositingKey.SHAPE.value
# global keys
k_compositing       = CompositingKey.COMPOSITING.value
k_glue              = CompositingKey.GLUE.value
k_osc_type          = CompositingKey.OSC_TYPE.value
k_osc_article       = CompositingKey.OSC_ARTICLE.value
# compositing keys
k_comp_oscs_singular     = CompositingKey.OSCS_SINGULAR.value
k_comp_oscs_plural       = CompositingKey.OSCS_PLURAL.value
k_comp_oscs_mix_balanced = CompositingKey.OSCS_MIX_BALANCED.value
k_comp_oscs_mix_forward  = CompositingKey.OSCS_MIX_FORWARD.value
k_comp_osc_singular      = CompositingKey.OSC_SINGULAR.value
k_comp_osc_plural        = CompositingKey.OSC_PLURAL.value
k_comp_osc_vol_text      = CompositingKey.OSC_COMPOSITING_VOL_TEXT.value
k_comp_osc_vol_number    = CompositingKey.OSC_COMPOSITING_VOL_NUMBER.value
k_comp_osc_sub           = CompositingKey.OSC_SUB.value
k_comp_osc_sub_not       = CompositingKey.OSC_SUB_NOT.value
k_comp_shape_default     = CompositingKey.SHAPE_COMPOSITING_DEFAULT.value
k_comp_shape_vol         = CompositingKey.SHAPE_COMPOSITING_VOL.value

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
k_wave_feedback    = WaveformEnum.FEEDBACK.value
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