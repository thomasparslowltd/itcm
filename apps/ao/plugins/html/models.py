from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models import CMSPlugin
from django.conf import settings
from django.utils.html import strip_tags
from django.utils.text import truncate_words

class HTML(CMSPlugin):
    """A block of html content"""
    body = models.TextField(_("body"))
    search_fields = ('body',)
    
    def __unicode__(self):
        return u"%s" % (truncate_words(strip_tags(self.body), 3)[:30]+"...")
