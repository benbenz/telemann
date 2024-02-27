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
from .core.audio import convert_to_wav , convert_to_pcm , render_audio , get_sound_analysis , get_image_data
from .core.midi import MIDIPattern , parse_new_program_value
import io
import math
from tags.models import Tag
from tags.views import get_most_popular_tags

def sounds(request,srcid=None):
    if srcid is None:
        sources = SoundSource.objects.all()
        return render(request,"sounds/sounds.html",{
            'sources' : sources
        })
    else:
        source   = SoundSource.objects.get(id=srcid)
        bank_msb , bank_lsb , program , pattern = get_program_info(request)
        category = request.GET.get('c',None)

        # looping feature
        # we let the UI be "ignorant" (only increment/decrement program...)
        # and the view is handling the computation of bank+program
        bank_msb , bank_lsb , program = parse_new_program_value(source,bank_msb,bank_lsb,program)

        if request.method == 'GET':
            try:
                sound_tone = SoundTone.objects.prefetch_related('tags').get(source=source,midi_program=program,midi_bank_msb=bank_msb,midi_bank_lsb=bank_lsb)
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
                    'pattern':pattern.name if pattern else None,
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
                    'pattern':pattern.name if pattern else None,
                    'patterns':MIDIPattern.__members__.items(),
                    'category':category,
                    'form':form,
                    'tags':get_most_popular_tags()
                })
        elif request.method == 'POST':
            try:
                sound_tone = SoundTone.objects.get(source=source,midi_program=program,midi_bank_msb=bank_msb,midi_bank_lsb=bank_lsb)
                form = SoundToneForm(request.POST,instance=sound_tone)
                sound_tone = form.save()                
            except SoundTone.DoesNotExist:
                sound_tone = SoundTone.objects.create(source=source,midi_program=program,midi_bank_msb=bank_msb,midi_bank_lsb=bank_lsb)
                form = SoundToneForm(request.POST,instance=sound_tone)
                sound_tone = form.save()
                
            resp = json.loads(form.cleaned_data['tags'])
            sound_tone.tags.clear()
            if 'items' in resp:
                for item in resp['items']:
                    tagobj , created = Tag.objects.get_or_create(tag=item['name'])
                    if not sound_tone.tags.contains(tagobj):
                        sound_tone.tags.add(tagobj)
            sound_tone.save()

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
    
    bank_msb , bank_lsb , program , pattern = get_program_info(request)

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

    format = request.GET.get('f','wav')
    mime = request.GET.get('mt',None)
    if format == 'wav':
        if not mime:
            mime = 'audio/wave' 
        return FileResponse(convert_to_wav(audio,source.audio_device_samplerate),content_type=mime,headers=headers)
    elif format == 'pcm':
        content_type = f"audio/pcm;rate={source.audio_device_samplerate};encoding=int;bits=16"
        return FileResponse(convert_to_pcm(audio,convertto16bits=True),content_type=content_type,headers=headers)

def analyze_sound(request,srcid):

    bank_msb , bank_lsb , program , _ = get_program_info(request)

    source:SoundSource = SoundSource.objects.get(id=srcid)

    bank_msb , bank_lsb , program = parse_new_program_value(source,bank_msb,bank_lsb,program)

    sound_info = get_sound_analysis(source,bank_msb=bank_msb,bank_lsb=bank_lsb,program=program)

    return JsonResponse(sound_info)


def capture_sound_image(request,srcid):

    bank_msb , bank_lsb , program , _ = get_program_info(request)

    source:SoundSource = SoundSource.objects.get(id=srcid)

    bank_msb , bank_lsb , program = parse_new_program_value(source,bank_msb,bank_lsb,program)

    image_data = get_image_data(source,bank_msb=bank_msb,bank_lsb=bank_lsb,program=program)

    #return JsonResponse({"image":image_data,"error":None})
    return FileResponse(image_data,content_type='image/jpeg')

def get_program_info(request):
    bank_msb = request.GET.get('bm',0)
    bank_lsb = request.GET.get('bl',0)
    program  = request.GET.get('p',0)
    pattern  = request.GET.get('ptn')

    if isinstance(bank_msb,str):
        bank_msb = int(bank_msb)
    if isinstance(bank_lsb,str):
        bank_lsb = int(bank_lsb)
    if isinstance(program,str):
        program = int(program)
    if pattern is not None:
        pattern = MIDIPattern[pattern]

    return bank_msb , bank_lsb , program , pattern

    
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

def soundsource_post(request,pk):
    try:
        sound_source = SoundSource.objects.get(pk=pk)
        if request.method=='POST':
            form = SoundSourceForm(request.POST,instance=sound_source)
            sound_source = form.save()                
        else:
            form = SoundSourceForm(instance=sound_source)
        return render(request,"sounds/source_form.html",{
            'form' : form
        })
    except SoundSource.DoesNotExist:
        return HttpResponse(status=404)
