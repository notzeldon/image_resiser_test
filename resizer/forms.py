from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from . import models


class DownloadImageForm(forms.Form):

    link = forms.URLField(
        label=_('link'),
    )

    file = forms.FileField(
        label=_('file'),
    )

    def clean(self):
        cd = super().clean()

        link = bool(cd['link'])
        file = bool(cd['file'])

        if not link and not file:
            raise ValidationError(_('Enter link or file'))

        if link and file:
            raise ValidationError(_('You cannot use both fields. Please clear one field'))

        return cd


class ResizeImageModelForm(forms.ModelForm):

    class Meta:
        model = models.ModifiedImage
        fields = ['source_image', 'width', 'height']

