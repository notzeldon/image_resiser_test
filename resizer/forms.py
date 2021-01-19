from django import forms
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile
from django.utils.translation import ugettext_lazy as _

import requests

from . import models


class DownloadImageForm(forms.Form):

    link = forms.URLField(
        label=_('link'),
        required=False,
    )

    file = forms.FileField(
        label=_('file'),
        required=False,
    )

    def clean(self):
        cd = super().clean()

        link = bool(cd['link'])
        file = bool(cd['file'])

        if not link and not file:
            raise ValidationError(_('Enter link or file'))

        if link and file:
            raise ValidationError(_('You cannot use both fields. Please clear one field'))

        # Проверяем ссылку, скачиваем файл
        if link:
            response = requests.get(cd['link'])
            cd['title'] = cd['link'].split('/')[-1]
            cd['link'] = response.content
        else:
            cd['title'] = cd['file'].name

        return cd

    def save(self):
        obj = models.SourceImage(
            title=self.cleaned_data['title'],
        )
        if self.cleaned_data['link']:
            obj.image = ContentFile(self.cleaned_data['link'])
        else:
            obj.image = self.cleaned_data['file']
        obj.save()
        return obj


class ResizeImageModelForm(forms.ModelForm):

    class Meta:
        model = models.ModifiedImage
        fields = ['width', 'height']

    def __init__(self, *args, source_image: models.SourceImage, **kwargs):
        self.source = source_image
        super().__init__(*args, **kwargs)

