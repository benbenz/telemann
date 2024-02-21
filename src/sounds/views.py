import json
import uuid
from django.conf import settings
from django.http import HttpResponse, StreamingHttpResponse , JsonResponse , FileResponse
from django.shortcuts import render
from django.templatetags.static import static
from django.views.generic.edit import CreateView , UpdateView
from django.urls import reverse_lazy
from .models import SoundSource , SoundTone
from .forms import SoundSourceForm , SoundToneForm
from .core.audio import convert_to_wav , render_audio , get_sound_analysis
from .core.midi import MIDIPattern , parse_new_program_value
import io
import math

def sounds(request,srcid=None):
    if srcid is None:
        sources = SoundSource.objects.all()
        return render(request,"sounds/sounds.html",{
            'sources' : sources
        })
    else:
        source   = SoundSource.objects.get(id=srcid)
        program  = request.GET.get('p',0)
        bank_msb = request.GET.get('bm',0)
        bank_lsb = request.GET.get('bl',0)
        pattern  = request.GET.get('ptn')
        category = request.GET.get('c',None)
        if isinstance(program,str):
            program = int(program)
        if isinstance(bank_msb,str):
            bank_msb = int(bank_msb)
        if isinstance(bank_lsb,str):
            bank_lsb = int(bank_lsb)

        # looping feature
        # we let the UI be "ignorant" (only increment/decrement program...)
        # and the view is handling the computation of bank+program
        bank_msb , bank_lsb , program = parse_new_program_value(source,bank_msb,bank_lsb,program)

        if request.method == 'GET':
            try:
                sound_tone = SoundTone.objects.get(source=source,midi_program=program,midi_bank_msb=bank_msb,midi_bank_lsb=bank_lsb)
                category = sound_tone.category
                form = SoundToneForm(instance=sound_tone)
            except SoundTone.DoesNotExist:
                sound_tone = SoundTone(source=source,midi_program=program,midi_bank_msb=bank_msb,midi_bank_lsb=bank_lsb,category=category)
                form = SoundToneForm(instance=sound_tone)

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return render(request,"sounds/widgets/soundtone.html",{
                    'source' : source ,
                    'bank_msb':bank_msb,
                    'bank_lsb':bank_lsb,
                    'program':program,
                    'pattern':pattern,
                    'patterns':MIDIPattern.__members__.items(),
                    'category':category,
                    'form':form
                })
            else:
                return render(request,"sounds/sounds.html",{
                    'source' : source ,
                    'bank_msb':bank_msb,
                    'bank_lsb':bank_lsb,
                    'program':program,
                    'pattern':pattern,
                    'patterns':MIDIPattern.__members__.items(),
                    'category':category,
                    'form':form,
                })
        elif request.method == 'POST':
            try:
                sound_tone = SoundTone.objects.get(source=source,midi_program=program,midi_bank_msb=bank_msb,midi_bank_lsb=bank_lsb)
                form = SoundToneForm(request.POST,instance=sound_tone)
                form.save()
            except SoundTone.DoesNotExist:
                sound_tone = SoundTone.objects.create(source=source,midi_program=program,midi_bank_msb=bank_msb,midi_bank_lsb=bank_lsb)
                form = SoundToneForm(request.POST,instance=sound_tone)
                form.save()
            return JsonResponse({"response":"OK","error":None})     
           
    
def stream_audio(audio,framerate):
    # for frame in np.nditer(audio):
    #     bytes = frame.tobytes()
    #     yield bytes
    
    # we need to change format so that the <audio> element recognizes it
    wavaudio = convert_to_wav(audio,framerate)
    while wavaudio.readable:
        yield wavaudio.read(128)

def render_sound(request,srcid):
    program  = request.GET.get('p',0)
    bank_msb = request.GET.get('bm',0)
    bank_lsb = request.GET.get('bl',0)
    pattern  = request.GET.get('ptn')

    if isinstance(program,str):
        program = int(program)
    if isinstance(bank_msb,str):
        bank_msb = int(bank_msb)
    if isinstance(bank_lsb,str):
        bank_lsb = int(bank_lsb)
    if pattern is not None:
        pattern = MIDIPattern[pattern]

    source:SoundSource = SoundSource.objects.get(id=srcid)

    bank_msb , bank_lsb , program = parse_new_program_value(source,bank_msb,bank_lsb,program)

    audio = render_audio(source,
                         bank_msb=bank_msb,
                         bank_lsb=bank_lsb,
                         program=program,
                         pattern=pattern)
    headers = {
#        'Cache-Control': 'no-cache, no-store, must-revalidate',
#        'Content-Length': audio.size * audio.itemsize
    }
    return FileResponse(convert_to_wav(audio,source.audio_device_samplerate),headers=headers)


def analyze_sound(request,srcid):
    program  = request.GET.get('p',0)
    bank_msb = request.GET.get('bm',0)
    bank_lsb = request.GET.get('bl',0)

    if isinstance(program,str):
        program = int(program)
    if isinstance(bank_msb,str):
        bank_msb = int(bank_msb)
    if isinstance(bank_lsb,str):
        bank_lsb = int(bank_lsb)

    source:SoundSource = SoundSource.objects.get(id=srcid)

    bank_msb , bank_lsb , program = parse_new_program_value(source,bank_msb,bank_lsb,program)

    sound_info = get_sound_analysis(source,bank_msb=bank_msb,bank_lsb=bank_lsb,program=program)

    return JsonResponse(sound_info)
    
def sources(request):
    sources = SoundSource.objects.all()
    return render(request,"sounds/sources.html",{'sources':sources})
    
def source(request,srcid):
    if request.method != "POST":
        return render(request,"sounds/source.html",{

        })
    try:
        data = json.loads(request.body)
        return HttpResponse( "OK", status=200,content_type="text/html")
    except Exception as e:  # pylint: disable=broad-exception-caught
        error_message = f"Sorry, an error occurred: {type(e).__name__} - {str(e)}"
        return HttpResponse(error_message, content_type="text/plain", status=500)    
    

class SoundSourceCreateView(CreateView):
    model = SoundSource
    form_class = SoundSourceForm
    template_name = 'sounds/source_form.html'  # Specify your template path
    success_url = reverse_lazy('sounds:sources')  # Redirect after a successful form submission

class SoundSourceUpdateView(UpdateView):
    model = SoundSource
    form_class = SoundSourceForm
    template_name = 'sounds/source_form.html'  # You can use the same template as for creating
    success_url = reverse_lazy('sounds:sources')  # Redirect after a successful form update
