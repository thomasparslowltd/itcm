from cms.plugin_pool import plugin_pool
from itcq.plugins.researchareapreview.models import ResearchAreaPreview
#from cms.plugins.text.forms import TextForm
# from cms.plugins.text.cms_plugins import TextPlugin
from djangocms_text_ckeditor.cms_plugins import TextPlugin
from itcq.plugins.researchareapreview.forms import ResearchAreaPreviewForm


class ResearchAreaPreviewPlugin(TextPlugin):
    model = ResearchAreaPreview
    name = "Research Area Preview"
    form = ResearchAreaPreviewForm
    render_template = "cms/plugins/researchareapreview.html"
    # change_form_template = "admin/cms/page/plugin_change_form.html"

    def render(self, context, instance, placeholder):
        context = super(ResearchAreaPreviewPlugin, self).render(context, instance, placeholder)
        context.update({
            'instance': instance,
        })
        return context

plugin_pool.register_plugin(ResearchAreaPreviewPlugin)
