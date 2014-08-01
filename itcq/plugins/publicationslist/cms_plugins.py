from django.contrib import admin
from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from django.utils.translation import ugettext_lazy as _
from itcq.plugins.publicationslist.models import PublicationList, Publication

from django.contrib import admin

class PublicationAdmin(admin.StackedInline):
    model = Publication

class PublicationListPlugin(CMSPluginBase):
    model = PublicationList
    name = _("Publications")
    
    inlines = [
        PublicationAdmin,
    ]
    
    render_template = "itcq/plugins/publicationslist.html"
    

    def render(self, context, instance, placeholder):
        return {"publication_list": instance.publicationpublic_set.all().order_by("id")}
    
plugin_pool.register_plugin(PublicationListPlugin)
