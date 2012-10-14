__author__ = 'Luca'


from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from models import GraphTemplateCategory , GraphTemplate , GraphElementTemplate
import settings


class GraphElementTemplateAdminInline(admin.StackedInline):
    """
    GraphElementTemplateAdminInline class - inherits from admin.StackedInline
    This class is a admin stacked for an element (example: Lines Bar Color)
    to add Chart view
    """
    model = GraphElementTemplate
    max_num = 3
    extra = 1
    fk_name = 'fk_graph_template'
    fieldsets = (
        (None, {
            'fields':(  ('name', 'slug','is_published',),
                        ('type', 'colour', 'width'),
                        ('font_size','dot_size',),
                        ('inspection','tooltip',),
                        ('dot_style_type', 'dot_style_dot_size', 'dot_style_colour', 'dot_style_halo_size'),
                     )
        }),

        ('Json', {
            'classes': ('collapse',),
            'fields': ('graph_element_json',)
        }),
    )
    prepopulated_fields = {"slug": ("name",)}



class GraphTemplateAdmin(admin.ModelAdmin):
    """
    GraphElementTemplateAdminInline class - inherits from admin.ModelAdmin
    This class is a admin stacked for a template graph.
    One template graph can contain more than one graph element.
    """
    fieldsets = (
        (None, {
            'fields': ('name', 'slug','is_published', 'fk_graph_template_category')
        }),
        ('Title', {
            'classes': ('collapse',),
            'fields': (
                        ('title_text','title_style','bg_colour',),

                      )

        }),
        ('X-Axis', {
            'classes': ('collapse',),
            'fields': (
                       ('x_axis_labels_labels','x_axis_labels_colour'),
                       ('x_axis_colour', 'x_axis_grid_colour',),
                       ('x_axis_offset','x_axis_stroke','x_axis_tick_height', ),
                       ('x_axis_min','x_axis_max','x_axis_steps' ),
                       ('x_legend_style', 'x_legend_text')

            )
        }),
         ('Y-Axis', {
            'classes': ('collapse',),
            'fields': (
                       ('y_axis_labels_labels','y_axis_labels_colour'),
                       ('y_axis_colour', 'y_axis_grid_colour',),
                       ('y_axis_offset','y_axis_stroke','y_axis_tick_length', ),
                       ('y_axis_min','y_axis_max','y_axis_steps' ),
                       ('y_legend_style', 'y_legend_text')
            )
        }),
          ('Y-Axis-Right', {
            'classes': ('collapse',),
            'fields': (
                       ('is_y_axis_right_available',),
                       ('y_axis_right_labels_labels','y_axis_right_labels_colour'),
                       ('y_axis_right_colour', 'y_axis_right_grid_colour',),
                       ('y_axis_right_offset','y_axis_right_stroke','y_axis_right_tick_length', ),
                       ('y_axis_right_min','y_axis_right_max','y_axis_right_steps' ),

            )
        }),
        ('Json', {
            'classes': ('collapse',),
            'fields': ('graph_template_json',)
        }),
    )
    
    list_display = ('id', 'name', 'slug','fk_graph_template_category')
    list_display_links = ['id', 'name',]
    list_filter = ('name', 'fk_graph_template_category')
    prepopulated_fields = {"slug": ("name",)}
    inlines = [GraphElementTemplateAdminInline,]
    save_on_top = True
    save_as = True


    


class GraphTemplateCategoryAdmin(admin.ModelAdmin):
    """
    GraphTemplateCategoryAdmin class - inherits from admin.ModelAdmin
    This class is category container for graphs
    """
    fieldsets = (
        (None, {
            'fields': ('name', 'slug','is_published','description')
        }),
       
    )
    list_display = ('name', 'slug',)
    list_filter = ('name',)
    prepopulated_fields = {"slug": ("name",)}




admin.site.register(GraphTemplate, GraphTemplateAdmin)
admin.site.register(GraphTemplateCategory,GraphTemplateCategoryAdmin)