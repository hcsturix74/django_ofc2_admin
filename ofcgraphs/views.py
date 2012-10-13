# Create your views here.
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.http import HttpResponse,Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.utils import simplejson
from ofcgraphs.models import GraphTemplate, GraphElementTemplate
from random import randint






def home(request):
    """
    Just a simple homepage, flash object is inside template
    """

    return render_to_response("homepage.html", {"unique_message": "Specific to a template"}, context_instance=RequestContext(request))



def get_graph_data(request, gobj_id):
    """
    Retrieve data e provide a json for graph rendering
    """

    try:
       graph_template =  GraphTemplate.pub_objects.get(id = gobj_id)
    except MultipleObjectsReturned:
        raise Http404
    except ObjectDoesNotExist:
         raise Http404
    #create a dict
    ograph = graph_template.build_obj_graph()
    element_list = []
    for el in graph_template.graph_elements.all():
        #get values, here just random values
        vlist = [randint(0,800) for r in range(0,100)]

        #set element values using a list
        el.set_element_values(vlist)
        #append to a list of elements
        element_list.append(el.build_obj_element())
    #update
    ograph['elements']= element_list


    return HttpResponse(simplejson.dumps(ograph))



