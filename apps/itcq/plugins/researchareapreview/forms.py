from django.forms.models import ModelForm
# from cms.plugins.text.models import Text
from itcq.plugins.researchareapreview.models import ResearchAreaPreview
from django import forms


class ResearchAreaPreviewForm(ModelForm):
    class Meta:
        model = ResearchAreaPreview
        exclude = ('page', 'position', 'placeholder', 'language', 'plugin_type')
