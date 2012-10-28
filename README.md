django_ofc2_admin
=================

Store your open-flash-chart-2 settings templates in admin


``django_ofc2_admin`` is a simple django application for managing
open-flash-chart-2 graph template in django admin

I needed a simple way for having all ofc2 settings in administration re-using
them in my project(s)


Dependecies
-----------

* Open-Flash-Chart-2: http://teethgrinder.co.uk/open-flash-chart-2/
* guillaumeesquevin/django-colors: https://github.com/guillaumeesquevin/django-colors



Examples
--------

This is a complete project based on sqlite database

::
python manage.py runserver


ADMIN LOGIN:
  username: admin
  password: admin

You can, of course, delete the DB (graphdb) and perform a syncdb:

python manage.py syncdb

Some fixtures are present in ofcgraphs application for some Graph Templates demo
Remove or override them if needed.


Screenshots
-----------------------

Some screenshots are presented here to see the possible output graphs.
This projects does NOT support all the available graph types provided by OFC2 library.

* Line graphs

![screenshot-1](https://raw.github.com/hcsturix74/django_ofc2_admin/master/screenshots/screenshot-1.png)

* 3D Bar graphs

![screenshot-2](https://raw.github.com/hcsturix74/django_ofc2_admin/master/screenshots/screenshot-2.png)


* Bar graphs

![screenshot-3](https://raw.github.com/hcsturix74/django_ofc2_admin/master/screenshots/screenshot-3.png)


* Multi graphs (bars + line)

![screenshot-4](https://raw.github.com/hcsturix74/django_ofc2_admin/master/screenshots/screenshot-4.png)


* Line Dot graphs (Hollow, solid, star...)

![screenshot-5](https://raw.github.com/hcsturix74/django_ofc2_admin/master/screenshots/screenshot-5.png)


Usage
-----------------------

This django application just manages graph templates and elements (i.e. data type series) but does not provide
a link to your physical data which could be stored in another table application or model.


In views.py you can see a demo view which is something like:

```python

    def get_graph_data(request, gobj_id):
        """
        Retrieve data e provide a json for graph rendering
        Here data are set randomly, just a demo to see how it works
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
            vlist = [randint(0,800) for r in range(0,24)]

            #set element values using a list
            el.set_element_values(vlist)
            #append to a list of elements
            element_list.append(el.build_obj_element())
        #update
        ograph['elements']= element_list


        return HttpResponse(simplejson.dumps(ograph))

```

This is just a guideline to show how data could be presented to the user but keep in mind that
it is up to you to retrieve data from your models or apps and then set the values using:
'set_element_values' function.

It's quite simple:
 * Retrieve your data and put them in a list
 * Call on an element "set_element_value" method passing the list
 * Append the element to the graph
 * return using HttpResponse the json of the graph



If you are using a django model for your data, alternatively you can create a ForeignKey in this
model in order to link it to a particular Graph Template.
In this way, if you have different models for different measures (with numeric values stored)
you can customize the graph for each.
Example:

```python

    class MyDataModel(models.Model):
        data_title       = models.CharField(max_length=255, verbose_name = _('Title'))
        date             = models.DateField(verbose_name = _(u'Start Date'))
        value_1          = models.FloatField(verbose_name=_(u'Value 1'), blank=True, null=True)
        value_2          = models.FloatField(verbose_name=_(u'Value 2'), blank=True, null=True)
        ...
        #create here a ForignKey to your Graph Template
        graph_template   = models.ForeignKey('GraphTemplate',verbose_name= _('Graph Template'), blank=True, null=True)

        # Continue with your own model implementation
        ....
```

Of course you have to manage the data retrieval and graph creation in your application views.py using 
the above example "get_graph_data(request, gobj_id)" as guideline.



Application Structure
-----------------------------------------

Here you can see tables structure (models.py class structure).
For this I've used "modelviz.py" script which is part of django_extension application.

![screenshot](https://raw.github.com/hcsturix74/django_ofc2_admin/master/screenshots/ofcgraphs_models.png)