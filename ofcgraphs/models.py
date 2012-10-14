from django.db import models
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models.fields.related import ForeignKey
from django.db.models.fields import PositiveSmallIntegerField, CharField,\
    SlugField, TextField, IntegerField, FloatField,BooleanField
from django.utils import simplejson
from django.utils.safestring import mark_safe

from django.core.validators import MaxValueValidator
from ofcgraphs.managers import PublishedManager
#from widgets import ColorPickerWidget
from colors.fields import ColorField
import datetime




GRAPH_TYPE_CHOICES = (( 'line','LINE'),
                      ( 'linedot','LINE-DOT'),
                      ( 'bar','BAR'),
                      ( 'bar_3d','BAR-3D'),
                      #( 'pie','PIE'),
                      #( 'hbar','HBAR'),
                      )

INSPECTION_DATE_CHOICES = (( 'next','next'),
                           ( 'self','self'),
                           ( 'previous','previous'),)

SIZE_CHOICES = [(i,"%spx " % i)  for i in range(1,10)]
DOT_STYLE_CHOICES = (( 'dot','DOT'),
                      ( 'hollow-dot','HOLLOW-DOT'),
                      ( 'solid-dot','SOLID-DOT'),
                      ( 'star','STAR'),
                      ( 'bow','BOW'),
                      ( 'anchor','ANCHOR'),
                    )

#Two default values never changed...Till now
DEFAULT_TITLE_STYLE   = '{font-size: 20px; color:#0000ff; font-family:Helvetica; text-align:center;}'
DEFAULT_LEGEND_STYLE = '{color: #736AFF; font-size: 12px;}'

#Not yet supported but to be inserted in future
#EVENTS_LINE_ANIMATON_CHOICES = ( ( 'pop-up','POP-UP'),
#                            ( 'explode','EXPLODE'),
#                            ( 'mid-slide','MID-SLIDE'),
#                            ( 'drop','DROP'),
#                            ( 'fade-in','FADE-IN'),
#                            ( 'shrink-in','SHRINK-IN'),
#                        )









class GenericBaseModel(models.Model):
    """
    GenericBaseModel class - inherits from models.Model
    This class is an abstract structure for site
    content (not translatable fields, see GenericBaseTranslationModel) management
    It provides some basic attributes (i.e. table columns) common to Content base
    applications
    """
    is_published    = models.BooleanField(blank=True, default=True, verbose_name=_('Published'))
    created         = models.DateTimeField(verbose_name=_('Creation Date'), default=datetime.datetime.now())
    updated         = models.DateTimeField(verbose_name=_('Modify Date'), default=datetime.datetime.now())
    objects         = models.Manager()
    pub_objects     = PublishedManager()




    class Meta:
        abstract = True


    def save(self,*args, **kwargs):
        """
        This is the overridden save method
        """
        if not self.id:
            self.created = datetime.datetime.now()
        self.updated = datetime.datetime.now()
        super(GenericBaseModel, self).save(*args, **kwargs)


    def get_history(self):
        """
        This method retrieves the history for this object searching in LogEntry Table
        """
        lst = []
        try:
            lst = LogEntry.objects.filter(content_type=ContentType.objects.get_for_model(self).id, object_id=self.pk)
        except Exception:
            pass
        return lst


    def _get_creation_date(self):
        """
        This method retrieves the creation date for this object
        """
        return self.created
    creation_date = property(_get_creation_date)



    def _get_modify_date(self):
        """
        This method retrieves the modification date for this object
        """
        return self.updated
    modify_date = property(_get_modify_date)








class BaseGraphTemplate(GenericBaseModel):
    """
    GraphTemplateCategory class - inherits from GenericBaseModel
    """
    name = CharField(max_length=255, verbose_name = _('Name'))
    slug = SlugField(max_length=255, unique=True, verbose_name = _('Slug'))


    class Meta:
        #app_label   = 'graphs'
        verbose_name = _('Base Graph Template')
        verbose_name_plural = _('Base Graph Templates')


    def __unicode__(self):
        """
        Unicode function
        """
        return  u'%s' % _(self.name)


class GraphTemplateCategory(BaseGraphTemplate):
    """
    GraphTemplateCategory class - inherits from BaseGraphTemplate
    """
    description = TextField(blank=True,default='',verbose_name = _('Description'))

    class Meta:
        #app_label   = 'graphs'
        verbose_name = _('Graph Template Category')
        verbose_name_plural = _('Graph Template Categories')


    def __unicode__(self):
        """
        This the unicode method
        """
        return u'%s' % self.name



    def get_absolute_url(self):
        """
        This the get_absolute_url method
        """

        return '/graphs/category/%s' % self.slug






class GraphTemplate(BaseGraphTemplate):
    """
    GraphTemplateCategory class - inherits from BaseGraphTemplate
    JSON Format is used.
    Attributes implemented for this dict are:
      "title":{
        "text":"Many data lines",
        "style":"{font-size: 30px;}"
      },
      "y_legend":{
        "text":"Open Flash Chart",
        "style":"{font-size: 12px; color:#736AFF;}"
      },
    "x_axis":{
    "stroke":      1,
    "tick_height": 10,
    "colour":      "#d000d0",
    "grid_colour": "#00ff00",
    "labels":      ["January","February","March","April","May","June","July","August","September"]

    """

    fk_graph_template_category = ForeignKey('GraphTemplateCategory', related_name='graph_templates')


    title_text          = CharField(max_length=255, verbose_name = _('Title Text'), blank=True, null=True)
    title_style         = CharField(max_length=255, verbose_name = _('Title Style'), blank=True, null=True ,default = DEFAULT_TITLE_STYLE,
                                    help_text=_('Use CSS style (example: {font-size: 30px;background-color: #0000ff;}'))
    x_legend_text       = CharField(max_length=255, verbose_name = _('X Legend Text'))
    x_legend_style      = CharField(max_length=255, verbose_name = _('X Legend Style'), blank=True, null=True, default = DEFAULT_LEGEND_STYLE,
                                    help_text=_('Use CSS style (example: {font-size: 30px;background-color: #0000ff;}'))
    y_legend_text       = CharField(max_length=255, verbose_name = _('Y Legend Text'))
    y_legend_style      = CharField(max_length=255, verbose_name = _('Y Legend Style'), blank=True, null=True, default = DEFAULT_LEGEND_STYLE,
                                    help_text=_('Use CSS style (example: {font-size: 30px;background-color: #0000ff;}'))
    bg_colour           = ColorField(verbose_name = _('Background Colour'),default = 'eeeeee')
    x_axis_stroke       = IntegerField(validators=[MaxValueValidator(20)], verbose_name = _('X Axis Stroke'), blank=True, null=True,choices=SIZE_CHOICES)
    x_axis_tick_height  = IntegerField(validators=[MaxValueValidator(20)], verbose_name = _('X Axis Stroke Tick Height'), blank=True, null=True,choices=SIZE_CHOICES)
    x_axis_colour       = ColorField(verbose_name = _('X Axis Colour'), blank=True, null=True)
    x_axis_grid_colour  = ColorField(verbose_name = _('X Axis Grid Colour'), blank=True, null=True)
    x_axis_steps        = IntegerField(verbose_name = _('X Axis Steps'), blank=True, null=True)
    x_axis_min          = IntegerField(verbose_name = _('X Axis Min'), blank=True, null=True, help_text=_('Insert min value'))
    x_axis_max          = IntegerField(verbose_name = _('X Axis Max'), blank=True, null=True, help_text=_('Insert Max value'))
    x_axis_offset       = BooleanField(verbose_name = _('X Axis Offset'), default = True)
    x_axis_labels_labels= CharField(max_length=255, verbose_name = _('X Axis Labels'), blank=True, null=True)
    x_axis_labels_colour = ColorField(max_length=255, verbose_name = _('X Axis Labels Colour'), blank=True, null=True)

    y_axis_stroke       = IntegerField(validators=[MaxValueValidator(20)], verbose_name = _('Y Axis Stroke'), blank=True, null=True, choices=SIZE_CHOICES)
    y_axis_tick_length  = IntegerField(validators=[MaxValueValidator(20)], verbose_name = _('Y Axis Tick Length'), blank=True, null=True, choices=SIZE_CHOICES)
    y_axis_colour       = ColorField(max_length=255, verbose_name = _('Y Axis Colour'), blank=True, null=True)
    y_axis_grid_colour  = ColorField(max_length=255, verbose_name = _('Y Axis Grid Colour'), blank=True, null=True)
    y_axis_offset       = BooleanField(verbose_name = _('Y Axis Offset'), default = True)
    y_axis_steps        = IntegerField(verbose_name = _('Y Axis Steps'), blank=True, null=True)
    y_axis_min          = IntegerField(verbose_name = _('Y Axis Min'), blank=True, null=True, help_text=_('Insert min value'))
    y_axis_max          = IntegerField(verbose_name = _('Y Axis Max'), blank=True, null=True, help_text=_('Insert Max value'))
    y_axis_labels_labels= CharField(max_length=255, verbose_name = _('Y Axis Labels'), blank=True, null=True)
    y_axis_labels_colour= ColorField(max_length=255, verbose_name = _('Y Axis Labels Colour'), blank=True, null=True)
    is_y_axis_right_available = BooleanField(verbose_name = _('Y Axis-Right Available'), default = False)
    y_axis_right_min    = IntegerField(verbose_name = _('Y Axis-Right Min'), blank=True, null=True, help_text=_('Insert min value'))
    y_axis_right_max    = IntegerField(verbose_name = _('Y Axis-Right Max'), blank=True, null=True, help_text=_('Insert Max value'))
    y_axis_right_stroke = IntegerField(validators=[MaxValueValidator(20)], verbose_name = _('Y Axis-Right Stroke'), blank=True, null=True, choices=SIZE_CHOICES)
    y_axis_right_colour = ColorField(max_length=255, verbose_name = _('Y Axis-Right Colour'), blank=True, null=True)
    y_axis_right_steps  = IntegerField(verbose_name = _('Y Axis-Right Steps'), blank=True, null=True)
    y_axis_right_tick_length = IntegerField(validators=[MaxValueValidator(20)],verbose_name = _('Y Axis-Right Tick length '), blank=True, null=True)
    y_axis_right_labels_labels = CharField(max_length=255, verbose_name = _('Y Axis-Right Labels'), blank=True, null=True)
    y_axis_right_labels_colour = ColorField(max_length=255, verbose_name = _('Y Axis-Right Labels Colour'), blank=True, null=True)
    y_axis_right_offset       = BooleanField(verbose_name = _('Y Axis-Right Offset'), default = True)
    y_axis_right_grid_colour  = ColorField(max_length=255, verbose_name = _('Y Axis-Right Grid Colour'), blank=True, null=True)

    graph_template_json = CharField(max_length=2048, verbose_name = _('Graph Template JSON'), blank=True, null=True)


    class Meta:
        """
        Meta class
        """
        #app_label   = 'graphs'
        verbose_name = _('Graph Template')
        verbose_name_plural = _('Graph Templates')


    def __unicode__(self):
        """
        This the unicode method
        """
        return u'%s' % self.name


    
    def get_absolute_url(self):
        """
        This the get_absolute_url method
        """

        return '/graphs/%s' % self.slug


    def build_y_axis(self):
        yax = dict()
        yax['y_axis']  = dict()
        yax['y_axis']['labels']  = dict()
        #Y Axis
        if self.y_axis_tick_length:   yax['y_axis']['tick_length']= self.y_axis_tick_length
        if self.y_axis_colour:        yax['y_axis']['colour']     = '#%s' % self.y_axis_colour
        if self.y_axis_grid_colour:   yax['y_axis']['grid-colour']= '#%s' % self.y_axis_grid_colour
        if self.y_axis_offset:        yax['y_axis']['offset']     = self.y_axis_offset
        if self.y_axis_max:           yax['y_axis']['max'] = self.y_axis_max
        if self.y_axis_steps:         yax['y_axis']['steps'] = self.y_axis_steps
        if self.y_axis_min:           yax['y_axis']['min'] = self.y_axis_min
        if self.y_axis_stroke:        yax['y_axis']['stroke']     = self.y_axis_stroke
        if self.y_axis_labels_labels: yax['y_axis']['labels']['labels'] = self.y_axis_labels_labels
        if self.y_axis_labels_colour: yax['y_axis']['labels']['colour'] = '#%s' % self.y_axis_labels_colour
        return yax


    
    def build_y_axis_right(self):
        yaxr = dict()
        yaxr['y_axis_right']  = dict()
        yaxr['y_axis_right']['labels']  = dict()
        if self.y_axis_right_min:             yaxr['y_axis_right']['min'] = self.y_axis_right_min
        if self.y_axis_right_max:             yaxr['y_axis_right']['max'] = self.y_axis_right_max
        if self.y_axis_right_steps:           yaxr['y_axis_right']['steps'] = self.y_axis_right_steps
        if self.y_axis_right_stroke:          yaxr['y_axis_right']['stroke']     = self.y_axis_right_stroke
        if self.y_axis_right_colour:          yaxr['y_axis_right']['colour'] = '#%s' % self.y_axis_right_colour
        if self.y_axis_grid_colour:   yaxr['y_axis_right']['grid-colour']= '#%s' % self.y_axis_right_grid_colour
        if self.y_axis_right_tick_length:     yaxr['y_axis_right']['tick_length'] = self.y_axis_right_max
        if self.y_axis_right_labels_labels:     yaxr['y_axis_right']['labels']['labels'] = self.y_axis_right_labels_labels
        if self.y_axis_right_labels_colour:     yaxr['y_axis_right']['labels']['colour'] = '#%s' % self.y_axis_right_labels_colour
        if self.y_axis_right_offset:        yaxr['y_axis_right']['offset']     = self.y_axis_right_offset
        return yaxr

    def build_x_legend(self):
        xleg = dict()
        xleg['x_legend'] = dict()
        #Y legend
        if self.x_legend_text:      xleg['x_legend']['text']      = self.x_legend_text
        if self.x_legend_style:     xleg['x_legend']['style']     = self.x_legend_style
        return xleg

    def build_y_legend(self):
        yleg = dict()
        yleg['y_legend'] = dict()
        #Y legend
        if self.y_legend_text:      yleg['y_legend']['text']      = self.y_legend_text
        if self.y_legend_style:     yleg['y_legend']['style']     = self.y_legend_style
        return yleg

    def build_x_axis(self):
        xax = dict()
        xax['x_axis']  = dict()
        xax['x_axis']['labels']  = dict()
        #X Axis
        if self.x_axis_stroke:      xax['x_axis']['stroke']     = self.x_axis_stroke
        if self.x_axis_tick_height: xax['x_axis']['tick_height'] = self.x_axis_tick_height
        if self.x_axis_colour:      xax['x_axis']['colour']      = '#%s' % self.x_axis_colour
        if self.x_axis_grid_colour: xax['x_axis']['grid-colour'] = '#%s' % self.x_axis_grid_colour
        if self.x_axis_steps:       xax['x_axis']['steps'] = self.x_axis_steps
        if self.x_axis_min:         xax['x_axis']['min'] = self.x_axis_min
        if self.x_axis_max:         xax['x_axis']['max'] = self.x_axis_max
        if self.x_axis_labels_labels: xax['x_axis']['labels']['labels'] = self.x_axis_labels_labels
        if self.x_axis_labels_colour: xax['x_axis']['labels']['colour'] = '#%s' % self.x_axis_labels_colour
        if self.x_axis_offset:        xax['x_axis']['offset']     = self.x_axis_offset
        return xax



    def build_title(self):
        title_dict = dict()
        if self.title_text:
            if self.title_style:
                title_dict.setdefault('title',{}).setdefault('style','%s' % self.title_style)
            title_dict['title'].setdefault('text',self.title_text)
        else:
            title_dict.setdefault('title',{})
        return title_dict





    def build_obj_graph(self):
        """
        This method creates the dict with attributes inserted
        """
        obj={}
        try:
            rel_elements = self.graph_elements.all()
            r_elements_list=[]
            for e in rel_elements:
                el_obj_dict = e.build_obj_element()
                #print el_obj_dict
                r_elements_list.append(el_obj_dict)
            obj['elements'] = r_elements_list
        except Exception:
            print "No Elements related!"
        #set bg_colour
        if self.bg_colour:          obj['bg_colour']              = '#%s' % self.bg_colour
        #update dictionaries
        obj.update(self.build_title())
        obj.update(self.build_x_axis())
        obj.update(self.build_y_axis())
        #this is the only one configurable (normally there is no need for the second axis)
        if self.is_y_axis_right_available:
            obj.update(self.build_y_axis_right())
        obj.update(self.build_x_legend())
        obj.update(self.build_y_legend())
        return obj


    def to_json(self):
        """
        This method returns a json given a dict object
        return - json object built from obj
        """
        obj = self.build_obj_graph()
        return simplejson.dumps(obj)
        


    def save(self,*args, **kwargs):
        """
        This is just the save method, crate a json and save it in the corresponding field
        """
        #tmpl_dict_object = self.build_obj_graph()
        self.graph_template_json = self.to_json()
        super(GraphTemplate,self).save(*args, **kwargs)


class GraphElementTemplate(BaseGraphTemplate):
    """
    GraphElementTemplate class - inherits from BaseGraphTemplate
    JSON Format is used.
    Attributes implemented for this dict are:

    "type":      "line",
    "colour":    "#9933CC",
    "text":      "Page views",
    "width":     2,
    "font-size": 10,
    "dot-size":  6,
    "values" :   [15,18,19,14,17,18,15,18,17]

    """
    type               = CharField(max_length=255, verbose_name = _('Type'), choices=GRAPH_TYPE_CHOICES)
    fk_graph_template  = ForeignKey('GraphTemplate', related_name='graph_elements')
    alpha              = FloatField(verbose_name = _('Alpha'), default = 0.5)
    colour             = ColorField(verbose_name = _('Colour'), blank=True, null=True)
    text               = CharField(max_length=255, verbose_name = _('Text'))
    width              = PositiveSmallIntegerField(verbose_name = _('Width'))
    font_size          = PositiveSmallIntegerField(verbose_name = _('Font Size'))
    dot_size           = PositiveSmallIntegerField(verbose_name = _('Dot Size'))
    tooltip            = CharField(max_length=100, verbose_name = _('Tooltip'), default= _('#val#'), help_text=_('Use some keywords like #val# Example: value:#val#'))
    inspection         = CharField(max_length=255, verbose_name = _('Ispect'),  choices=INSPECTION_DATE_CHOICES,default='self')
    dot_style_type     = CharField(max_length=255, verbose_name = _('Dot-Style Type'), choices= DOT_STYLE_CHOICES, blank=True, null=True)
    dot_style_dot_size = PositiveSmallIntegerField(verbose_name = _('Dot-Style Size'),blank=True, null=True)
    dot_style_colour   = ColorField(verbose_name = _('Dot-Style Colour'), blank=True, null=True)
    dot_style_halo_size= PositiveSmallIntegerField(verbose_name = _('Dot-Style Halo Size'), blank=True, null=True)
    graph_element_json = CharField(max_length=1024, verbose_name = _('Element JSON'), blank=True, null=True)


    values = []

    class Meta:
        """
        Meta class
        """
        #app_label   = 'graphs'
        verbose_name = _('Graph Template Element')
        verbose_name_plural = _('Graph Template Elements')


    def set_values_in_object(self, obj, vl):
        """
        This method set the values for a graph element object
        obj - the element object where the values have to be set
        vl - the list of values
        """
        obj['values'] = vl

        

    def set_element_values(self, vl):
        """
        This method set the values for a graph element,
        setting the corresponding attribute.
        vl - the list of values to be set
        """
        self.values = vl


    def build_dot_style(self):
        """
        """
        ds = dict()
        ds['dot-style'] = dict()
        if self.dot_style_type:  ds['dot-style']['type']= self.dot_style_type
        if self.dot_style_dot_size:  ds['dot-style']['dot-size']= self.dot_style_dot_size
        if self.dot_style_halo_size:  ds['dot-style']['halo-size']= self.dot_style_halo_size
        if self.dot_style_colour:  ds['dot-style']['colour']= self.dot_style_colour
        return ds





    def build_obj_element(self):
        obj = dict()
        obj['values']=[]
        if self.type:
            t = self.type
            if self.type == 'linedot':
                t = 'line'
            obj['type'] = t

            if self.tooltip:    obj['tip'] =  str(self.tooltip)
            if self.colour:     obj['colour']    = '#%s' % self.colour
            if self.alpha:      obj['alpha']    = self.alpha
            if self.text:       obj['text']      = str(self.text)
            if self.width:      obj['width']     = self.width
            if self.font_size:  obj['font-size'] = self.font_size
            if self.dot_size:   obj['dot-size']  = self.dot_size
            if self.type == 'linedot':
                dst = self.build_dot_style()
                obj.update(dst)
        if len(self.values)>0:
            obj['values']    = self.values

        
        return obj

    def to_json(self):
        """
        This method returns a json given a dict object
        return - json object built from obj
        """
        obj = self.build_obj_element()
        return simplejson.dumps(obj)




    def to_json(self):
        """
        This method returns a json given a dict object
        obj - the dict object to be passed
        return - json object built from obj
        """
        obj = self.build_obj_element()
        return simplejson.dumps(obj)


    def __unicode__(self):
        """
        This the unicode method
        """
        return u'%s' % self.name


    
    def save(self,*args, **kwargs):
        """
        This is just the save method, crate a json and save it in the corresponding field
        """
        self.graph_element_json = self.to_json()
        super(GraphElementTemplate,self).save(*args, **kwargs)




