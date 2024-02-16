import json
import uuid
from django.conf import settings
from django.http import HttpResponse, StreamingHttpResponse , JsonResponse
from django.shortcuts import render
from django.templatetags.static import static
from django.views.generic.edit import CreateView , UpdateView
from django.urls import reverse_lazy
from .models import SoundGenerator
from .forms import SoundGeneratorForm



def sounds(request):
    return render(request,"sounds/sounds.html",{})

def sound(request,soundid):
    if request.method != "POST":
        return render(request,"sounds/sound.html",{

        })
    try:
        data = json.loads(request.body)
        return HttpResponse( "OK", status=200,content_type="text/html")
    except Exception as e:  
        error_message = f"Sorry, an error occurred: {type(e).__name__} - {str(e)}"
        return HttpResponse(error_message, content_type="text/plain", status=500)
    
def generators(request):
    return render(request,"sounds/generators.html",{})
    
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




