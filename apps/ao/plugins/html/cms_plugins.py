from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase
from django.utils.translation import ugettext_lazy as _
from models import HTML
from django.forms.fields import CharField
from django.conf import settings
from django.template import Template

class HTMLPlugin(CMSPluginBase):
    model = HTML
    name = _("HTML")
    render_template = "ao/plugins/html.html"

    def render(self, context, instance, placeholder):
        try:
            body = Template(instance.body).render(context)
        except Exception, e:
            print "HTMLPlugin error", repr(e), e
            body = ""
        context.update({
            'body': body
        })
        return context

plugin_pool.register_plugin(HTMLPlugin)
