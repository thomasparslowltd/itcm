from django.contrib import admin
from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from django.utils.translation import ugettext_lazy as _
from itcq.plugins.person.models import Person

from django.contrib import admin

class PersonPlugin(CMSPluginBase):
    model = Person
    name = _("Person")
    
    render_template = "itcq/plugins/person.html"
    
    def render(self, context, instance, placeholder):
        return {"person": instance}
    
plugin_pool.register_plugin(PersonPlugin)
