from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models import CMSPlugin
from publisher import Publisher

if 'reversion' in settings.INSTALLED_APPS:
    import reversion

class PublicationList(CMSPlugin):
    """A list of references to published papers/books etc
    """
    def __unicode__(self):
        return u" | ".join(map(unicode,list(self.publication_set.all())))
        
class Publication(Publisher):
    """
    A published paper/book etc
    """
    publicationlist = models.ForeignKey(PublicationList)
    text = models.TextField()
    link = models.URLField(blank=True, null=True)
    pdf = models.FileField(upload_to=lambda p, *args: CMSPlugin.get_media_path(p.publicationlist,*args), blank=True, null=True)
    bibtex = models.TextField(blank=True)

    def __unicode__(self):
        return self.text

if 'reversion' in settings.INSTALLED_APPS:
    reversion.register(PublicationList, follow=["cmsplugin_ptr", "publication_set"])
    reversion.register(Publication)
