from django.db import models
from django.utils.translation import ugettext_lazy as _
from cms.models import CMSPlugin,Page
from django.conf import settings
from django.utils.html import strip_tags
from django.utils.text import truncate_words
from cms.plugins.text.utils import plugin_admin_html_to_tags,\
    plugin_tags_to_admin_html

if 'reversion' in settings.INSTALLED_APPS:
    import reversion

class ResearchAreaPreview(CMSPlugin):
    heading = models.CharField(_("heading"), max_length=256)
    image = models.ImageField(_("image"), upload_to=CMSPlugin.get_media_path, blank=True, null=True)
    body = models.TextField(_("body"))
    more_link = models.ForeignKey(Page, verbose_name=_("Read more link"), help_text=_("Image, heading and the link at the bottom will all link to this page."), blank=True, null=True)
    
    def _set_body_admin(self, text):
        self.body = plugin_admin_html_to_tags(text)

    def _get_body_admin(self):
        return plugin_tags_to_admin_html(self.body)

    body_for_admin = property(_get_body_admin, _set_body_admin, None,
                              """
                              body attribute, but with transformations
                              applied to allow editing in the
                              admin. Read/write.
                              """)

    
    def __unicode__(self):
        return u"%s" % (truncate_words(strip_tags(self.heading), 3)[:30]+"...")

if 'reversion' in settings.INSTALLED_APPS:        
    reversion.register(ResearchAreaPreview, follow=["cmsplugin_ptr"])
    

