from django.contrib import admin
from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from django.utils.translation import ugettext_lazy as _
from itcq.plugins.heading.models import SectionHeading
from .forms import HeadingForm

from django.contrib import admin

class HeadingPlugin(CMSPluginBase):
    model = SectionHeading
    name = "Section Heading"
    render_template = "itcq/plugins/heading.html"
    form = HeadingForm
    
    def render(self, context, instance, placeholder):
        context = super(HeadingPlugin, self).render(context, instance, placeholder)
        context.update({"heading": instance.heading, "level": instance.heading_level, "link": instance.link})
        return context
    
plugin_pool.register_plugin(HeadingPlugin)
