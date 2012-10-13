__author__ = 'Luca'

from django.db import models



class PublishedManager(models.Manager):
    """
    This manager implements the get_query_set() method
    and  filters only the published 'contents'
    """

    def get_query_set(self):
        """
        This is the get_query_set method override.
        Here only published stuff is retrieved; this filter is on
        is_published field.
        """
        return super(PublishedManager, self).get_query_set().filter(is_published=True)
  