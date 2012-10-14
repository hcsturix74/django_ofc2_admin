from django import template
from ofcgraphs import graph_settings
import settings


register = template.Library()




@register.inclusion_tag('tt-chart-simple.html')
def show_simple_graph(object_id, width=None, height=None):
    """present graph"""

    w = graph_settings.DEFAULT_OFC2_GRAPH_WIDTH
    h = graph_settings.DEFAULT_OFC2_GRAPH_HEIGHT
    
    if width is not None:
        w = width
    if height is None:
        h = height

    return {
            'width' : w,
            'height': h,
            'data_file' : '/graphs/%s/' % object_id,
            'ofc_base_url_swf': settings.STATIC_URL +'ofc2/',
            'ofc' : 'open-flash-chart.swf',
            'loading_message' : 'Loading graph...',
            }



