from django.urls import reverse
from django.views import generic

from . import models, forms


class ImageListView(generic.ListView):
    model = models.ModifiedImage
    template_name = 'resizer/image_list.html'
    paginate_by = 50


class ImageDetailView(generic.ListView):
    model = models.ModifiedImage
    template_name = 'resizer/image_detail.html'


class ImageCreateView(generic.FormView):
    form_class = forms.DownloadImageForm
    template_name = 'resizer/image_create.html'

    def form_valid(self, form):
        instance = form.save()
        self.success_url = reverse('image_resize', kwargs=dict(pk=instance.pk))
        return super().form_valid(form)


class ImageResizeView(generic.CreateView):
    form_class = forms.ResizeImageModelForm
    template_name = 'resizer/image_resize.html'


