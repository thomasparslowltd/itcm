from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models import CMSPlugin,Page
from publisher import Publisher

if 'reversion' in settings.INSTALLED_APPS:
    import reversion

class SectionHeading(CMSPlugin):
    """A heading
    """
    heading = models.CharField(max_length=255)
    # Level is hidden for the moment but there in case it's needed
    heading_level = models.PositiveIntegerField(default=1,choices=((1,"Primary"),(2,"Secondary")))
    link = models.ForeignKey(Page, help_text="Make the headline clickable by selecting a page here..", blank=True, null=True)
    
    def __unicode__(self):
        return self.heading

if 'reversion' in settings.INSTALLED_APPS:
    reversion.register(SectionHeading, follow=["cmsplugin_ptr"])

