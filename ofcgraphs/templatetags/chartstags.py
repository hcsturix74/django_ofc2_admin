from random import randint
from django import template
import settings
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.http import HttpResponse
from django.utils.safestring import mark_safe
from ofcgraphs.models import GraphTemplate


#@register.inclusion_tag('tt-chart-simple.html')
#def show_simplechart(object_id):
#    """visualize example charts"""
#    try:
#       gtemplate =  GraphTemplate.pub_objects.get(id = object_id)
#    except MultipleObjectsReturned:
#        print "Multiple Objects!"
#    except ObjectDoesNotExist:
#         print "Object doas not exist!"
#
#    #settings data
#    for gel in gtemplate.graph_elements:
#        gel.values = [randint(0,9) for i in range(9)]
#
#    json= ''
#    return {
#            'width' : '100%',
#            'height': '400',
#            'data_files' : '/amedia/swf/ofc/data.json',# not used
#            'ofc_base_url_swf': settings.STATIC_URL +'/ofc2/',
#            'ofc' : '/graphs/%s/' % (object_id),
#            'loading_message' : 'loading chart',
#            }



