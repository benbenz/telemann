import json
import uuid
from django.conf import settings
from django.http import HttpResponse, StreamingHttpResponse , JsonResponse
from django.shortcuts import render
from django.templatetags.static import static

def sound(request, conversation_id=None):
    if not conversation_id:
        conversation_id = uuid.uuid4()
    if request.method != "POST":
        return render(
            request,
            "sounds/sound.html",
            {
               
            },
        )

    try:
        data = json.loads(request.body)
        return HttpResponse( "OK", status=200,content_type="text/html")
    except Exception as e:  # pylint: disable=broad-exception-caught
        error_message = f"Sorry, an error occurred: {type(e).__name__} - {str(e)}"
        return HttpResponse(error_message, content_type="text/plain", status=500)


