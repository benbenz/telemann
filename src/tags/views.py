from django.conf import settings
from django.http import HttpResponse, StreamingHttpResponse , JsonResponse , FileResponse
from django.shortcuts import render
from django.templatetags.static import static
from django.urls import reverse_lazy
from .models import Tag
from django.db.models import Count


def get_most_popular_tags(num_tags=20):
    # Aggregate the count of each tag
    tag_counts = Tag.objects.annotate(num_sounds=Count('sounds'))
    
    # Order the tags by the number of associated sounds in descending order
    # do not select the "words"/pre-selected tags, only the new ones from the user ...
    popular_tags = tag_counts.filter(select=False).order_by('-num_sounds')[:num_tags]
    
    return popular_tags

def get_words(with_groups=True):
    if with_groups:
        tags = Tag.objects.filter(select=True).order_by('group','tag').all()
        group = None
        result = []
        for tag in tags:
            if group is None or group != tag.group:
                result.append({'group_name':tag.group})
                group = tag.group
            result.append(tag)
        tags = result 
    else:
        tags = Tag.objects.filter(select=True).order_by('tags').all()
    
    return tags

def tags_search(request):
    if request.method == 'GET':
        q = request.GET.get('q',None)
        if q is None:
            return JsonResponse(status=400) 
        tags = []
        try:
            tags = Tag.objects.filter(tag__contains=q).all()
            itemsList = []
            for tag in tags:
                itemsList.append({
                    "name": tag.tag ,
                    "id":tag.id
                })
        except Tag.DoesNotExist:
            pass
        return JsonResponse(itemsList,safe=False)
    else:
        return JsonResponse(status=404)
    

def tags_widget(request):

    return render(request,"tags/widgets/tags.html",{
        'tags' : get_most_popular_tags ,
    })    
    