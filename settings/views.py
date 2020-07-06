from django.shortcuts import render, redirect, get_object_or_404
from settings.models import SiteFaq
from django.views import View, generic

# Create your views here.


class SiteFaqView(generic.ListView):
    model = SiteFaq
    context_object_name = 'faq_list'
    template_name = 'common/site_faq.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Frequently Asked Questions'
        return context
