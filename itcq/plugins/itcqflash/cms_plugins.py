from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from django.utils.translation import ugettext_lazy as _
from models import ITCQFlash
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from cms.plugins.flash.forms import FlashForm

class ITCQFlashPlugin(CMSPluginBase):
    model = ITCQFlash
    name = _("Flash (with caption)")
    form = FlashForm
    
    render_template = "itcq/plugins/itcqflash.html"
    def render(self, context, instance, placeholder):
        context.update({
            'object': instance,
            'placeholder':placeholder,
        })
        return context
    
plugin_pool.register_plugin(ITCQFlashPlugin)
