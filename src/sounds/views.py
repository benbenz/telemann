import json
import uuid
from django.conf import settings
from django.http import HttpResponse, StreamingHttpResponse , JsonResponse , FileResponse
from django.shortcuts import render
from django.templatetags.static import static
from django.views.generic.edit import CreateView , UpdateView
from django.urls import reverse_lazy
from .models import SoundGenerator , SoundSource
from .forms import SoundGeneratorForm , SoundSourceForm
from .core.audio import convert_to_wav , render_audio
import io

def sounds(request,generatorid=None):
    if generatorid is None:
        generators = SoundGenerator.objects.all()
        return render(request,"sounds/sounds.html",{
            'generators' : generators
        })
    else:
        generator = SoundGenerator.objects.get(id=generatorid)
        program = request.GET.get('p',0)
        bank    = request.GET.get('b',0)
        if isinstance(program,str):
            program = int(program)
        if isinstance(bank,str):
            bank = int(bank)
        if request.method == 'GET':
            try:
                sound_source = SoundSource.objects.get(generator=generator,midi_program=program,midi_bank=bank)
                form = SoundSourceForm(instance=sound_source)
            except SoundSource.DoesNotExist:
                sound_source = SoundSource.objects.create(generator=generator,midi_program=program,midi_bank=bank)
                form = SoundSourceForm()

            return render(request,"sounds/sounds.html",{
                'generator' : generator ,
                'program':program,
                'bank':bank,
                'form':form
            })
        elif request.method == 'POST':
            try:
                sound_source = SoundSource.objects.get(generator=generator,midi_program=program,midi_bank=bank)
                form = SoundSourceForm(request.POST,instance=sound_source)
                form.save()
            except SoundSource.DoesNotExist:
                sound_source = SoundSource.objects.create(generator=generator,midi_program=program,midi_bank=bank)
                form = SoundSourceForm(request.POST,instance=sound_source)
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

def render_sound(request,generatorid):
    program = request.GET.get('p',0)
    bank    = request.GET.get('b',0)
    generator:SoundGenerator = SoundGenerator.objects.get(id=generatorid)
    # pedalboard return 32 bits float data
    # content_type = f"audio/pcm;rate={generator.audio_device_samplerate};encoding=float;bits=32"
    content_type = "audio/wave"
    audio = render_audio(generator,bank=bank,program=program)
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
    return FileResponse(convert_to_wav(audio,generator.audio_device_samplerate),headers=headers)
    
def generators(request):
    generators = SoundGenerator.objects.all()
    return render(request,"sounds/generators.html",{'generators':generators})
    
def generator(request,generatorid):
    if request.method != "POST":
        return render(request,"sounds/generator.html",{

        })
    try:
        data = json.loads(request.body)
        return HttpResponse( "OK", status=200,content_type="text/html")
    except Exception as e:  # pylint: disable=broad-exception-caught
        error_message = f"Sorry, an error occurred: {type(e).__name__} - {str(e)}"
        return HttpResponse(error_message, content_type="text/plain", status=500)    
    

class SoundGeneratorCreateView(CreateView):
    model = SoundGenerator
    form_class = SoundGeneratorForm
    template_name = 'sounds/generator_form.html'  # Specify your template path
    success_url = reverse_lazy('sounds:generators')  # Redirect after a successful form submission

class SoundGeneratorUpdateView(UpdateView):
    model = SoundGenerator
    form_class = SoundGeneratorForm
    template_name = 'sounds/generator_form.html'  # You can use the same template as for creating
    success_url = reverse_lazy('sounds:generators')  # Redirect after a successful form update
