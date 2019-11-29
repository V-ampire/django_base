from django.views.generic.base import TemplateView


class ToolbarIndexView(TemplateView):
    template_name = 'vampire_toolbar/vampire_toolbar.html'
