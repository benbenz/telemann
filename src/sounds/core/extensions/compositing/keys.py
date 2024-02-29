from enum import StrEnum , auto
from ..defs import StyleGuide

class CompositingKey(StrEnum):

    OSCILLATORS = auto()
    GLUE = auto()
    COMPOSITING = auto()
    SINGULAR = auto()
    PLURAL   = auto()
    BALANCED_MIX = auto()
    FORWRD_MIX = auto()


k_oscillators  = CompositingKey.OSCILLATORS.value
k_compositing  = CompositingKey.COMPOSITING.value
k_glue         = CompositingKey.GLUE.value
k_singular     = CompositingKey.SINGULAR.value
k_plural       = CompositingKey.PLURAL.value
k_balanced_mix = CompositingKey.BALANCED_MIX.value
k_forward_mix  = CompositingKey.FORWRD_MIX.value
k_basic        = StyleGuide.BASIC.value
k_succint      = StyleGuide.SUCCINT.value
k_concise      = StyleGuide.CONCISE.value
k_detailed     = StyleGuide.DETAILED.value

