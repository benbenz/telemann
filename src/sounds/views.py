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
from .core.audio import convert_to_wav , render_audio
import io

def sounds(request,srcid=None):
    if srcid is None:
        sources = SoundSource.objects.all()
        return render(request,"sounds/sounds.html",{
            'sources' : sources
        })
    else:
        source   = SoundSource.objects.get(id=srcid)
        program  = request.GET.get('p',0)
        bank     = request.GET.get('b',0)
        category = request.GET.get('c',None)
        if isinstance(program,str):
            program = int(program)
        if isinstance(bank,str):
            bank = int(bank)
        if request.method == 'GET':
            try:
                sound_tone = SoundTone.objects.get(source=source,midi_program=program,midi_bank=bank)
                form = SoundToneForm(instance=sound_tone)
            except SoundTone.DoesNotExist:
                sound_tone = SoundTone(source=source,midi_program=program,midi_bank=bank,category=category)
                form = SoundToneForm(instance=sound_tone)

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return render(request,"sounds/widgets/soundtone.html",{
                    'source' : source ,
                    'program':program,
                    'bank':bank,
                    'form':form
                })
            else:
                return render(request,"sounds/sounds.html",{
                    'source' : source ,
                    'program':program,
                    'bank':bank,
                    'form':form,
                })
        elif request.method == 'POST':
            try:
                sound_tone = SoundTone.objects.get(source=source,midi_program=program,midi_bank=bank)
                form = SoundToneForm(request.POST,instance=sound_tone)
                form.save()
            except SoundTone.DoesNotExist:
                sound_tone = SoundTone.objects.create(source=source,midi_program=program,midi_bank=bank)
                form = SoundToneForm(request.POST,instance=sound_tone)
                form.save()
            return JsonResponse("OK")     
           
    
def stream_audio(audio,framerate):
    # for frame in np.nditer(audio):
    #     bytes = frame.tobytes()
    #     yield bytes
    
    # we need to change format so that the <audio> element recognizes it
    wavaudio = convert_to_wav(audio,framerate)
    while wavaudio.readable:
        yield wavaudio.read(128)

def render_sound(request,srcid):
    program = request.GET.get('p',0)
    bank    = request.GET.get('b',0)
    source:SoundSource = SoundSource.objects.get(id=srcid)
    # pedalboard return 32 bits float data
    # content_type = f"audio/pcm;rate={source.audio_device_samplerate};encoding=float;bits=32"
    content_type = "audio/wave"
    audio = render_audio(source,bank=bank,program=program)
    headers = {
#        'Cache-Control': 'no-cache, no-store, must-revalidate',
#        'Content-Length': audio.size * audio.itemsize
    }
    # return StreamingHttpResponse(
    #     stream_audio(audio,generator.audio_device_samplerate),
    #     content_type=content_type,
    #     status=200,
    #     headers=headers
    # )
    return FileResponse(convert_to_wav(audio,source.audio_device_samplerate),headers=headers)
    
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
