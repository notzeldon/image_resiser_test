import math
from io import BytesIO

from PIL import Image
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
            obj.image.save(name=obj.title, content=ContentFile(self.cleaned_data['link']))
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
        for field_name in ['width', 'height']:
            self.fields[field_name].required = False

    def clean(self):
        cd = super(ResizeImageModelForm, self).clean()
        w = cd['width']
        h = cd['height']

        if not w and not h:
            raise ValidationError(_('Your need enter width or height or both fields'))

        sw = self.source.image.width
        sh = self.source.image.height

        k = sw / sh

        new_w = w
        new_h = h

        if w and h:
            # Умещаем изображение в прямоугольник
            # Чтобы не получить 0, используем ceil
            if w / h > k:
                new_w = math.ceil(h * k)
            else:
                new_h = math.ceil(w / k)

        elif w:
            # Если задана только ширина
            new_h = math.ceil(w / k)

        else:
            # Оставшееся условие - только высота
            new_w = math.ceil(h * k)

        cd['width'] = new_w
        cd['height'] = new_h

        # Пробуем обработать изображение здесь
        dot_pos = self.source.image.name.rfind('.')
        file_format = self.source.image.name[dot_pos + 1:] if dot_pos + 1 < len(self.source.image.name) else 'png'
        if file_format == 'jpg':
            file_format = 'jpeg'

        file_buffer = BytesIO()
        im = Image.open(self.source.image.path)
        im.resize((new_w, new_h))
        try:
            im.save(file_buffer, format=file_format.upper())
            cd['buffer'] = file_buffer
        except:
            self.add_error('__all__', _('Cannot save new image'))
            file_buffer.close()

        return cd

    def save(self, commit=True):
        obj = super().save(commit=False)
        obj.source_image = self.source

        obj.image.save(name=self.source.image.name, content=ContentFile(self.cleaned_data['buffer'].read()))
        self.cleaned_data['buffer'].close()
