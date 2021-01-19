from django.core import validators
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class SourceImage(models.Model):

    class Meta:
        verbose_name = _('source image')
        verbose_name_plural = _('source images')

        ordering = ['title']

    title = models.CharField(
        verbose_name=_('title'),
        max_length=255,
        db_index=True,
    )

    uploaded = models.DateTimeField(
        verbose_name=_('uploaded'),
        auto_now_add=True,
    )

    image = models.ImageField(
        verbose_name=_('image'),
        upload_to='upload/source_images',
    )

    def __str__(self):
        return self.title


class ModifiedImage(models.Model):

    class Meta:
        verbose_name = _('modified image')
        verbose_name_plural = _('modified images')

        ordering = ['source_image__title', 'width', 'height']

    source_image = models.ForeignKey(
        verbose_name=_('source image'),
        to=SourceImage,
        on_delete=models.CASCADE,
    )

    width = models.PositiveIntegerField(
        verbose_name=_('image width'),
        validators=[
            validators.MinValueValidator(0),
        ]
    )

    height = models.PositiveIntegerField(
        verbose_name=_('image height'),
        validators=[
            validators.MinValueValidator(0),
        ]
    )

    image = models.ImageField(
        verbose_name=_('image'),
        upload_to='upload/modified_images',
    )

    def __str__(self):
        return f'{self.source_image} [{self.width} x {self.height}]'

    def get_absolute_url(self):
        return reverse('image_detail', kwargs=dict(pk=self.pk))


