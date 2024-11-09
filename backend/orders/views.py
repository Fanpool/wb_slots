from django.shortcuts import render
from django.views.generic import TemplateView


class WebAppView(TemplateView):
    template_name = 'orders/templates/orders/webapp.html'
